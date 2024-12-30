# pylite/lexer.py

import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class PyLiteLexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.pos = 0
        self.tokens = []

    def tokenize(self):
        while self.pos < len(self.source_code):
            char = self.source_code[self.pos]

            if char.isspace():
                self.pos += 1
                continue
            elif char == '#':
                 while self.pos < len(self.source_code) and self.source_code[self.pos] != '\n':
                     self.pos+=1
                 self.pos+=1
                 continue
            elif char.isdigit() or (char == '-' and self.peek(1).isdigit()):
                self.tokens.append(self.tokenize_number())
            elif char.isalpha():
                 self.tokens.append(self.tokenize_identifier())
            elif char == '"':
                 self.tokens.append(self.tokenize_string())
            elif char in "+-*/%()=<>!":
                self.tokens.append(self.tokenize_operator())
            elif char == '\n':
                self.tokens.append(Token("NEWLINE", "\n"))
                self.pos +=1
            else:
                raise ValueError(f"Unexpected character '{char}' at position {self.pos}")

        self.tokens.append(Token("EOF", None))
        return self.tokens

    def peek(self, offset):
       if self.pos + offset < len(self.source_code):
         return self.source_code[self.pos+offset]
       return None

    def tokenize_number(self):
          start_pos = self.pos
          decimal_point = False
          while self.pos < len(self.source_code) and (self.source_code[self.pos].isdigit() or self.source_code[self.pos] == '.' or self.source_code[self.pos] == '-'):
              if self.source_code[self.pos] == '.':
                  if decimal_point:
                      raise ValueError(f"Invalid number at position {start_pos}")
                  decimal_point = True
              self.pos += 1

          value = self.source_code[start_pos:self.pos]
          if decimal_point:
            return Token("FLOAT", float(value))
          else:
             return Token("INT", int(value))


    def tokenize_identifier(self):
          start_pos = self.pos
          while self.pos < len(self.source_code) and (self.source_code[self.pos].isalnum() or self.source_code[self.pos] == '_'):
             self.pos += 1
          value = self.source_code[start_pos:self.pos]
          if value in ("if", "elif", "else", "while", "print", "and", "or", "not", "True", "False"):
              return Token("KEYWORD", value)
          else:
              return Token("IDENTIFIER", value)

    def tokenize_string(self):
        self.pos+=1
        start_pos = self.pos
        while self.pos < len(self.source_code) and self.source_code[self.pos] != '"':
            self.pos += 1
        if self.pos == len(self.source_code):
            raise ValueError(f"Unterminated String at position {start_pos}")
        value = self.source_code[start_pos:self.pos]
        self.pos+=1
        return Token("STRING", value)

    def tokenize_operator(self):
        char = self.source_code[self.pos]
        if char == '=':
            if self.peek(1) == '=':
                 self.pos+=2
                 return Token("OPERATOR", "==")
            else:
                 self.pos += 1
                 return Token("OPERATOR", "=")
        elif char == '!':
            if self.peek(1) == '=':
                 self.pos+=2
                 return Token("OPERATOR", "!=")
            else:
                 raise ValueError(f"Unexpected character '{char}' at position {self.pos}")
        elif char == '<':
             if self.peek(1) == '=':
                  self.pos+=2
                  return Token("OPERATOR", "<=")
             else:
                 self.pos+=1
                 return Token("OPERATOR", "<")
        elif char == '>':
             if self.peek(1) == '=':
                 self.pos+=2
                 return Token("OPERATOR", ">=")
             else:
                 self.pos+=1
                 return Token("OPERATOR", ">")
        else:
            self.pos +=1
            return Token("OPERATOR", char)
