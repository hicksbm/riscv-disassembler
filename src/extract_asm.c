#include <stdio.h>
#include <stdlib.h>

#include "riscv-disas.h"

#define array_size(arr) (sizeof(arr) / sizeof(arr[0]))

void remove_first_word(char* str) {
	if (str != NULL) {
		int startOfSecondWord = 0;
		bool foundFirstNonSpace = false;
		bool foundFirstSpaceAfterNonSpace = false;
		bool foundFirstNonSpaceAfterFirstWord = false;
		while(str[startOfSecondWord] != 0 && !foundFirstNonSpaceAfterFirstWord) {
			if (!foundFirstNonSpace && str[startOfSecondWord != ' ']) {
				foundFirstNonSpace = true;
				startOfSecondWord++;
			} else if (!foundFirstSpaceAfterNonSpace && str[startOfSecondWord] == ' ') {
				foundFirstSpaceAfterNonSpace = true;
			} else if (foundFirstSpaceAfterNonSpace && str[startOfSecondWord] != ' ') {
				foundFirstNonSpaceAfterFirstWord = true;
			} else {
				startOfSecondWord++;
			}
		}

		if (!foundFirstNonSpaceAfterFirstWord) str[0] = 0; // delete entire string
		int i = 0;
		int j = startOfSecondWord;
		for (; str[j] != 0;) {
			str[i++] = str[j++];
		}
		str[i] = 0; // append null char
	}
}

void print_inst(const char* filename, uint64_t pc, uint32_t inst)
{
    char buf[80] = { 0 };
    disasm_inst(buf, sizeof(buf), rv64, pc, inst);
    printf("%016" PRIx64 ":  %s\n", pc, buf);

	// append the instruction to input file
	FILE *writeFilePtr = fopen(filename, "a");
	if (writeFilePtr == NULL) {
		printf("Error! File not opened\n");
		exit(1);
	}

	remove_first_word(buf); // get's rid of instruction word
	fprintf(writeFilePtr, "%s\n", buf);
}

struct inst_t
{
	uint64_t addr;
	uint32_t inst;
};

void run(const char* filename)
{
	FILE *readFilePtr = fopen(filename, "rb");
	if (readFilePtr == NULL) {
		printf("Error! File not opened\n");
		exit(1);
	}

	char writeFilename[80];
	strcpy(writeFilename, filename);

	// remove .bin extension from filename and add .s extension
	int filenameLength = strlen(writeFilename);
	writeFilename[filenameLength-3] = 's';
	writeFilename[filenameLength-2] = 0;
	FILE *writeFilePtr = fopen(writeFilename, "w");
	if (writeFilePtr == NULL) {
		printf("Error! File not opened\n");
		exit(1);
	}

	// write _start: to beginning of file
	fprintf(writeFilePtr, ".section .text\n.globl _start\n\n_start:\n");

	// write initializing instruction
	fprintf(writeFilePtr, "add           x0,x1,x2\n");

	// close writeFilePtr
	fclose(writeFilePtr);
	
	struct inst_t instruction;
	while (fread(&instruction, 12, 1, readFilePtr)) {//read until end of file
		print_inst(writeFilename, instruction.addr, instruction.inst);		
    }

	// reopen writeFilePtr to append "end:"

	writeFilePtr = fopen(writeFilename, "a");

	fprintf(writeFilePtr, "end:\n");
}

int main(int argc, char **argv)
{
	if (argc < 2) {
		printf("Error! Missing filename argument!\n");
		exit(1);
	}
    run(argv[1]);
}
