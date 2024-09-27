class CodeWriter:
    def __init__(self, file_name: str):
        """Opens an output file/stream and gets ready to write into it"""
        self.file = open(file_name, "w")
        self.labelCounter = 0
        self.retCounter = 0
        self.currFunctionName = ""
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
            jumpLabel = "CompLabel" + str(self.labelCounter)
            self.labelCounter += 1
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

    def writeLabel(self, label):
        """Writes assembly code that effects the label command"""
        print(f"({self.currFunctionName}${label})", file=self.file)

    def writeGoTo(self, label):
        """Writes assembly code that effects the goto command"""
        print(f"@{self.currFunctionName}${label}", file=self.file)
        print("0;JMP", file=self.file)

    def writeIf(self, label):
        """Writes assembly code that effects the if-goto command"""
        output = ["@SP", "M=M-1", "A=M", "D=M",
                  f"@{self.currFunctionName}${label}", "D;JNE"]
        for line in output:
            print(line, file=self.file)

    def writeFunction(self, functionName, nVars):
        """Writes assembly code that effects the function command"""
        self.retCounter = 0  # Sets retCounter to zero
        self.setCurrFunctionName(functionName)
        output = [f"({functionName})", "@LCL", "A=M"]
        for i in range(nVars):
            # Initialize local variables to 0
            output.extend(["M=0", "A=A+1", "D=A", "@SP", "M=M+1", "A=D"])
        # output.append("")  # Empty line
        for line in output:
            print(line, file=self.file)

    def writeCall(self, functionName, nArgs):
        """Writes assembly code that effects the call command"""
        returnLabel = f"{self.currFunctionName}$ret.{self.retCounter}"
        output = [f'@{returnLabel}', "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1", "@LCL", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1", "@ARG", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1", "@THIS", "D=M", "@SP", "A=M", "M=D",
                  "@SP", "M=M+1", "@THAT", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1", "@SP", "D=M", "@5", "D=D-A", f"@{nArgs}", "D=D-A", "@ARG", "M=D", "@SP", "D=M", "@LCL", "M=D", f"@{functionName}", "0;JMP", f'({returnLabel})']
        for line in output:
            print(line, file=self.file)
        self.retCounter += 1

    def writeReturn(self):
        """Writes assembly code that effects the return command"""
        output = ["@LCL", "D=M", "@R13", "M=D", "@R13", "D=M", "@5", "D=D-A", "A=D", "D=M", "@R14", "M=D", "@SP", "M=M-1", "A=M", "D=M", "@ARG", "A=M", "M=D", "@ARG", "D=M", "@SP", "M=D+1", "@R13", "D=M", "@1", "D=D-A", "A=D", "D=M",
                  "@THAT", "M=D", "@R13", "D=M", "@2", "D=D-A", "A=D", "D=M", "@THIS", "M=D", "@R13", "D=M", "@3", "D=D-A", "A=D", "D=M", "@ARG", "M=D", "@R13", "D=M", "@4", "D=D-A", "A=D", "D=M", "@LCL", "M=D", "@R14", "A=M", "0;JMP"]
        for line in output:
            print(line, file=self.file)

    def close(self):
        """Closes the output file"""
        self.file.close()

    def writeComment(self, command: str):
        """Writes to the output the comment"""
        print(f"// {command}", file=self.file)

    def setFileName(self, fileName):
        """Informs that the translation of a new VM file has started (called by the VMTranslator)."""
        self.currFile = fileName

    def setCurrFunctionName(self, function_name):
        """Sets the name of the current working function"""
        self.currFunctionName = function_name

    def writeBootstrap(self):
        """Writes to the output the Bootstrap commands"""
        output = []
        output.extend(["@256", "D=A", "@SP", "M=D"])
        for line in output:
            print(line, file=self.file)
        self.writeCall('Sys.init', 0)
