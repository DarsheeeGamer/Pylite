# pylite/main.py
import sys
from lexer import PyLiteLexer
from parser import PyLiteParser
from interpreter import PyLiteInterpreter

def run_pylite_code(code):
    lexer = PyLiteLexer(code)
    tokens = lexer.tokenize()
    parser = PyLiteParser(tokens)
    ast = parser.parse()
    interpreter = PyLiteInterpreter()
    interpreter.interpret(ast)


def main():
    if len(sys.argv) > 1:
         file_path = sys.argv[1]
         if not file_path.endswith(".pylite"):
             print("Error: only .pylite files are allowed")
             sys.exit(1)
         try:
             with open(file_path, 'r') as f:
                code = f.read()
             run_pylite_code(code)
         except FileNotFoundError:
             print(f"Error: File not found '{file_path}'")
         except Exception as e:
              print(f"Error: {e}")
         sys.exit(0)
    else:
      interpreter = PyLiteInterpreter()
      while True:
            try:
                code = input(">>> ")
                if code == "exit()":
                   break
                lexer = PyLiteLexer(code)
                tokens = lexer.tokenize()
                parser = PyLiteParser(tokens)
                ast = parser.parse()
                interpreter.interpret(ast)
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    main()
