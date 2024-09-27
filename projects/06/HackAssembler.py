from Parser import Parser
from SymbolTable import SymbolTable
from Code import Code


class HackAssembler:
    def __init__(self, parser):
        self.parser = parser
        self.symbol_table = SymbolTable()
        self.code = Code()

    def assemble(self, output_file_path):
        self.first_pass()
        self.second_pass(output_file_path)

    def first_pass(self):
        ram_address = 0
        while self.parser.has_more_lines():
            self.parser.advance()
            if self.parser.instruction_type() == "L_INSTRUCTION":
                symbol = self.parser.symbol()
                self.symbol_table.add_entry(symbol, ram_address)
            else:
                ram_address += 1

    def second_pass(self, output_file_path):
        ram_address = 16
        with open(output_file_path, 'w') as output_file:
            self.parser.__init__(self.parser.file_path)
            while self.parser.has_more_lines():
                self.parser.advance()
                if self.parser.instruction_type() == "A_INSTRUCTION":
                    symbol = self.parser.symbol()
                    if symbol.isdigit():
                        binary_address = format(int(symbol), '016b')
                    else:
                        if not self.symbol_table.contains(symbol):
                            self.symbol_table.add_entry(symbol, ram_address)
                            ram_address += 1
                        binary_address = format(
                            self.symbol_table.get_address(symbol), '016b')
                    output_file.write(f"{binary_address}\n")
                elif self.parser.instruction_type() == "C_INSTRUCTION":
                    dest = self.code.dest(self.parser.dest())
                    comp = self.code.comp(self.parser.comp())
                    jump = self.code.jump(self.parser.jump())
                    output_file.write(f"111{comp}{dest}{jump}\n")
                elif self.parser.instruction_type() == "L_INSTRUCTION":
                    pass
