# pylite/interpreter.py
from lexer import Token, PyLiteLexer
from parser import ASTNode, PyLiteParser

class PyLiteInterpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}


    def interpret(self, ast):
         for node in ast:
           self.evaluate(node)

    def evaluate(self, node, function_scope = None):
        if function_scope is None:
            function_scope = {}
        if node.type == "INT" or node.type == "FLOAT" or node.type == "STRING" or node.type == "BOOLEAN":
              return node.value
        elif node.type == "IDENTIFIER":
             if node.value in function_scope:
                return function_scope[node.value]
             if node.value in self.variables:
                 return self.variables[node.value]
             else:
                  raise Exception(f"Undefined variable {node.value}")

        elif node.type == "ASSIGNMENT":
            value = self.evaluate(node.children[0], function_scope)
            if function_scope is not None:
                function_scope[node.value] = value
            else:
                self.variables[node.value] = value
            return value
        elif node.type == "UNARY_OP":
              if node.value == "-":
                  value = self.evaluate(node.children[0], function_scope)
                  if isinstance(value, (int, float)):
                      return -value
                  else:
                     raise Exception("Invalid operation for unary '-'")
              if node.value == "not":
                    value = self.evaluate(node.children[0], function_scope)
                    if isinstance(value, bool):
                       return not value
                    else:
                        raise Exception("Invalid operation for unary 'not'")
        elif node.type == "BINARY_OP":
            left = self.evaluate(node.children[0], function_scope)
            right = self.evaluate(node.children[1], function_scope)

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
        elif node.type == "CALL_EXPRESSION":
              name = self.evaluate(node.children[0], function_scope)
              args = []
              for arg in node.children[1:]:
                  args.append(self.evaluate(arg, function_scope))
              if name == "len":
                   if len(args) != 1 or not isinstance(args[0], str):
                        raise Exception(f"Invalid args for len function: {args}")
                   return len(args[0])
              elif name == "int":
                  if len(args) != 1:
                      raise Exception("Invalid number of arguments for int()")
                  try:
                    return int(args[0])
                  except:
                      raise Exception("Invalid argument for int()")
              elif name == "float":
                  if len(args) != 1:
                    raise Exception("Invalid number of arguments for float()")
                  try:
                    return float(args[0])
                  except:
                      raise Exception("Invalid argument for float()")
              elif name == "str":
                   if len(args) != 1:
                        raise Exception("Invalid number of arguments for str()")
                   return str(args[0])
              elif name == "input":
                  if len(args) > 1:
                     raise Exception("Invalid number of arguments for input()")
                  prompt = args[0] if args else ""
                  return input(prompt)
              elif name in self.functions:
                    func_node = self.functions[name]
                    params = func_node.children[0]
                    func_scope = {}
                    if len(params) != len(args):
                        raise Exception(f"Expected {len(params)} arguments for function {name} but got {len(args)}")
                    for i, param in enumerate(params):
                        func_scope[param] = args[i]
                    for statement in func_node.children[1:]:
                       result = self.evaluate(statement, func_scope)
                       if statement.type == "RETURN_STATEMENT":
                          return result
                    return None # No return value
              else:
                 raise Exception(f"Undefined function: {name}")

        elif node.type == "PRINT_STATEMENT":
            values_to_print = []
            for child in node.children:
               values_to_print.append(str(self.evaluate(child, function_scope)))
            print(" ".join(values_to_print))
        elif node.type == "IF_STATEMENT":
             condition = self.evaluate(node.children[0], function_scope)
             if condition:
                 for statement in node.children[1:-1]:
                    self.evaluate(statement, function_scope)
             else:
                 elif_statements = node.children[-1]['elif']
                 else_statements = node.children[-1]['else']
                 elif_executed = False
                 for elif_block in elif_statements:
                     elif_condition = self.evaluate(elif_block['condition'], function_scope)
                     if elif_condition:
                          for statement in elif_block['statements']:
                            self.evaluate(statement, function_scope)
                          elif_executed = True
                          break

                 if not elif_executed:
                   for statement in else_statements:
                       self.evaluate(statement, function_scope)
        elif node.type == "WHILE_STATEMENT":
            while self.evaluate(node.children[0], function_scope):
                 for statement in node.children[1:]:
                      self.evaluate(statement, function_scope)
        elif node.type == "FUNCTION_DEFINITION":
              self.functions[node.value] = node
        elif node.type == "RETURN_STATEMENT":
              if node.children[0]:
                return self.evaluate(node.children[0], function_scope)
              return None
        else:
             raise Exception(f"Unknown node type: {node.type}")
