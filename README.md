# RISC-V Disassembler

RISC-V Disassembler with support for RV32/RV64/RV128 IMAFDC

## Build instructions

1. run ```gcc src/extract_asm.c src/riscv-disas.c -o build/disas.exe```

# Usage instructions

1. create folder in root called ```input```
2. place ```<waveform>.csv``` in ```input```
3. cd into ```scripts``` and run ```extract_obj.py```
4. cd into ```build``` and run ```disas.exe ../output/<waveform>.bin```