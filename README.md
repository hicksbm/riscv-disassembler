# RISC-V Disassembler

RISC-V Disassembler with support for RV32/RV64/RV128 IMAFDC

## Build instructions

1. create folder in root called ```build```
2. run ```gcc src/extract_asm.c src/riscv-disas.c -o build/disas.exe```

# Usage instructions

1. create folder in root called ```input```
2. place ```<waveform>.csv``` in ```input```
3. cd into ```scripts``` and run ```extract_obj.py```
4. cd into ```build``` and run ```disas.exe ../output/<waveform>.bin```

# Limitations

1. Branch and jump instruction targets not a part of the execution flow
2. extract_obj.py can be run with or without -order flag.
    - Removing -order gives output asm in same order as execution flow
        1. repeat instructions will be in the as
    - Adding -order gives output asm in order based on the PC value