import sys
import os
from os.path import splitext
from Parser import Parser
from HackAssembler import HackAssembler


def main():
    file_path = sys.argv[1]
    if os.path.isdir(file_path):
        # If it's a folder, assemble all .asm files in the folder
        for file_name in os.listdir(file_path):
            if file_name.endswith(".asm"):
                file_path_full = os.path.join(file_path, file_name)
                assemble_file(file_path_full)
    elif os.path.isfile(file_path) and file_path.endswith(".asm"):
        # If it's one .asm file, assemble it
        assemble_file(file_path)


def assemble_file(file_path):
    parser = Parser(file_path)
    assembler = HackAssembler(parser)
    output_file_path = splitext(file_path)[0] + ".hack"
    assembler.assemble(output_file_path)


if __name__ == "__main__":
    main()
