# pylite/parser.py

from lexer import Token, PyLiteLexer
class ASTNode:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children if children else []

    def __repr__(self):
         return f"ASTNode({self.type}, {self.value}, {self.children})"


class PyLiteParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        statements = []
        while self.peek().type != "EOF":
           statements.append(self.parse_statement())
        return statements


    def peek(self, offset=0):
        if self.pos + offset < len(self.tokens):
            return self.tokens[self.pos + offset]
        return Token("EOF", None)

    def consume(self):
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def match(self, type, value=None):
        if self.peek().type == type and (value is None or self.peek().value == value):
           return self.consume()
        return None

    def require(self, type, value=None):
         token = self.match(type, value)
         if not token:
             if value:
                raise Exception(f"Expected {type} with value {value}, got {self.peek()}")
             else:
                raise Exception(f"Expected {type}, got {self.peek()}")
         return token

    def parse_statement(self):
         if self.match("KEYWORD", "if"):
              return self.parse_if_statement()
         if self.match("KEYWORD", "while"):
              return self.parse_while_statement()
         if self.match("KEYWORD", "print"):
              return self.parse_print_statement()
         return self.parse_assignment()

    def parse_if_statement(self):
        self.require("OPERATOR", "(")
        condition = self.parse_expression()
        self.require("OPERATOR", ")")
        self.require("OPERATOR", ":")
        if_statements = []
        while self.peek().type != 'EOF' and self.peek(1).type != 'KEYWORD' and self.peek(0).type != "NEWLINE":
            if_statements.append(self.parse_statement())

        elif_statements = []
        else_statements = []

        if self.match("KEYWORD", "elif"):
            while True:
                 self.require("OPERATOR", "(")
                 condition = self.parse_expression()
                 self.require("OPERATOR", ")")
                 self.require("OPERATOR", ":")
                 elif_block = []
                 while self.peek().type != 'EOF' and self.peek(1).type != 'KEYWORD' and self.peek(0).type != "NEWLINE":
                      elif_block.append(self.parse_statement())
                 elif_statements.append({"condition": condition, "statements": elif_block})
                 if not self.match("KEYWORD", "elif"):
                     break

        if self.match("KEYWORD", "else"):
            self.require("OPERATOR", ":")
            while self.peek().type != 'EOF' and self.peek(0).type != "NEWLINE":
                 else_statements.append(self.parse_statement())

        return ASTNode("IF_STATEMENT", children = [condition, *if_statements, {"elif": elif_statements, "else": else_statements}])


    def parse_while_statement(self):
        self.require("OPERATOR", "(")
        condition = self.parse_expression()
        self.require("OPERATOR", ")")
        self.require("OPERATOR", ":")
        statements = []
        while self.peek().type != 'EOF' and self.peek(0).type != "NEWLINE":
           statements.append(self.parse_statement())

        return ASTNode("WHILE_STATEMENT", children = [condition, *statements])

    def parse_print_statement(self):
         self.require("OPERATOR", "(")
         expression = self.parse_expression()
         self.require("OPERATOR", ")")
         return ASTNode("PRINT_STATEMENT", children=[expression])

    def parse_assignment(self):
         if self.peek(1).value == "=":
              identifier = self.require("IDENTIFIER").value
              self.require("OPERATOR", "=")
              expression = self.parse_expression()
              return ASTNode("ASSIGNMENT", identifier, children=[expression])
         return self.parse_expression()

    def parse_expression(self):
         return self.parse_or_expression()

    def parse_or_expression(self):
        left = self.parse_and_expression()
        while self.match("KEYWORD", "or"):
             right = self.parse_and_expression()
             left = ASTNode("BINARY_OP", "or", children=[left, right])
        return left

    def parse_and_expression(self):
        left = self.parse_not_expression()
        while self.match("KEYWORD", "and"):
            right = self.parse_not_expression()
            left = ASTNode("BINARY_OP", "and", children = [left, right])
        return left

    def parse_not_expression(self):
        if self.match("KEYWORD", "not"):
           expression = self.parse_not_expression()
           return ASTNode("UNARY_OP", "not", children=[expression])
        return self.parse_comparison()

    def parse_comparison(self):
         left = self.parse_addition()
         while self.peek().type == "OPERATOR" and self.peek().value in ["==", "!=", "<", ">", "<=", ">="]:
              op = self.consume().value
              right = self.parse_addition()
              left = ASTNode("BINARY_OP", op, children=[left,right])
         return left

    def parse_addition(self):
         left = self.parse_multiplication()
         while self.peek().type == "OPERATOR" and self.peek().value in ["+", "-"]:
              op = self.consume().value
              right = self.parse_multiplication()
              left = ASTNode("BINARY_OP", op, children=[left, right])
         return left


    def parse_multiplication(self):
        left = self.parse_unary()
        while self.peek().type == "OPERATOR" and self.peek().value in ["*", "/", "//", "%", "**"]:
            op = self.consume().value
            right = self.parse_unary()
            left = ASTNode("BINARY_OP", op, children=[left, right])
        return left

    def parse_unary(self):
        if self.peek().type == 'OPERATOR' and self.peek().value == '-':
            self.consume()
            expression = self.parse_unary()
            return ASTNode("UNARY_OP", "-", children=[expression])
        return self.parse_primary()

    def parse_primary(self):
         if self.peek().type == "INT":
              return ASTNode("INT", self.consume().value)
         if self.peek().type == "FLOAT":
              return ASTNode("FLOAT", self.consume().value)
         if self.peek().type == "STRING":
              return ASTNode("STRING", self.consume().value)
         if self.peek().type == "KEYWORD" and self.peek().value == "True":
             self.consume()
             return ASTNode("BOOLEAN", True)
         if self.peek().type == "KEYWORD" and self.peek().value == "False":
             self.consume()
             return ASTNode("BOOLEAN", False)
         if self.peek().type == "IDENTIFIER":
              return ASTNode("IDENTIFIER", self.consume().value)
         if self.match("OPERATOR", "("):
            expression = self.parse_expression()
            self.require("OPERATOR", ")")
            return expression
         raise Exception(f"Expected an expression, got {self.peek()}")
