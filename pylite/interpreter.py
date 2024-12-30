# pylite/interpreter.py
from lexer import Token, PyLiteLexer
from parser import ASTNode, PyLiteParser

class PyLiteInterpreter:
    def __init__(self):
        self.variables = {}

    def interpret(self, ast):
        for node in ast:
            self.evaluate(node)

    def evaluate(self, node):
        if node.type == "INT" or node.type == "FLOAT" or node.type == "STRING" or node.type == "BOOLEAN":
              return node.value
        elif node.type == "IDENTIFIER":
             if node.value in self.variables:
                 return self.variables[node.value]
             else:
                  raise Exception(f"Undefined variable {node.value}")

        elif node.type == "ASSIGNMENT":
            value = self.evaluate(node.children[0])
            self.variables[node.value] = value
            return value
        elif node.type == "UNARY_OP":
              if node.value == "-":
                  value = self.evaluate(node.children[0])
                  if isinstance(value, (int, float)):
                      return -value
                  else:
                     raise Exception("Invalid operation for unary '-'")
              if node.value == "not":
                    value = self.evaluate(node.children[0])
                    if isinstance(value, bool):
                       return not value
                    else:
                        raise Exception("Invalid operation for unary 'not'")
        elif node.type == "BINARY_OP":
            left = self.evaluate(node.children[0])
            right = self.evaluate(node.children[1])

            if node.value == "+": return left + right
            if node.value == "-": return left - right
            if node.value == "*": return left * right
            if node.value == "/":
                if right == 0:
                   raise Exception("Division by zero")
                return left / right
            if node.value == "//":
                if right == 0:
                  raise Exception("Division by zero")
                return left // right
            if node.value == "%":
                if right == 0:
                  raise Exception("Modulo by zero")
                return left % right
            if node.value == "**": return left ** right
            if node.value == "==": return left == right
            if node.value == "!=": return left != right
            if node.value == "<": return left < right
            if node.value == ">": return left > right
            if node.value == "<=": return left <= right
            if node.value == ">=": return left >= right
            if node.value == "and": return left and right
            if node.value == "or": return left or right

        elif node.type == "PRINT_STATEMENT":
            value = self.evaluate(node.children[0])
            print(value)
        elif node.type == "IF_STATEMENT":
             condition = self.evaluate(node.children[0])
             if condition:
                 for statement in node.children[1:-1]:
                    self.evaluate(statement)
             else:
                 elif_statements = node.children[-1]['elif']
                 else_statements = node.children[-1]['else']
                 elif_executed = False
                 for elif_block in elif_statements:
                     elif_condition = self.evaluate(elif_block['condition'])
                     if elif_condition:
                          for statement in elif_block['statements']:
                            self.evaluate(statement)
                          elif_executed = True
                          break

                 if not elif_executed:
                   for statement in else_statements:
                       self.evaluate(statement)
        elif node.type == "WHILE_STATEMENT":
            while self.evaluate(node.children[0]):
                 for statement in node.children[1:]:
                      self.evaluate(statement)

        else:
             raise Exception(f"Unknown node type: {node.type}")
