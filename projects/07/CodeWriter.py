class CodeWriter:
    def __init__(self, file_name: str):
        """Opens an output file/stream and gets ready to write into it"""
        self.file_name = file_name[:-4]
        self.file = open(file_name, "w")
        self.label_counter = 0
        self.currFile = ""
        self.symbols = {
            "add": "M=D+M",
            "sub": "M=M-D",
            "and": "M=D&M",
            "or": "M=D|M",
            "neg": "M=-M",
            "not": "M=!M",
            "eq": "D;JEQ",
            "gt": "D;JGT",
            "lt": "D;JLT",
            "local": "@LCL",
            "argument": "@ARG",
            "this": "@THIS",
            "that": "@THAT",
            "constant": "",
            "static": "",
            "pointer": "@3",
            "temp": "@5"
        }

    def writeArithmetic(self, command: str):
        """Writes to the output file the assembly code tha implements the arithmetic-logical command"""
        output = []
        if command in ["add", "sub", "and", "or"]:
            output.append("@SP")
            output.append("AM=M-1")
            output.append("D=M")
            output.append("@SP")
            output.append("A=M-1")
            output.append(self.symbols[command])
        elif command in ["neg", "not"]:
            output.append("@SP")
            output.append("A=M-1")
            output.append(self.symbols[command])
        elif command in ["eq", "gt", "lt"]:
            jumpLabel = "CompLabel" + str(self.label_counter)
            self.label_counter += 1
            output.append("@SP")
            output.append("AM=M-1")
            output.append("D=M")
            output.append("@SP")
            output.append("A=M-1")
            output.append("D=M-D")
            output.append("M=-1")
            output.append("@" + jumpLabel)
            output.append(self.symbols[command])
            output.append("@SP")
            output.append("A=M-1")
            output.append("M=0")
            output.append("(" + jumpLabel + ")")
        output.append("")  # Enter line
        for line in output:
            print(line, file=self.file)

    def writePushPop(self, command: str, segment: str, index: int):
        """Writes to the output file the assembly code tha implements the given push or pop command"""
        output = []
        if command == "C_PUSH":
            if segment == "constant":
                output.append("@" + str(index))
                output.append("D=A")
                output.append("@SP")
                output.append("AM=M+1")
                output.append("A=A-1")
                output.append("M=D")
            elif segment in ["local", "argument", "this", "that", "temp", "pointer"]:
                output.append("@" + str(index))
                output.append("D=A")
                if segment == "temp" or segment == "pointer":
                    output.append(self.symbols[segment])
                else:
                    output.append(self.symbols[segment])
                    output.append("A=M")
                output.append("A=D+A")
                output.append("D=M")
                output.append("@SP")
                output.append("A=M")
                output.append("M=D")
                output.append("@SP")
                output.append("M=M+1")
            elif segment == "static":
                output.append("@" + self.currFile + "." + str(index))
                output.append("D=M")
                output.append("@SP")
                output.append("A=M")
                output.append("M=D")
                output.append("@SP")
                output.append("M=M+1")
        elif command == "C_POP":
            if segment in ["local", "argument", "this", "that", "temp", "pointer"]:
                output.append("@" + str(index))
                output.append("D=A")
                if segment == "temp" or segment == "pointer":
                    output.append(self.symbols[segment])
                else:
                    output.append(self.symbols[segment])
                    output.append("A=M")
                output.append("D=D+A")
                output.append("@R13")
                output.append("M=D")
                output.append("@SP")
                output.append("AM=M-1")
                output.append("D=M")
                output.append("@R13")
                output.append("A=M")
                output.append("M=D")
            elif segment == "static":
                output.append("@SP")
                output.append("AM=M-1")
                output.append("D=M")
                output.append("@" + self.currFile + "." + str(index))
                output.append("M=D")
        output.append("")  # Enter line
        for line in output:
            print(line, file=self.file)

    def close(self):
        """Closes the output file"""
        self.file.close()

    def writeComment(self, command: str):
        """writes to the output the comment"""
        print("// " + command, file=self.file)

    def setFileName(self, file):
        self.currFile = file
