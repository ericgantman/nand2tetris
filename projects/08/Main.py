from Parser import Parser
from CodeWriter import CodeWriter
import sys
import os


def translateFile(filePath, codeWriter):
    # Create a Parser instance for the input VM file.
    parser = Parser(filePath)
    # Gets the current working file
    codeWriter.setFileName(os.path.basename(filePath)[:-3])
    # Translate VM commands to assembly code.
    while parser.hasMoreCommands():
        parser.advance()
        codeWriter.writeComment(parser.currCommand)
        commandType = parser.commandType()
        if commandType == "C_ARITHMETIC":
            codeWriter.writeArithmetic(parser.arg1())
        elif commandType in ["C_PUSH", "C_POP"]:
            codeWriter.writePushPop(commandType, parser.arg1(), parser.arg2())
        elif commandType == "C_LABEL":
            codeWriter.writeLabel(parser.arg1())
        elif commandType == "C_GOTO":
            codeWriter.writeGoTo(parser.arg1())
        elif commandType == "C_IF":
            codeWriter.writeIf(parser.arg1())
        elif commandType == "C_FUNCTION":
            codeWriter.setCurrFunctionName(parser.arg1())
            codeWriter.writeFunction(parser.arg1(), parser.arg2())
        elif commandType == "C_CALL":
            codeWriter.writeCall(parser.arg1(), parser.arg2())
        elif commandType == "C_RETURN":
            codeWriter.writeReturn()
    # codeWriter.close()


def translateDirectory(directoryPath, codeWriter):
    # Get all .vm files in the specified directory.
    vmFiles = [f for f in os.listdir(directoryPath) if f.endswith(".vm")]
    # Check if Sys.vm is present
    if "Sys.vm" in vmFiles:
        # Write bootstrap code if Sys.vm is present
        codeWriter.writeBootstrap()
    # Translate each VM file in the directory.
    for vmFile in vmFiles:
        vmFilePath = os.path.join(directoryPath, vmFile)
        translateFile(vmFilePath, codeWriter)


def main():
    # Check if a valid number of arguments is provided.
    if len(sys.argv) != 2:
        return
    # Get the input path from the command line argument.
    inputPath = sys.argv[1]
    # Create a CodeWriter instance with the output file path.
    if os.path.isdir(inputPath):
        # If the input is a directory, create a single output file in that directory.
        outputFilePath = os.path.join(
            inputPath, os.path.basename(inputPath) + ".asm")
        codeWriter = CodeWriter(outputFilePath)
        translateDirectory(inputPath, codeWriter)


if __name__ == "__main__":
    main()
