from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from ir import IRGenerator

def compile_program(source_code):
    print("=" * 50)
    print("COMPILER PIPELINE")
    print("=" * 50)
    
   
    print("\n[PHASE 1: LEXICAL ANALYSIS]")
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    
    print("Tokens:")
    for token in tokens:
        if token.type != 'EOF':
            print(f"  {token}")
    
    
    print("\n[PHASE 2: SYNTAX ANALYSIS]")
    parser = Parser(tokens)
    ast = parser.parse()
    print("✓ AST generated successfully")
    
   
    print("\n[PHASE 3: SEMANTIC ANALYSIS]")
    semantic_analyzer = SemanticAnalyzer()
    is_valid = semantic_analyzer.analyze(ast)
    
    if not is_valid:
        print("\n✗ Compilation failed due to semantic errors")
        return None
    
    print("\n✓ Semantic analysis passed")
    print("\nSymbol Table:")
    for var, dtype in semantic_analyzer.get_symbol_table().items():
        print(f"  {var}: {dtype}")
    
 
    print("\n[PHASE 4: IR GENERATION]")
    ir_generator = IRGenerator(semantic_analyzer.get_symbol_table())
    instructions = ir_generator.generate(ast)
    ir_generator.print_instructions()
    
    print("\n" + "=" * 50)
    print("✓ COMPILATION SUCCESSFUL")
    print("=" * 50)
    
    return instructions


if __name__ == "__main__":
 
    test_program = """
int x;
float y = 5.2;
x = 10;
y = x + 3.1;
int z = x + 5;
float w = y * 2.0 + x;
"""
    
    print("Source Code:")
    print(test_program)
    print()
    
    compile_program(test_program)
    
    print("\n\n" + "=" * 50)
    print("TESTING WITH ERRORS")
    print("=" * 50)
    
   
    error_program = """
z = 3;
x = 3.5;
float x;
"""
    
    print("\nSource Code:")
    print(error_program)
    print()
    
    compile_program(error_program)