# RISC-V Disassembler

RISC-V Disassembler with support for RV32/RV64/RV128 IMAFDC

1. add the desired input files to the ```input``` folder
2. execute ```run.py``` in the root directory

# Limitations

1. Branch and jump instruction targets not a part of the execution flow
    - executing the output assembly is not guarunteed to produce same instructions or same order of execution
    - output assembly may not compile