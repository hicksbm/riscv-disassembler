# import necessary libraries
import subprocess
import pandas as pd
import numpy as np
import os
import glob

# import user-defined library
from scripts import helper

# use glob to get all the csv files 
# in the folder
path = os.getcwd()
csv_files = glob.glob(os.path.join("input/**/*.csv"), recursive=True)

# create output folder
if not os.path.isdir('output'):
    os.mkdir('output')
# create build folder
if not os.path.isdir('build'):
    os.mkdir('build')

# loop over the list of csv files, create compressed and full binaries for all of them
for f in csv_files:

    # construct dataframe
    df = pd.read_csv(f)

    # normalize dataframe
    df_array = df.to_numpy().T
    df = pd.DataFrame(df_array[1::], columns=[df_array[0]])

    f = f.replace('input\\','', 1)

    # identify binaries from 'i_frontend.fetch_entry_o.instruction'
    if 'id_stage_i.instruction' not in df:
        print('id_stage_i.instruction not in ' + f)
        continue
    instruction_binaries = df['id_stage_i.instruction'].to_numpy().flatten()
    instruction_binaries = [helper.to_binary_string(binary) for binary in instruction_binaries]
    instruction_binaries = np.array([int(binary,2) for binary in instruction_binaries], dtype=np.uint32)[np.newaxis]
    instruction_binaries = instruction_binaries.T

    # identify program counts from 'id_stage_i.decoded_instruction.pc'
    if 'id_stage_i.decoded_instruction.pc' not in df:
        print('id_stage_i.decoded_instruction.pc not in ' + f)
        continue
    instruction_addresses = df['id_stage_i.decoded_instruction.pc'].to_numpy().flatten()
    instruction_addresses = [helper.to_binary_string(binary) for binary in instruction_addresses]
    instruction_addresses = np.array([int(binary,2) for binary in instruction_addresses], dtype=np.uint64)[np.newaxis]
    instruction_addresses = instruction_addresses.T

    # create directory in output folder
    directory = 'output/'+f[:-4]
    os.makedirs(directory, exist_ok=True)

    full_instruction_filename = directory + '/full.bin'
    comp_instruction_filename = directory + '/comp.bin'

    with open(full_instruction_filename, 'wb') as file:
        for i in range(len(instruction_addresses)):
            file.write(np.uint64(instruction_addresses[i]))
            file.write(np.uint32(instruction_binaries[i]))
    
    with open(comp_instruction_filename, 'wb') as file:
        # write a single initializing add x0, x0, 0 instruction, with PC = 0
        file.write(np.uint64(0))
        file.write(np.uint32(0))

        valid_found = False
        for i in range(len(instruction_addresses)):
            # don't write the initializing add x0, x0, 0 until first occurence of different instruction
            if (valid_found or instruction_binaries[i] != 0):
                valid_found = True
                file.write(np.uint64(instruction_addresses[i]))
                file.write(np.uint32(instruction_binaries[i]))


# re-compile the src code, use subprocess so we wait until compilation completes
process = subprocess.Popen(['gcc', 'src/extract_asm.c', 'src/riscv-disas.c', '-o', 'build/disas.exe'])
process.communicate()

# loop over the list of bin files, create asm code for all of them

# use glob to get all the bin files 
# in the folder
path = os.getcwd()
bin_files = glob.glob(os.path.join("output/**/*.bin"), recursive=True)

for f in bin_files:
    subprocess.Popen(['build/disas.exe', f])
