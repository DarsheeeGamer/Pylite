# PyLite Programming Language Documentation

## Introduction

PyLite is a simplified programming language inspired by Python. It aims to be easy to learn and use while providing core programming functionalities. PyLite supports basic variable assignments, control flow (if/else, for/while), function definitions, basic data structures, importing other `.py` files and basic access to python packages

## Core Concepts

### 1. Basic Syntax

*   **Line-Based:** Each statement is written on a new line.
*   **Indentation:** Code blocks (within if/else, for/while, functions, classes) are defined using indentation (spaces).
*   **Comments:** Lines starting with `#` are treated as comments and are ignored by the interpreter.
*   **Case-Sensitive:**  Variable names are case sensitive

### 2. Variables

*   **Implicit Types:** You don't need to declare the type of a variable. PyLite infers the type during runtime
*   **Assignment:** Use the `=` operator to assign values to variables.

    ```pylite
    name = "Alice"
    age = 30
    pi = 3.14
    ```

*   **Data Types:** PyLite supports the following data types:
    *   Integers (e.g., `10`, `500`)
    *   Floating-point numbers (e.g., `3.14`, `2.71`)
    *   Strings (e.g., `"hello"`, `"world"`)
    *   Lists (e.g., `[1, 2, 3]`)
    *   Dictionaries (e.g., `{"name": "Alice", "age": 30}`)
    *   Tuples (e.g., `(1, 2, 3)`)

### 3. Data Structures

*   **Lists:** Ordered, mutable (changeable) collections of items, defined using square brackets `[]`

    ```pylite
    numbers = [1, 2, 3, 4, 5]
    print(numbers[0]) # Accessing elements by index
    numbers.append(6)  # Adding elements to the end of a list
    ```
*   **Dictionaries:** Unordered collections of key-value pairs. defined using curly brackets `{}`

     ```pylite
        person = {"name": "Bob", "age": 25}
        print(person["name"])
        print(person["age"])
     ```
*   **Tuples:** Ordered, immutable (unchangeable) collections, defined using parenthesis `()`

   ```pylite
       point = (10, 20)
       print(point[0])
       print(point[1])
   ```

### 4. Operators

*   **Arithmetic:**
    *   `+` (addition)
    *   `-` (subtraction)
    *   `*` (multiplication)
    *   `/` (division)

    ```pylite
    sum = 5 + 10
    product = 5 * 5
    ```
*   **Comparison:**
    *   `>` (greater than)
    *   `<` (less than)
    *   `==` (equal to)
    *   `!=` (not equal to)

     ```pylite
        age = 25
        if age > 18:
            print("You are an adult")
        endif
     ```

*   **String Concatenation:**

     ```pylite
         name = "Alice"
         greeting = "Hello, " + name
     ```

### 5. Control Flow

*   **`if/else/endif` Statement:**
    ```pylite
    age = 25
    if age > 20:
      print("You're an adult")
    else:
      print("You're not an adult")
    endif
    ```
    *   The `if` statement evaluates a condition.
    *   If the condition is `true`, the code inside the `if` block is executed.
    *   If the condition is `false` and there is an `else` block, the `else` block is executed.
    *   The `endif` keyword closes the if statement
*   **`for/endfor` Loop:** Used for iterating over a list or range

    ```pylite
    numbers = [1, 2, 3, 4, 5]
    for n in numbers:
      print(n)
    endfor

    for i in range(1, 5):
        print(i)
    endfor
    ```
    *   `for <var> in <list>`: Iterates over each element in the list, assigning each element to `<var>` for each iteration.
     *   `for <var> in range(start, end)`:  Iterates from `start` (included) to `end` (excluded)
*  **`while/endwhile` Loop:** Used to repeat code execution based on a condition

     ```pylite
         i = 0
         while i < 3:
             print(i)
             i = i + 1
         endwhile
     ```
    *   The `while` loop continues to execute the code block as long as the condition is `true`.

### 6. Functions

*   **Definition:** Functions are defined using the `fun` keyword, followed by the function name, parameters in parentheses, and then the function body.
*   **Return value:** Functions can return a value using the `return` keyword.
*   **Function Block End:** Function blocks are closed using the `endfun` keyword.

    ```pylite
    fun add(x, y):
      result = x + y
      return result
    endfun

    z = add(5, 3)
    print(z)
    ```
### 7. Classes
*   **Definition**: Classes are defined using the `class` keyword, followed by class name and then the class body.
*   **Attributes and methods**: Classes have attributes and methods that can be accessed using the `.` operator
*   **Class End**: Class blocks are closed using the `endclass` keyword.
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
### 8. Exception Handling

*   **Try/Except block:** used to handle exceptions that can happen during the execution of your program.
*   **`try/endtry` block**: contains the code that might cause an exception.
*   **`except/endtry` block**: contains the code that is executed when an exception happens.

      ```pylite
          try:
              x = 1 / 0
          except:
            print("Zero division error")
          endtry
      ```

### 9. Input/Output

*   **`print()`**: Outputs the value to the console.

    ```pylite
    print("Hello, World!")
    ```

### 10. Importing Files

*  **`import`:** used to import variables, functions and classes from other `.py` files
    ```pylite
       import mymodule.py
       print(mymodule.my_var)
    ```
   *  You can also import python packages.
    ```pylite
       import sys
       print(sys.version)
    ```

### 11. Accessing python attributes and functions
*   If a python package is imported or a python class is instantiated, you can access their attributes or functions using the `.` operator.

```pylite
    import sys
    print(sys.version)
    import mymodule.py
    mymodule.my_class_instance.my_method("hello")
```
## Example Program
```pylite
import mymodule.py
print(mymodule.my_var)
print(mymodule.my_func(3))
mymodule.my_class_instance.my_method("hello")

try:
    x = 1 / 0
except:
  print("Zero division error")
endtry

import sys
print(sys.version)

numbers = [1,2,3,4,5]
print(numbers[0])
numbers.append(6)
print(numbers)

t = (1,2,3)
print(t[0])

d = {"name":"bob", "age": 25}
print(d["name"])
print(d["age"])

age = 25
if age > 20:
    print("You're an adult")
else:
    print("You're not an adult")
endif

for n in numbers:
    print(n)
endfor

i = 0
while i < 3:
    print(i)
    i = i + 1
endwhile

fun add(x,y):
  result = x + y
  return result
endfun

z = add(5,3)
print(z)

fun sayHello(name):
    print("Hi " + name)
    return "done"
endfun

sayHello("Bob")

class Person:
    name = "default"
    def __init__(self, name):
        self.name = name
    fun say_name(self, extra):
        print(self.name + extra)
    endfun
endclass
p = Person("alice")
p.say_name("!")

```

## Limitations
*   PyLite does not support nesting of control flow statements and function and class declarations.
*   The interpreter is very naive in how it handles string, math and condition parsing.
*   Error messages are basic
*   Some python features are not supported (e.g decorators, lambda, etc)
*   Object-oriented programming is supported only in the very basic way
