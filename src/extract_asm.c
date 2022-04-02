#include <stdio.h>
#include <stdlib.h>

#include "riscv-disas.h"

#define array_size(arr) (sizeof(arr) / sizeof(arr[0]))

void print_inst(uint64_t pc, uint32_t inst)
{
    char buf[80] = { 0 };
    disasm_inst(buf, sizeof(buf), rv32, pc, inst);
    printf("%016" PRIx64 ":  %s\n", pc, buf);
}

struct inst_t
{
	uint64_t addr;
	uint32_t inst;
};

void run(const char* filename)
{
	FILE *fptr = fopen(filename, "rb");
	if (fptr == NULL) {
		printf("Error! File not opened\n");
		exit(1);
	}
	
	struct inst_t instruction;
	while (fread(&instruction, 12, 1, fptr)) {//read until end of file
		print_inst(instruction.addr, instruction.inst);		
    }
}

int main(int argc, char **argv)
{
	if (argc < 2) {
		printf("Error! Missing filename argument!\n");
		exit(1);
	}
    run(argv[1]);
}
