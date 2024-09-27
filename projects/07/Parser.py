class Parser:
    def __init__(self, fileName: str):
        """Parser Constructor"""
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
        """Checks if there is more work to do"""
        return (self.current + 1) < len(self.commands)

    def advance(self):
        """Gets the next instruction and makes it the current instruction"""
        self.current += 1
        self.currCommand = self.commands[self.current]

    def commandType(self) -> str:
        """Returns the type of the current command"""
        arithmeticCommands = ["add", "sub", "neg",
                              "eq", "gt", "lt", "and", "or", "not"]
        vmCommand = self.currCommand.split(" ")[0]
        if vmCommand in arithmeticCommands:
            return "C_ARITHMETIC"
        elif vmCommand == "push":
            return "C_PUSH"
        elif vmCommand == "pop":
            return "C_POP"
        return "Error"

    def arg1(self) -> str:
        """Returns the first argument of the current command, In the case of C_ARITHMETIC, the command itself is returned"""
        if self.commandType() == "C_ARITHMETIC":
            return self.currCommand.split(" ")[0]
        else:
            return self.currCommand.split(" ")[1]

    def arg2(self) -> int:
        """Returns the second argument of the current command, Called only if the current command is C_PUSH, C_POP, C_FUNCTION, or C_CALL"""
        return int(self.currCommand.split(" ")[2])
