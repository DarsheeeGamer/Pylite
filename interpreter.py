import re
import sys
import inspect

class Interpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.classes = {}
        self.modules = {}
        self.imported_python = {}

    def _parse_value(self, value):
         if value.isdigit():
             return int(value)
         try:
             return float(value)
         except ValueError:
             if value.startswith('"') and value.endswith('"'):
                 return value[1:-1]
             elif value.startswith('[') and value.endswith(']'):
                 list_str = value[1:-1]
                 if not list_str:
                   return []
                 return [self._parse_value(element.strip()) for element in list_str.split(",")]
             elif value.startswith('{') and value.endswith('}'):
                 dict_str = value[1:-1]
                 if not dict_str:
                     return {}
                 items = dict_str.split(",")
                 dict_items = {}
                 for item in items:
                     key, val = item.split(":")
                     dict_items[self._parse_value(key.strip())] = self._parse_value(val.strip())
                 return dict_items
             elif value.startswith('(') and value.endswith(')'):
                 tuple_str = value[1:-1]
                 if not tuple_str:
                     return ()
                 return tuple(self._parse_value(element.strip()) for element in tuple_str.split(","))
             elif value in self.variables:
                return self.variables[value]
             else:
                 return value  # Assume string or variable name

    def execute_line(self, line):
         line = line.strip()
         if not line or line.startswith("#"):
             return  # Skip empty lines and comments
 
         parts = re.split(r'\s+', line)
         if parts[0] == "print":
             if len(parts) > 1:
                 print_value = self._parse_value(parts[1])
                 print(print_value)
         elif parts[1] == "=":
             var_name = parts[0]
             value = parts[2]
             self.variables[var_name] = self._parse_value(value)
         elif parts[0] == "fun":  # Function definition
             fun_name = parts[1].split("(")[0]
             params = re.findall(r'\(.*?\)', line)[0][1:-1].split(',') #Get params between parenthesis
             params = [param.strip() for param in params if param.strip()] #Remove spaces
             fun_body = []
             
             i = parts.index("fun")
             current_line = line
             while i < len(parts):
               fun_body.append(current_line.strip())
               current_line = input()
               if current_line.strip() == "endfun":
                   break
               i = -1 #Make the loop continue even when no fun keyword
             
             self.functions[fun_name] = (params, fun_body)
         elif parts[0] == "class":
            class_name = parts[1]
            class_body = []
            current_line = input()
            while not current_line.strip() == "endclass":
                 class_body.append(current_line)
                 current_line = input()
            self.classes[class_name] = class_body
         elif parts[0] in self.functions:  # Function call
            self.call_function(parts[0], parts[1:])
         elif parts[0] in self.classes:
             self.create_instance(parts[0], parts[1:])
         elif parts[0] == "if":
             self.handle_if_statement(line)
         elif parts[0] == "for":
             self.handle_for_loop(line)
         elif parts[0] == "while":
             self.handle_while_loop(line)
         elif parts[0] == "try":
             self.handle_try_except(line)
         elif parts[0] == "import":
             self.handle_import(line)
         elif "." in parts[0]:
            object_name, method = parts[0].split(".")
            args = parts[1:]
            if object_name in self.variables and object_name.startswith("class"):
               instance_name = self.variables[object_name]
               if method in self.variables[instance_name]:
                   method_params, method_body = self.variables[instance_name][method]
                   self.call_function(method, args, local_vars=self.variables[instance_name])
               elif method in self.imported_python:
                    if isinstance(self.imported_python[method], dict):
                       for name, value in self.imported_python[method].items():
                         if name == object_name:
                           #if args != None:
                               #result = getattr(value, method)(*args)
                           #else:
                           result = getattr(value, method)
                           
                           if callable(result):
                             result = result(*args)
                           
                           return result
                            
                         
                    elif hasattr(self.imported_python[method], method):
                        result = getattr(self.imported_python[method], method)
                        if callable(result):
                          result = result(*args)
                        return result
            elif object_name in self.imported_python:
                if hasattr(self.imported_python[object_name], method):
                   result = getattr(self.imported_python[object_name], method)
                   if callable(result):
                     result = result(*args)
                   return result
    
    def create_instance(self, class_name, args):
         if class_name not in self.classes:
           print(f"Error: Class '{class_name}' not found")
           return
         
         class_body = self.classes[class_name]
         instance_var = self.variables.get("last_instance", 0) + 1
         self.variables["last_instance"] = instance_var
         instance_name = class_name + str(instance_var) # Create a unique instance name for each object
         self.variables[instance_name] = {}
         self.variables[f"class{instance_var}"] = instance_name
         
         for line in class_body:
           parts = re.split(r'\s+', line)
           if len(parts) > 1:
             if parts[0] == "fun":
               fun_name = parts[1].split("(")[0]
               params = re.findall(r'\(.*?\)', line)[0][1:-1].split(',') #Get params between parenthesis
               params = [param.strip() for param in params if param.strip()] #Remove spaces
               fun_body = []
               i = parts.index("fun")
               current_line = line
               while i < len(parts):
                   fun_body.append(current_line.strip())
                   current_line = input()
                   if current_line.strip() == "endfun":
                      break
                   i = -1 #Make the loop continue even when no fun keyword
               self.variables[instance_name][fun_name] = (params, fun_body)
             elif parts[1] == "=": #Variable assignement
               self.variables[instance_name][parts[0]] = self._parse_value(parts[2])

    def handle_import(self, line):
        parts = re.split(r'\s+', line)
        module_name = parts[1]
        try:
         if module_name.endswith(".py"):
           file_path = module_name
           with open(file_path, "r") as f:
              python_code = f.read()
              translated_code = self.parser.translate_code(python_code)
              if translated_code:
                 self.run(translated_code)
              else:
                 module_namespace = {}
                 exec(python_code, module_namespace)
                 self.imported_python[module_name] = module_namespace
                 for name, value in module_namespace.items():
                     if inspect.isfunction(value) or inspect.isclass(value):
                        self.imported_python[name] = value
                               
         else:
             module = __import__(module_name)
             self.imported_python[module_name] = module
        except ImportError:
             print(f"Error: Could not import module '{module_name}'")
 
    def call_function(self, fun_name, args, local_vars = None):
         if fun_name not in self.functions and fun_name not in self.imported_python:
             print(f"Error: Function '{fun_name}' not defined")
             return
         
         if fun_name in self.functions:
            params, body = self.functions[fun_name]
            if len(args) != len(params):
                 print("Error: Invalid args number")
                 return
            
            local_scope = {}
            if local_vars != None:
               local_scope = local_vars.copy()
            for param, arg in zip(params, args):
                 local_scope[param] = self._parse_value(arg)
 
            for line in body:
               parts = re.split(r'\s+', line)
               if parts[0] == "return":
                 return_value = self._parse_value(parts[1]) if len(parts) > 1 else None
                 return return_value
               else:
                  self.execute_line(line)
         elif fun_name in self.imported_python and callable(self.imported_python[fun_name]):
               return self.imported_python[fun_name](*[self._parse_value(arg) for arg in args])
 
    def handle_if_statement(self, line):
       condition_start = line.find("if ") + 3
       condition_end = line.find(":")
       condition = line[condition_start:condition_end].strip()
 
       if self.evaluate_condition(condition):
             block = []
             current_line = input()
             while not current_line.strip() == "endif":
               block.append(current_line)
               current_line = input()
 
             for line in block:
               self.execute_line(line)
       else:
             else_found = False
             block = []
             current_line = input()
 
             while not (current_line.strip() == "endif" or current_line.strip() =="else"):
                 block.append(current_line)
                 current_line = input()
             if current_line.strip() == "else":
                else_found = True
             
             if else_found:
               block = []
               current_line = input()
               while not current_line.strip() == "endif":
                   block.append(current_line)
                   current_line = input()
               for line in block:
                   self.execute_line(line)
 
    def handle_for_loop(self, line):
       parts = re.split(r'\s+', line)
       var_name = parts[1]
       
       if parts[3].startswith("[") and parts[3].endswith("]"):
          list_values = [self._parse_value(v) for v in parts[3][1:-1].split(",")]
       elif parts[3].lower() == "range":
         start, end = parts[4][1:-1].split(",")
         start = self._parse_value(start)
         end = self._parse_value(end)
         list_values = list(range(start,end))
       else:
         print("Invalid for loop expression")
         return
 
       block = []
       current_line = input()
       while not current_line.strip() == "endfor":
          block.append(current_line)
          current_line = input()
 
       for value in list_values:
         self.variables[var_name] = value
         for line in block:
             self.execute_line(line)
     
    def handle_while_loop(self, line):
        condition_start = line.find("while ") + 6
        condition_end = line.find(":")
        condition = line[condition_start:condition_end].strip()
 
        block = []
        current_line = input()
        while not current_line.strip() == "endwhile":
            block.append(current_line)
            current_line = input()
 
        while self.evaluate_condition(condition):
           for line in block:
              self.execute_line(line)
 
    def handle_try_except(self, line):
         try_block = []
         current_line = input()
         while not (current_line.strip() == "except" or current_line.strip() == "endtry"):
           try_block.append(current_line)
           current_line = input()
         try:
            for line in try_block:
             self.execute_line(line)
         except Exception as e:
           
           if current_line.strip() == "except":
              except_block = []
              current_line = input()
              while not current_line.strip() == "endtry":
                 except_block.append(current_line)
                 current_line = input()
              for line in except_block:
                  self.execute_line(line)
    def evaluate_condition(self, condition):
         """ Evaluates a boolean condition (e.g., 'age > 20', 'count == 0'). """
 
         condition = re.sub(r'\s+', '', condition) #Remove spaces
         #Handle single comparisons
         if ">" in condition:
            parts = condition.split(">")
            return self._parse_value(parts[0]) > self._parse_value(parts[1])
         elif "<" in condition:
            parts = condition.split("<")
            return self._parse_value(parts[0]) < self._parse_value(parts[1])
         elif "==" in condition:
             parts = condition.split("==")
             return self._parse_value(parts[0]) == self._parse_value(parts[1])
         elif "!=" in condition:
             parts = condition.split("!=")
             return self._parse_value(parts[0]) != self._parse_value(parts[1])
         else:
             print("Invalid Condition")
             return False
 
    def run(self, code):
         lines = code.split("\n")
         for line in lines:
             self.execute_line(line)
    
    def interpret(self, tokens):
         """
         Interprets the stream of tokens
         """
         return self.run(tokens)
