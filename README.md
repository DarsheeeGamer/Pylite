# PyLite: A Simplified Python-like Language Interpreter

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**GitHub Repository:** [https://github.com/DarsheeeGamer/Pylite/](https://github.com/DarsheeeGamer/Pylite/)

## Introduction

PyLite is a simplified programming language inspired by Python. It is implemented using Python itself and is designed to be a minimal yet functional language interpreter. PyLite aims to demonstrate the core concepts of lexing, parsing, and interpretation without the complexities of a full-fledged language.

This project provides a command-line interface (CLI) that can execute .pylite files or interpret code interactively.

## Features

*   **Basic Data Types:** Integers, Floats, Strings, Booleans
*   **Dynamic Typing:** Like Python, variables don't need explicit type declarations.
*   **Arithmetic Operators:** `+`, `-`, `*`, `/`, `//`, `%`, `**`
*   **Comparison Operators:** `==`, `!=`, `>`, `<`, `>=`, `<=`
*   **Logical Operators:** `and`, `or`, `not`
*   **Conditional Statements:** `if`, `elif`, `else`
*   **Looping:** `while`
*   **Basic Input/Output:** `print()` for output
*   **Comments:** `#` for single-line comments
*   **File Execution:** Can run `.pylite` files from the command line
*   **Interactive Mode:** REPL (Read-Eval-Print Loop) for interactive code execution

## Usage

### Running from CLI

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/DarsheeeGamer/Pylite.git
    cd Pylite
    ```

2.  **Execute a .pylite file:**

    ```bash
    python pylite/main.py my_script.pylite
    ```
    or if main.py is made executable

    ```bash
    ./pylite/main.py my_script.pylite
    ```
    (Replace `my_script.pylite` with the path to your PyLite script file.)
    - Note: Only .pylite files will be executed

3. **Interactive Mode**
    ```bash
    python pylite/main.py
    ```
    or if main.py is made executable

    ```bash
    ./pylite/main.py
    ```

    This will launch a command-line interpreter where you can enter and run PyLite code line by line. To exit the interpreter type `exit()`.
### Example Pylite code `example.pylite`
```
x = 10
y = 20
print(x + y)
z = "Hello, Pylite!"
print(z)
if (x < 15):
  print("x is less than 15")
elif (x > 15):
  print("x is greater than 15")
else:
  print("x is equal to 15")
count = 0
while (count < 3):
  print(count)
  count = count + 1
b = True
if (not b):
  print("b is not True")
else:
  print ("b is True")
```
## Project Structure

*   `lexer.py`: Contains the PyLiteLexer class responsible for tokenizing the source code.
*   `parser.py`: Contains the PyLiteParser class that generates the Abstract Syntax Tree (AST) from tokens.
*   `interpreter.py`: Contains the PyLiteInterpreter class, responsible for executing the AST and managing program state.
*   `main.py`: Entry point of the interpreter. Handles command line argument processing and the REPL loop.

### Possible Future Enhancements

*   Add support for functions.
*   Implement proper scope management for variables.
*   Include data structures like lists or dictionaries.
*   Introduce more operators.
*   Improve error reporting and handling.
*   Allow for Multi-line comments.
