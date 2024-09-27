KEYWORD = 'KEYWORD'
SYMBOL = 'SYMBOL'
IDENTIFIER = 'IDENTIFIER'
INT_CONST = 'INT_CONST'
STRING_CONST = 'STRING_CONST'
KEYWORD_DICT = {'class': 'CLASS',
                'constructor': 'CONSTRUCTOR',
                'function': 'FUNCTION',
                'method': 'METHOD',
                'field': 'FIELD',
                'static': 'STATIC',
                'var': 'VAR',
                'int': 'INT',
                'char': 'CHAR',
                'boolean': 'BOOLEAN',
                'void': 'VOID',
                'true': 'TRUE',
                'false': 'FALSE',
                'null': 'NULL',
                'this': 'THIS',
                'let': 'LET',
                'do': 'DO',
                'if': 'IF',
                'else': 'ELSE',
                'while': 'WHILE',
                'return': 'RETURN'
                }


class JackTokenizer:
    def __init__(self, jkfile_name):
        self.jkfile_name = jkfile_name
        with open(jkfile_name, 'r') as file:
            self.contents = file.read()
        # self.token_list = self.list_of_tokens()
        self.content_no_cmt = self.clean_comment()
        self.curr_token = None
        self.curr_token_place = 0
        self.token_type = None
        self.symbols = ['{', '}', '(', ')', '[', ']', '.', ',',
                        ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']

    def hasMoreTokens(self):
        return self.curr_token_place < len(self.content_no_cmt)

    def advance(self):
        while self.content_no_cmt[self.curr_token_place] == " ":
            self.curr_token_place += 1
        temp = ""
        # SYMBOL
        if self.content_no_cmt[self.curr_token_place] in self.symbols:
            self.curr_token = self.content_no_cmt[self.curr_token_place]
            self.token_type = SYMBOL
            self.curr_token_place += 1
        # STRING CONST
        elif self.content_no_cmt[self.curr_token_place] == '"':
            self.curr_token_place += 1
            self.token_type = STRING_CONST
            while self.content_no_cmt[self.curr_token_place] != '"':
                temp += self.content_no_cmt[self.curr_token_place]
                self.curr_token_place += 1
            self.curr_token = temp
            self.curr_token_place += 1
        # INT CONST
        elif self.content_no_cmt[self.curr_token_place].isdigit():
            while self.content_no_cmt[self.curr_token_place].isdigit():
                temp += self.content_no_cmt[self.curr_token_place]
                self.curr_token_place += 1
            self.curr_token = temp
            self.token_type = INT_CONST
        # KEYWORD
        else:
            while self.content_no_cmt[self.curr_token_place] != " " and self.content_no_cmt[self.curr_token_place] not in self.symbols:
                temp += self.content_no_cmt[self.curr_token_place]
                self.curr_token_place += 1
            if temp in KEYWORD_DICT:
                self.curr_token = temp
                self.token_type = KEYWORD
        # IDENTIFIER
            else:
                self.token_type = IDENTIFIER
                self.curr_token = temp

    def tokenType(self):
        return self.token_type

    def keyWord(self):
        return KEYWORD_DICT[self.curr_token]

    def symbol(self):
        return self.curr_token

    def identifier(self):
        return self.curr_token

    def intVal(self) -> int:
        return int(self.curr_token)

    def stringVal(self) -> str:
        return self.curr_token

    def clean_comment(self):
        no_commemts = ""
        lines = self.contents.split('\n')
        lines = [line.strip() for line in lines]
        lines = [line.split('//')[0] for line in lines]
        comments = False
        for i, ln in enumerate(lines):
            start, end = ln[:2], ln[-2:]
            if start == '/*':
                comments = True
            if comments:
                lines[i] = ''
            if start == '*/' or end == '*/':
                comments = False
        for line in lines:
            no_commemts += line
        return no_commemts
