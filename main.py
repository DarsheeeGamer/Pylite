
import sys
from interpreter import Interpreter
from parser import Parser

def main():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        try:
            with open(file_path, "r") as f:
                pylite_code = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {file_path}")
            return
    else:
        print("Enter PyLite code (type 'exit' to quit):")
        pylite_code = ""
        while True:
            line = input("> ")
            if line.lower() == "exit":
                break
            pylite_code += line + "\n"

    parser = Parser()
    interpreter = Interpreter()
    interpreter.parser = parser  # Give parser to interpreter so it can convert python to pylite
    try:
        interpreter.interpret(pylite_code) #Pass code directly for execution
    except Exception as e:
      print(f"Error: {e}")
if __name__ == "__main__":
    main()
