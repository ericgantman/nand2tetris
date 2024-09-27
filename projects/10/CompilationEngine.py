from JackTokenizer import *


class CompilationEngine:
    def __init__(self, jack_filename):
        filename_pieces = jack_filename.split('/')
        # Avoid overwriting original file
        # filename_pieces[-1] = 'My' + filename_pieces[-1]
        xml_filename = '/'.join(filename_pieces).replace('.jack', '.xml')
        self.tokenizer = JackTokenizer(jack_filename)
        self.xml = open(xml_filename, 'w')
        self.indent = 0
        # self.write('<tokens>\n')
        # self.updent()

    def compile_class(self):
        """Compiles a complete class."""
        self.start_nonterminal("class")
        self.tokenizer.advance()  # Compile 'class' keyword
        self.write_token()
        self.write_token()  # Compile class name
        self.write_token()  # '{'
        # Compile classVarDec*
        while self.tokenizer.tokenType() == KEYWORD and self.tokenizer.keyWord() in ["FIELD", "STATIC"]:
            self.compileClassVarDec()
        # Compile subroutineDec*
        while self.tokenizer.tokenType() == KEYWORD and self.tokenizer.keyWord() in ["CONSTRUCTOR", "FUNCTION", "METHOD"]:
            self.compileSubroutine()
        # Compile '}'
        self.write_token()  # Compile '}'
        self.end_nonterminal("class")
        self.xml.close()

    def compileClassVarDec(self):
        """Compiles a static variable declaration, or a field declaration."""
        self.start_nonterminal("classVarDec")
        # Compile 'static' or 'field' keyword
        self.write_token()  # handle keywords
        # Compile variable type
        self.write_token()  # handle variable types
        # Compile variable names
        self.write_token()  # Implement this function to handle variable names
        # Compile additional variable names if present
        while self.tokenizer.tokenType() == SYMBOL and self.tokenizer.symbol() == ",":
            # Implement this function to handle symbols
            self.write_token()
            self.write_token()  # Implement this function to handle variable names
        # Compile semicolon
        self.write_token()
        self.end_nonterminal("classVarDec")

    def compileSubroutine(self):
        """Compiles a complete method, function, or constructor."""
        self.start_nonterminal("subroutineDec")
        # Compile 'constructor', 'function', or 'method' keyword
        self.write_token()
        # Compile return type
        self.write_token()
        # Compile subroutine name
        self.write_token()  # Implement this function to handle identifiers

        # Compile parameter list
        self.write_token()  # write '('
        self.compileParameterList()
        self.write_token()  # write ')'
        # Compile subroutine body
        self.compileSubroutineBody()  # handle subroutine bodies
        self.end_nonterminal("subroutineDec")

    def compileParameterList(self):
        """Compiles a (possibly empty) parameter list. Does not handle the enclosing parentheses tokens ( and )."""
        self.start_nonterminal("parameterList")
        # Compile parameter type
        while self.tokenizer.tokenType() != SYMBOL:
            self.write_token()  # handle variable types
            self.write_token()  # parameter name
            if self.tokenizer.symbol() == ",":
                self.write_token()
        self.end_nonterminal("parameterList")

    def compileSubroutineBody(self):
        """Compiles a subroutine's body."""
        self.start_nonterminal("subroutineBody")
        self.write_token()  # Compile '{'
        # Compile var declarations
        while self.tokenizer.tokenType() == "KEYWORD" and self.tokenizer.keyWord() == "VAR":
            self.compileVarDec()  # Implement this function to handle var declarations
        # Compile statements
        self.compileStatements()
        self.write_token()  # write '}'
        self.end_nonterminal("subroutineBody")

    def compileVarDec(self):
        """Compiles a var declaration."""
        self.start_nonterminal("varDec")
        # Compile 'var' keyword
        self.write_token()
        # Compile variable type
        self.write_token()
        # Compile variable name
        self.write_token()  # Implement this function to handle identifiers
        # Compile optional additional variable names
        while self.tokenizer.tokenType() == "SYMBOL" and self.tokenizer.symbol() == ",":
            # Implement this function to handle symbols
            self.write_token()
            self.write_token()  # handle identifiers
        # Compile ';'
        self.write_token()  # handle ";"
        self.end_nonterminal("varDec")

    def compileStatements(self):
        """Compiles a sequence of statements. Does not handle the enclosing curly bracket tokens { and }."""
        self.start_nonterminal("statements")
        # Compile each statement until a closing curly brace is encountered
        while self.tokenizer.tokenType() == "KEYWORD" and self.tokenizer.keyWord() in ["LET", "IF", "WHILE", "DO", "RETURN"]:
            keyword = self.tokenizer.keyWord()
            if keyword == "LET":
                self.compileLet()  # Implement this function to handle let statements
            elif keyword == "IF":
                self.compileIf()  # Implement this function to handle if statements
            elif keyword == "WHILE":
                self.compileWhile()  # Implement this function to handle while statements
            elif keyword == "DO":
                self.compileDo()  # Implement this function to handle do statements
            elif keyword == "RETURN":
                self.compileReturn()  # Implement this function to handle return statements
        self.end_nonterminal("statements")

    def compileDo(self):
        """Compiles a do statement"""
        self.start_nonterminal("doStatement")
        # Compile 'do' keyword
        self.write_token()  # do
        # call #
        self.write_token()
        if self.tokenizer.symbol() == ".":
            self.write_token()  # "."
            self.write_token()  # identifier (subroutine name)
        self.write_token()  # '('
        self.compileExpressionList()
        self.write_token()  # ')'
        # end call #
        self.write_token()  # ";"
        self.end_nonterminal("doStatement")

    def compileLet(self):
        """Compiles a let statement"""
        self.start_nonterminal("letStatement")
        # Compile 'let' keyword
        self.write_token()
        self.write_token()  # name
        # Compile optional array indexing
        if self.tokenizer.symbol() == "[":
            # Implement this function to handle symbols
            self.write_token()  # write "["
            self.compileExpression()  # handle expressions
            # Implement this function to handle symbols
            self.write_token()  # write "["
        # Compile '=' symbol
        self.write_token()  # Write '='
        # Compile expression
        self.compileExpression()  # handle expressions
        # Compile semicolon
        self.write_token()  # Write ";"
        self.end_nonterminal("letStatement")

    def compileWhile(self):
        """Compiles a while statement"""
        self.start_nonterminal("whileStatement")
        # Compile 'while' keyword
        self.write_token()  # handle keywords
        # Compile '(' symbol
        self.write_token()  # handle symbol "("
        # Compile expression
        self.compileExpression()  # Implement this function to handle expressions
        # Compile ')' symbol
        self.write_token()  # handle symbol ")"
        # Compile '{' symbol
        self.write_token()  # handle symbol "{"
        # Compile statements
        self.compileStatements()  # Implement this function to handle statements
        # Compile '}' symbol
        self.write_token()  # handle symbol "}"
        self.end_nonterminal("whileStatement")

    def compileReturn(self):
        """Compiles a return statement"""
        self.start_nonterminal("returnStatement")
        # Compile 'return' keyword
        self.write_token()  # handle keywords
        # Check if there's an expression
        while self.tokenizer.symbol() != ";":
            # Compile expression
            self.compileExpression()  # handle expressions
        # Compile ';' symbol
        self.write_token()  # ";"
        self.end_nonterminal("returnStatement")

    def compileIf(self):
        """Compiles an if statement"""
        self.start_nonterminal("ifStatement")
        # Compile 'if' keyword
        self.write_token()
        # Compile '(' symbol
        self.write_token()
        # Compile expression
        self.compileExpression()  # Implement this function to handle expressions
        self.write_token()  # ")"
        self.write_token()  # "{"
        # Compile statements
        self.compileStatements()  # Implement this function to handle statements
        self.write_token()  # "}"
        # Check for optional 'else' clause
        if self.tokenizer.tokenType() == KEYWORD and self.tokenizer.keyWord() == 'ELSE':
            # Compile 'else' keyword
            self.write_token()
            # Compile '{' symbol
            self.write_token()
            # Compile statements
            self.compileStatements()  # Implement this function to handle statements
            # Compile '}' symbol
            self.write_token()
        self.end_nonterminal("ifStatement")

    def compileExpression(self):
        """Compiles an expression."""
        self.start_nonterminal("expression")
        # Compile term
        self.compileTerm()  # Implement this function to handle terms
        # Compile optional term and operator pairs
        while self.tokenizer.tokenType() == SYMBOL and self.tokenizer.symbol() in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
            # Compile operator
            self.write_token()  # handle symbols
            # Compile term
            self.compileTerm()  # Implement this function to handle terms
        self.end_nonterminal("expression")

    def compileTerm(self):
        """
        Compiles a term. If the current token is an identifier, the routine must resolve it into a variable, an array entry, or a subroutine call. A single lookahead token, which may be [, (, or ., suffices to distinguish between the possibilities.
        Any other token is not part of this term and should not be advanced over.
        """
        self.start_nonterminal("term")
        # Handle integer constant
        if self.tokenizer.tokenType() == INT_CONST or self.tokenizer.tokenType() == STRING_CONST:
            self.write_token()
        # Handle string constant
        # Handle keyword constant
        elif self.tokenizer.tokenType() == KEYWORD:
            self.write_token()  # Implement this function to handle keyword constants
        # Handle unaryOp term
        elif self.tokenizer.tokenType() == SYMBOL and self.tokenizer.symbol() in ["-", "~"]:
            self.write_token()  # Implement this function to handle unary operators
            self.compileTerm()  # Recursively compile the following term
        # Handle expression in parentheses
        elif self.tokenizer.tokenType() == SYMBOL and self.tokenizer.symbol() == "(":
            self.write_token()  # opening parenthesis
            self.compileExpression()  # Compile the expression within parentheses
            # Implement this function to handle the closing parenthesis
            self.write_token()  # ")"
        # Handle varName | varName '[' expression ']' | subroutineCall
        elif self.tokenizer.tokenType() == "IDENTIFIER":
            self.write_token()
            if self.tokenizer.tokenType() == SYMBOL and self.tokenizer.symbol() == "[":
                self.write_token()  # "["
                self.compileExpression()
                self.write_token()  # "]"
            if self.tokenizer.tokenType() == SYMBOL and self.tokenizer.symbol() == "(":
                self.write_token()  # "("
                self.compileExpression()
                self.write_token()  # ")"
            if self.tokenizer.tokenType() == SYMBOL and self.tokenizer.symbol() == ".":
                self.write_token()  # '.'
                self.write_token()  # subroutine name
                self.write_token()  # '('
                self.compileExpressionList()
                self.write_token()  # ')'
        self.end_nonterminal("term")

    def compileExpressionList(self):
        """
        Compiles a (possibly empty) comma-separated list of expressions.
        """
        self.start_nonterminal("expressionList")
        # Check if there are any expressions to compile
        if self.tokenizer.tokenType() != "SYMBOL" or self.tokenizer.symbol() != ")":
            self.compileExpression()  # Compile the first expression
            # Compile subsequent expressions, if any
            while self.tokenizer.tokenType() == "SYMBOL" and self.tokenizer.symbol() == ",":
                # Implement this function to handle the comma symbol
                self.write_token()  # ","
                self.compileExpression()  # Compile the next expression
        self.end_nonterminal("expressionList")

    # end of API  #
    def start_nonterminal(self, content):
        self.xml.write(' ' * self.indent + '<' + content + '>\n')
        self.updent()

    def end_nonterminal(self, content):
        self.downdent()
        self.xml.write(' ' * self.indent + '</' + content + '>\n')

    def write_token(self):
        token = self.tokenizer.curr_token
        token_type = self.tokenizer.token_type
        if token in ['&', '<', '>']:
            token = token.replace('&', '&amp;')
            token = token.replace('<', '&lt;')
            token = token.replace('>', '&gt;')
        if token_type == 'INT_CONST':
            token_type = 'integerConstant'
        elif token_type == 'STRING_CONST':
            token_type = 'stringConstant'
        else:
            token_type = str.lower(token_type)
        self.xml.write(' ' * self.indent +
                       '<{}> {} </{}>\n'.format(token_type, token, token_type))
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

    """def close(self):
        self.downdent()
        self.xml.write('</tokens>')
        self.xml.close()"""

    def updent(self):
        self.indent += 2

    def downdent(self):
        self.indent -= 2
