# Custom Compiler / Interpreter in Python

A custom compiler/interpreter built from scratch using Python. This project demonstrates the core implementation phases of a computer science compiler pipeline, parsing and executing source logic.

## 🚀 Compiler Pipeline Architecture

The project is structured around the standard phases of compiler design:
* **Lexical Analysis (`lexer.py`)**: Tokenizes the input stream into a sequence of meaningful tokens.
* **Syntax Analysis (`parser.py`)**: Parses the token stream against the grammar rules to verify correctness.
* **Semantic Analysis (`semantic.py`)**: Validates type checking, scope validation, and logical correctness.
* **Intermediate Representation (`ir.py`)**: Generates structured low-level intermediate code.
* **Execution & Drive (`main.py`)**: The primary entry point coordinating the whole compilation flow.

## 📊 Inputs & Outputs Examples

Below are the execution tests showing the logic input syntax processing and the corresponding terminal outputs:

### Test Case 1
![Input Output 1](input%20%26%20output%20%281%29.jpg)

### Test Case 2
![Input Output 2](input%20%26%20output%20%282%29.jpg)

### Test Case 3
![Input Output 3](input%20%26%20output%20%283%29.jpg)

## 🛠️ How to Run
To run the compiler execution driver on your system, execute:
```bash
python main.py
