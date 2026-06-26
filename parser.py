from lexer import Token

class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class Declaration(ASTNode):
    def __init__(self, dtype, identifier, init_expr=None):
        self.dtype = dtype
        self.identifier = identifier
        self.init_expr = init_expr

class Assignment(ASTNode):
    def __init__(self, identifier, expr):
        self.identifier = identifier
        self.expr = expr

class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

class Literal(ASTNode):
    def __init__(self, value, dtype):
        self.value = value
        self.dtype = dtype

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else None
    
    def advance(self):
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
    
    def parse(self):
        statements = []
        
        while self.current_token.type != 'EOF':
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        
        return Program(statements)
    
    def parse_statement(self):
        
        if self.current_token.type == 'KEYWORD' and self.current_token.value in ['int', 'float']:
            return self.parse_declaration()
        
        
        if self.current_token.type == 'IDENTIFIER':
            return self.parse_assignment()
        
        
        self.advance()
        return None
    
    def parse_declaration(self):
        dtype = self.current_token.value
        self.advance()
        
        if self.current_token.type != 'IDENTIFIER':
            print(f"Syntax Error: Expected identifier after type '{dtype}'")
            return None
        
        identifier = self.current_token.value
        self.advance()
        
        init_expr = None
        
       
        if self.current_token.type == 'ASSIGN':
            self.advance()
            init_expr = self.parse_expression()
        
       
        if self.current_token.type == 'SEMICOLON':
            self.advance()
        
        return Declaration(dtype, identifier, init_expr)
    
    def parse_assignment(self):
        identifier = self.current_token.value
        self.advance()
        
        if self.current_token.type != 'ASSIGN':
            print(f"Syntax Error: Expected '=' after identifier '{identifier}'")
            return None
        
        self.advance()
        expr = self.parse_expression()
        
       
        if self.current_token.type == 'SEMICOLON':
            self.advance()
        
        return Assignment(identifier, expr)
    
    def parse_expression(self):
        return self.parse_additive()
    
    def parse_additive(self):
        left = self.parse_multiplicative()
        
        while self.current_token.type in ['PLUS', 'MINUS']:
            op = self.current_token.value
            self.advance()
            right = self.parse_multiplicative()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_multiplicative(self):
        left = self.parse_primary()
        
        while self.current_token.type in ['MULTIPLY', 'DIVIDE']:
            op = self.current_token.value
            self.advance()
            right = self.parse_primary()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_primary(self):
       
        if self.current_token.type == 'INT_LITERAL':
            value = self.current_token.value
            self.advance()
            return Literal(value, 'int')
        
        if self.current_token.type == 'FLOAT_LITERAL':
            value = self.current_token.value
            self.advance()
            return Literal(value, 'float')
        
        
        if self.current_token.type == 'IDENTIFIER':
            name = self.current_token.value
            self.advance()
            return Identifier(name)
        
        
        if self.current_token.type == 'LPAREN':
            self.advance()
            expr = self.parse_expression()
            if self.current_token.type == 'RPAREN':
                self.advance()
            return expr
        
        print(f"Syntax Error: Unexpected token {self.current_token}")
        self.advance()
        return None