# RISC-V Disassembler

RISC-V Disassembler with support for RV32/RV64/RV128 IMAFDC

## Build instructions

1. run ```gcc src/extract_asm.c src/riscv-disas.c -o build/disas.exe```

# Usage instructions

1. place ```<waveform>.csv``` in input folder
2. cd into ```scripts``` and run ```extract_obj.py```
3. cd into ```build``` and run ```disas.exe ../output/<waveform>.bin```