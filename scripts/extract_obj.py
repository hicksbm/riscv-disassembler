# import necessary libraries
import pandas as pd
import numpy as np
import os
import glob

# import user-defined library
import helper

# use glob to get all the csv files 
# in the folder
path = os.getcwd()
csv_files = glob.glob(os.path.join("../input/*.csv"))

# loop over the list of csv files
for f in csv_files:

    # construct dataframe
    df = pd.read_csv(f)

    # normalize dataframe
    df_array = df.to_numpy().T
    df = pd.DataFrame(df_array[1::], columns=[df_array[0]])

    # identify binaries from 'i_frontend.fetch_entry_o.instruction'
    instruction_binaries = df['id_stage_i.instruction'].to_numpy().flatten()
    instruction_binaries = [helper.to_binary_string(binary) for binary in instruction_binaries]
    instruction_binaries = np.array([int(binary,2) for binary in instruction_binaries], dtype=np.uint32)[np.newaxis]
    instruction_binaries = instruction_binaries.T

    # identify program counts from 'id_stage_i.issue_entry_o.pc'
    instruction_addresses = df['id_stage_i.issue_entry_o.pc'].to_numpy().flatten()
    instruction_addresses = [helper.to_binary_string(binary) for binary in instruction_addresses]
    instruction_addresses = np.array([int(binary,2) for binary in instruction_addresses], dtype=np.uint64)[np.newaxis]
    instruction_addresses = instruction_addresses.T

    # map every address to the corresponding instruction
    # repeat addresses will get overwritten with last executed data
    # include addresses not 0 (mod 4) <-- TODO: Verify this is OK
    inst_addr_concat = np.concatenate((instruction_binaries, instruction_addresses), axis=1)
    instructions = {}
    for (instruction, address) in inst_addr_concat:
        #if (address % 4 == 0):
        instructions[address] = instruction
    
    filename = '../output/' + f[9:-4] + '.bin'
    with open(filename, 'wb') as f:
        for (address, instruction) in sorted(instructions.items()):
            f.write(np.uint64(address))
            f.write(np.uint32(instruction))