from parser import *

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.errors = []
    
    def analyze(self, ast):
        if isinstance(ast, Program):
            for stmt in ast.statements:
                self.analyze_statement(stmt)
        return len(self.errors) == 0
    
    def analyze_statement(self, stmt):
        if isinstance(stmt, Declaration):
            self.analyze_declaration(stmt)
        elif isinstance(stmt, Assignment):
            self.analyze_assignment(stmt)
    
    def analyze_declaration(self, decl):
        
        if decl.identifier in self.symbol_table:
            error = f"Semantic Error: Redeclaration of variable '{decl.identifier}'"
            self.errors.append(error)
            print(error)
            return
        
        
        self.symbol_table[decl.identifier] = decl.dtype
        print(f"Declaration: {decl.identifier} ({decl.dtype})")
        
       
        if decl.init_expr:
            expr_type = self.get_expression_type(decl.init_expr)
            if expr_type:
               
                if decl.dtype == 'int' and expr_type == 'float':
                    error = f"Semantic Error: Type mismatch: cannot assign float to int variable '{decl.identifier}'"
                    self.errors.append(error)
                    print(error)
    
    def analyze_assignment(self, assign):
        
        if assign.identifier not in self.symbol_table:
            error = f"Semantic Error: Undeclared variable '{assign.identifier}'"
            self.errors.append(error)
            print(error)
            return
        
        
        expr_type = self.get_expression_type(assign.expr)
        if not expr_type:
            return
        
        
        var_type = self.symbol_table[assign.identifier]
        if var_type == 'int' and expr_type == 'float':
            error = f"Semantic Error: Type mismatch: cannot assign float to int variable '{assign.identifier}'"
            self.errors.append(error)
            print(error)
            return
        
        print(f"Assignment: {assign.identifier} = <expression>")
    
    def get_expression_type(self, expr):
        if isinstance(expr, Literal):
            return expr.dtype
        
        if isinstance(expr, Identifier):
            if expr.name in self.symbol_table:
                return self.symbol_table[expr.name]
            else:
                error = f"Semantic Error: Undeclared variable '{expr.name}'"
                self.errors.append(error)
                print(error)
                return None
        
        if isinstance(expr, BinaryOp):
            left_type = self.get_expression_type(expr.left)
            right_type = self.get_expression_type(expr.right)
            
            if not left_type or not right_type:
                return None
            
           
            if left_type == 'float' or right_type == 'float':
                return 'float'
            else:
                return 'int'
        
        return None
    
    def get_symbol_table(self):
        return self.symbol_table