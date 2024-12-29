import re

class Lexer:
    def __init__(self):
        pass

    def tokenize(self, code):
        """
        Splits the code into tokens, each representing a distinct lexical element.
        Tokens: keywords, identifiers, numbers, strings, operators and special characters
        """
        tokens = []
        code = code.strip() #Remove extra spaces
        while code:
          match = re.match(r"^(\s+)",code)
          if match:
            code = code[len(match.group(0)):]
            continue

          match = re.match(r"^(\"([^\"]*)\")",code) #Match String
          if match:
             tokens.append(("STRING", match.group(0)))
             code = code[len(match.group(0)):]
             continue

          match = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*)", code) # Match Keywords and identifiers
          if match:
             tokens.append(("IDENTIFIER", match.group(0)))
             code = code[len(match.group(0)):]
             continue
          match = re.match(r"^(\d+(\.\d+)?)", code) #Match Numbers
          if match:
            tokens.append(("NUMBER",match.group(0)))
            code = code[len(match.group(0)):]
            continue
          match = re.match(r"^(\(|\)|\[|\]|\{|\}|:|=|\+|-|\*|/|>|<|==|!=|,|\.)",code) #Match special chars
          if match:
            tokens.append(("SPECIAL", match.group(0)))
            code = code[len(match.group(0)):]
            continue
          raise SyntaxError(f"Invalid syntax: '{code}'")
        return tokens
