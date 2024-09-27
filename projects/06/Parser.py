class Parser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.instructions = []
        self.current_instruction = None
        self.parse()

    def parse(self):
        with open(self.file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('//'):
                    continue
                if '/' in line:
                    line = line.split('/')[0].strip()
                self.instructions.append(line)

    def has_more_lines(self):
        return bool(self.instructions)

    def advance(self):
        self.current_instruction = self.instructions.pop(0)

    def instruction_type(self):
        if self.current_instruction.startswith('@'):
            return "A_INSTRUCTION"
        elif self.current_instruction.startswith('('):
            return "L_INSTRUCTION"
        else:
            return "C_INSTRUCTION"

    def symbol(self):
        if self.instruction_type() == "A_INSTRUCTION":
            return self.current_instruction[1:]
        elif self.instruction_type() == "L_INSTRUCTION":
            return self.current_instruction[1:-1]

    def dest(self):
        if '=' in self.current_instruction:
            return self.current_instruction.split('=')[0]
        else:
            return None

    def comp(self):
        if '=' in self.current_instruction:
            return self.current_instruction.split('=')[1]
        elif ';' in self.current_instruction:
            return self.current_instruction.split(';')[0]
        else:
            return None

    def jump(self):
        if ';' in self.current_instruction:
            return self.current_instruction.split(';')[1]
        else:
            return None
