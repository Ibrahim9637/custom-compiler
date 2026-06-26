import re

RESERVED_WORDS = {"if", "else", "while", "return", "for", "int", "float"}

class Token:
    def __init__(self, type, value, line=0):
        self.type = type
        self.value = value
        self.line = line
    
    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None
        self.line = 1
    
    def advance(self):
        if self.current_char == '\n':
            self.line += 1
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
    
    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()
    
    def read_number(self):
        num_str = ''
        has_dot = False
        
        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if has_dot:
                    break
                has_dot = True
            num_str += self.current_char
            self.advance()
        
        if has_dot:
            return Token('FLOAT_LITERAL', float(num_str), self.line)
        else:
            return Token('INT_LITERAL', int(num_str), self.line)
    
    def read_identifier(self):
        id_str = ''
        
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            id_str += self.current_char
            self.advance()
        
        
        if id_str in RESERVED_WORDS:
            return Token('KEYWORD', id_str, self.line)
        
        
        if len(id_str) > 10:
            return Token('ERROR', id_str, self.line)
        
        return Token('IDENTIFIER', id_str, self.line)
    
    def get_next_token(self):
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char.isdigit():
                return self.read_number()
            
            if self.current_char.isalpha() or self.current_char == '_':
                return self.read_identifier()
            
            if self.current_char == '=':
                self.advance()
                return Token('ASSIGN', '=', self.line)
            
            if self.current_char == '+':
                self.advance()
                return Token('PLUS', '+', self.line)
            
            if self.current_char == '-':
                self.advance()
                return Token('MINUS', '-', self.line)
            
            if self.current_char == '*':
                self.advance()
                return Token('MULTIPLY', '*', self.line)
            
            if self.current_char == '/':
                self.advance()
                return Token('DIVIDE', '/', self.line)
            
            if self.current_char == ';':
                self.advance()
                return Token('SEMICOLON', ';', self.line)
            
            if self.current_char == '(':
                self.advance()
                return Token('LPAREN', '(', self.line)
            
            if self.current_char == ')':
                self.advance()
                return Token('RPAREN', ')', self.line)
            
            
            char = self.current_char
            self.advance()
            return Token('ERROR', char, self.line)
        
        return Token('EOF', None, self.line)
    
    def tokenize(self):
        tokens = []
        token = self.get_next_token()
        
        while token.type != 'EOF':
            tokens.append(token)
            token = self.get_next_token()
        
        tokens.append(token)  
        return tokens