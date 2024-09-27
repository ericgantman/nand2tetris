class Parser:
    def __init__(self, fileName: str):
        """Opens the input file/stream, and gets ready to parse it"""
        self.currCommand = ""
        self.current = -1
        self.commands = []
        file = open(fileName)
        for line in file:
            line = line.partition("//")[0]
            line = line.strip()
            if line:
                self.commands.append(line)
        file.close()

    def hasMoreCommands(self) -> bool:
        """Are there more lines in the input"""
        return (self.current + 1) < len(self.commands)

    def advance(self):
        """
        Reads the next command form the input and makes it the current command.
        This method should be called only if hasMoreCommands is true. 
        Initially there is no current command
        """
        self.current += 1
        self.currCommand = self.commands[self.current]

    def commandType(self) -> str:
        """
        Returns the cinstant representing the type of the current command.
        If the current command is and arithmetic-logical command, returns C_ARITHMETIC.
        """
        arithmeticCommands = ["add", "sub", "neg",
                              "eq", "gt", "lt", "and", "or", "not"]
        vmCommand = self.currCommand.split(" ")[0]
        if vmCommand in arithmeticCommands:
            return "C_ARITHMETIC"
        elif vmCommand == "push":
            return "C_PUSH"
        elif vmCommand == "pop":
            return "C_POP"
        elif vmCommand == "label":
            return "C_LABEL"
        elif vmCommand == "goto":
            return "C_GOTO"
        elif vmCommand == "if-goto":
            return "C_IF"
        elif vmCommand == "function":
            return "C_FUNCTION"
        elif vmCommand == "call":
            return "C_CALL"
        elif vmCommand == "return":
            return "C_RETURN"
        else:
            return "Error"

    def arg1(self) -> str:
        """
        Returns the first argument of the current command, In the case of C_ARITHMETIC, the command itself is returned
        Should not be called if the current command is C_RETURN.
        """
        if self.commandType() == "C_ARITHMETIC":
            return self.currCommand.split(" ")[0]
        else:
            return self.currCommand.split(" ")[1]

    def arg2(self) -> int:
        """
        Returns the second argument of the current command.
        Should be called only if the current command is C_PUSH, C_POP, C_FUNCTION, or C_CALL.
        """
        return int(self.currCommand.split(" ")[2])
