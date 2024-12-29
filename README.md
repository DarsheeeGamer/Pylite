# PyLite Programming Language

PyLite is a simplified programming language inspired by Python, designed for learning and experimentation. It aims to provide a subset of core Python functionalities with a more straightforward syntax.

## Features

*   **Simplified Syntax:**  Aims for easier-to-learn keywords and structure.
*   **Implicit Typing:** No need to declare variable types explicitly.
*   **Basic Data Types:** Supports integers, floats, strings, lists, dictionaries and tuples.
*   **Control Flow:** Includes `if/else/endif`, `for/endfor`, and `while/endwhile` statements.
*   **Functions:**  Supports function definitions with `fun`, parameters, and return values.
*   **Classes:** Supports class definitions with `class`, methods and properties.
*    **Exception Handling:**  Supports basic exception handling with `try/except/endtry`
*   **Importing:** Allows importing other `.py` files and provides limited support for importing python packages.
*   **Basic I/O:** Includes a `print` function for output.
*   **Python Interop:** When a python module is imported, you can call their functions and access their attributes using python reflection.

## Getting Started

### Prerequisites

*   Python 3.6 or higher
*   You will need to have created a directory named `pylite` and the following files inside it:
    *  `pylite/lexer.py`
    *  `pylite/parser.py`
    *  `pylite/interpreter.py`
    *  `pylite/main.py`
  

### Running PyLite

1.  **Clone the repository:**
    ```bash
    cd ~/projects
    git clone https://github.com/DarsheeeGamer/Pylite.git
    ```

2.  **Navigate to the `pylite` directory:**

   ```bash
   # Assuming the `pylite` directory is located in the same location
   cd pylite
   ```

3.  **Run PyLite with a file or interactively:**
    *   **Run a file:**
        ```bash
        python main.py my_program.pylite
        ```
        (assuming you have a file named `my_program.pylite`).
    *   **Interactive mode:**
        ```bash
        python main.py
        ```
        Type your PyLite code line by line. Type `exit` to quit.

## Language Syntax

### 1. Variables

*   Variables are dynamically typed and assigned using the `=` operator.

    ```pylite
    name = "Alice"
    age = 30
    pi = 3.14
    numbers = [1, 2, 3, 4]
    person = {"name": "Bob", "age": 25}
    point = (1,2)
    ```

### 2. Control Flow

*   **`if/else` statements:**

    ```pylite
    age = 25
    if age > 20:
        print("You're an adult")
    else:
        print("You're not an adult")
    endif
    ```
*   **`for` loops:**

    ```pylite
    numbers = [1, 2, 3, 4, 5]
    for n in numbers:
        print(n)
    endfor

    for i in range(1, 5):
        print(i)
    endfor
    ```
*   **`while` loops:**

    ```pylite
    i = 0
    while i < 3:
      print(i)
      i = i + 1
    endwhile
    ```

### 3. Functions

*   Use the `fun` keyword to define functions.

    ```pylite
    fun add(x, y):
      result = x + y
      return result
    endfun
    z = add(5, 3)
    print(z)
    ```

### 4. Classes

*  Use the `class` keyword to define classes.

    ```pylite
    class Person:
      name = "default"
      fun __init__(self, name):
        self.name = name
      endfun
      fun say_name(self, extra):
          print(self.name + extra)
      endfun
    endclass
    p = Person("alice")
    p.say_name("!")
    ```

### 5. Exception Handling

*   Use `try/except` blocks to handle exceptions.

    ```pylite
     try:
         x = 1 / 0
     except:
       print("Zero division error")
     endtry
    ```

### 6. Import Statements

*   Use the `import` keyword to import code from other `.py` files or python packages

     ```pylite
        import mymodule.py
        print(mymodule.my_var)

        import sys
        print(sys.version)
     ```

### 7. Attribute Access
*   You can access attributes or call methods of imported modules or class instances using the `.` operator.

   ```pylite
   import mymodule.py
   mymodule.my_class_instance.my_method("hello")
    ```
## Limitations

*   PyLite is a simplified language with fewer features than Python.
*   It does not support all of Python's syntax.
*   The translator is limited and can't translate all python code to pylite
*   Error messages are very basic.
*   No nesting of control flow statement is supported
*   The interpreter is not optimized for performance
*   Object-oriented programming is supported in a basic way

## Contributing

Contributions are welcome! If you'd like to help improve PyLite, please feel free to fork this project and submit pull requests.
