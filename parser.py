import ast
from lexer import Lexer

class Parser:
     def __init__(self):
         self.lexer = Lexer()

     def _parse_value_ast(self, value_node):
        if isinstance(value_node, ast.Constant):
           return str(value_node.value)
        elif isinstance(value_node, ast.Name):
           return value_node.id
        elif isinstance(value_node, ast.BinOp):
           left = self._parse_value_ast(value_node.left)
           right = self._parse_value_ast(value_node.right)
           op = ""
           if isinstance(value_node.op, ast.Add):
             op = "+"
           elif isinstance(value_node.op, ast.Sub):
             op = "-"
           elif isinstance(value_node.op, ast.Mult):
             op = "*"
           elif isinstance(value_node.op, ast.Div):
             op = "/"
           return f"{left} {op} {right}"
        elif isinstance(value_node, ast.Compare):
           left = self._parse_value_ast(value_node.left)
           right = self._parse_value_ast(value_node.comparators[0])
           op = ""
           if isinstance(value_node.ops[0], ast.Gt):
               op = ">"
           elif isinstance(value_node.ops[0], ast.Lt):
               op = "<"
           elif isinstance(value_node.ops[0], ast.Eq):
               op = "=="
           elif isinstance(value_node.ops[0], ast.NotEq):
               op = "!="
           return f"{left} {op} {right}"
        elif isinstance(value_node, ast.List):
           values = [self._parse_value_ast(item) for item in value_node.elts]
           return f"[{','.join(values)}]"
        elif isinstance(value_node, ast.Dict):
           keys = [self._parse_value_ast(key) for key in value_node.keys]
           values = [self._parse_value_ast(val) for val in value_node.values]
           items = []
           for i,key in enumerate(keys):
             items.append(f"{key}:{values[i]}")
           return f"{{{','.join(items)}}}"
        elif isinstance(value_node, ast.Tuple):
            values = [self._parse_value_ast(item) for item in value_node.elts]
            return f"({','.join(values)})"
        elif isinstance(value_node, ast.Call):
           fun_name = value_node.func.id
           args = [self._parse_value_ast(arg) for arg in value_node.args]
           return f"{fun_name}({', '.join(args)})"
        elif isinstance(value_node, ast.Attribute):
           return f"{self._parse_value_ast(value_node.value)}.{value_node.attr}"
        else:
           return str(value_node)

     def _translate_python_to_pylite(self, python_code):
        try:
          tree = ast.parse(python_code)
        except SyntaxError:
          return None
        pylite_code = ""
 
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
               params = [arg.arg for arg in node.args.args]
               pylite_code += f"fun {node.name}({','.join(params)}):\n"
               for statement in node.body:
                  if isinstance(statement, ast.Return):
                      if statement.value:
                         pylite_code += "  return " + self._parse_value_ast(statement.value) + "\n"
                  elif isinstance(statement, ast.Assign):
                      pylite_code += "  " + statement.targets[0].id + " = " + self._parse_value_ast(statement.value) + "\n"
                  elif isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call) and statement.value.func.id == "print":
                        
                      pylite_code += f" print {self._parse_value_ast(statement.value.args[0])} \n"
               pylite_code += f"endfun\n"
            elif isinstance(node, ast.ClassDef):
               pylite_code += f"class {node.name}:\n"
               for body in node.body:
                 if isinstance(body, ast.FunctionDef):
                     params = [arg.arg for arg in body.args.args]
                     pylite_code += f"  fun {body.name}({','.join(params)}):\n"
                     for statement in body.body:
                        if isinstance(statement, ast.Return):
                          if statement.value:
                            pylite_code += "    return " + self._parse_value_ast(statement.value) + "\n"
                        elif isinstance(statement, ast.Assign):
                            pylite_code += "   " + statement.targets[0].id + " = " + self._parse_value_ast(statement.value) + "\n"
                        elif isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call) and statement.value.func.id == "print":
                           
                           pylite_code += f"   print {self._parse_value_ast(statement.value.args[0])} \n"
                     pylite_code += f"  endfun\n"
                 elif isinstance(body, ast.Assign):
                   pylite_code += "   " + body.targets[0].id + " = " + self._parse_value_ast(body.value) + "\n"
               pylite_code += "endclass\n"
            elif isinstance(node, ast.Assign):
               pylite_code += f"{node.targets[0].id} = {self._parse_value_ast(node.value)}\n"
            elif isinstance(node, ast.If):
                pylite_code += f"if {self._parse_value_ast(node.test)}:\n"
                for statement in node.body:
                    if isinstance(statement, ast.Assign):
                      pylite_code += f" {statement.targets[0].id} = {self._parse_value_ast(statement.value)}\n"
                    elif isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call) and statement.value.func.id == "print":
                      pylite_code += f"    print {self._parse_value_ast(statement.value.args[0])} \n"
                pylite_code += "else:\n"
                for statement in node.orelse:
                    if isinstance(statement, ast.Assign):
                      pylite_code += f"  {statement.targets[0].id} = {self._parse_value_ast(statement.value)}\n"
                    elif isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call) and statement.value.func.id == "print":
                      pylite_code += f"    print {self._parse_value_ast(statement.value.args[0])} \n"
                pylite_code += "endif\n"
            elif isinstance(node, ast.For):
               pylite_code += f"for {node.target.id} in {self._parse_value_ast(node.iter)}:\n"
               for statement in node.body:
                  if isinstance(statement, ast.Assign):
                     pylite_code += f"    {statement.targets[0].id} = {self._parse_value_ast(statement.value)}\n"
                  elif isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call) and statement.value.func.id == "print":
                     pylite_code += f"    print {self._parse_value_ast(statement.value.args[0])} \n"
               pylite_code += "endfor\n"
            elif isinstance(node, ast.While):
                pylite_code += f"while {self._parse_value_ast(node.test)}:\n"
                for statement in node.body:
                  if isinstance(statement, ast.Assign):
                     pylite_code += f"    {statement.targets[0].id} = {self._parse_value_ast(statement.value)}\n"
                  elif isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call) and statement.value.func.id == "print":
                     pylite_code += f"    print {self._parse_value_ast(statement.value.args[0])} \n"
                pylite_code += "endwhile\n"
 
        return pylite_code
     
     def parse(self, code):
        tokens = self.lexer.tokenize(code)
        return self.build_ast(tokens)
     def build_ast(self, tokens):
         """
         Builds the abstract syntax tree (AST) based on the stream of tokens
         For now, this function just returns the token for interpretation
         """
         return tokens

     def translate_code(self, python_code):
         """
         Translates the python code into pylite code
         """
         return self._translate_python_to_pylite(python_code)
