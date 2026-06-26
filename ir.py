from parser import *

class IRInstruction:
    pass

class ThreeAddressCode(IRInstruction):
    def __init__(self, result, arg1, op, arg2):
        self.result = result
        self.arg1 = arg1
        self.op = op
        self.arg2 = arg2
    
    def __str__(self):
        if self.op:
            return f"{self.result} = {self.arg1} {self.op} {self.arg2}"
        else:
            return f"{self.result} = {self.arg1}"

class IRGenerator:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.instructions = []
        self.temp_count = 0
    
    def new_temp(self):
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp
    
    def generate(self, ast):
        if isinstance(ast, Program):
            for stmt in ast.statements:
                self.generate_statement(stmt)
        return self.instructions
    
    def generate_statement(self, stmt):
        if isinstance(stmt, Declaration):
            self.generate_declaration(stmt)
        elif isinstance(stmt, Assignment):
            self.generate_assignment(stmt)
    
    def generate_declaration(self, decl):
       
        if decl.init_expr:
            result = self.generate_expression(decl.init_expr)
            
            instr = ThreeAddressCode(decl.identifier, result, None, None)
            self.instructions.append(instr)
    
    def generate_assignment(self, assign):
       
        result = self.generate_expression(assign.expr)
        
        
        instr = ThreeAddressCode(assign.identifier, result, None, None)
        self.instructions.append(instr)
    
    def generate_expression(self, expr):
        if isinstance(expr, Literal):
            return str(expr.value)
        
        if isinstance(expr, Identifier):
            return expr.name
        
        if isinstance(expr, BinaryOp):
           
            left_result = self.generate_expression(expr.left)
            right_result = self.generate_expression(expr.right)
            
            
            temp = self.new_temp()
            
            #
            instr = ThreeAddressCode(temp, left_result, expr.op, right_result)
            self.instructions.append(instr)
            
            return temp
        
        return None
    
    def print_instructions(self):
        print("\n=== Generated IR (Three-Address Code) ===")
        for i, instr in enumerate(self.instructions):
            print(f"{i}: {instr}")
    
    def get_instructions(self):
        return self.instructions