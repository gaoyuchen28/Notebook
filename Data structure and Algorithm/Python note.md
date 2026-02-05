# Basics

## Put in and put out

- Python's `input()` function is used to take user input. By default, it returns the user input in form of a **string**. 
  - We are taking multiple input from the user in a single line, splitting the values entered by the user into separate variables for each value using the `split()` method<br>
  ```py
  x, y = input("Enter two values: ").split()
  print("Number of boys: ", x)
  print("Number of girls: ", y)
  x, y, z = input("Enter three values: ").split()
  print("Total number of students: ", x)
  print("Number of boys is : ", y)
  print("Number of girls is : ", z)
  ```
  - Change the Type of Input in Python: 
  ```py
  int(input("Your age: "))
  float(input("Your weight: "))
  ```
- Printing Output using `print()` in Python
  - Python `split()` method is used to break a string into a list of smaller strings based on a specified delimiter.
  ```py
  text = 'geeks for geeks'
  print(text.split())  
  word = 'geeks, for, geeks'
  print(word.split(',')) 
  word = 'geeks:for:geeks'
  print(word.split(':')) 
  word = 'CatBatSatFatOr'
  print(word.split('t'))
  ```
- Find DataType of Input in Python:
  ```py
  a = "Hello World"
  b = 10
  c = 11.22
  d = ("Geeks", "for", "Geeks")
  e = ["Geeks", "for", "Geeks"]
  f = {"Geeks": 1, "for":2, "Geeks":3}
  print(type(a))
  print(type(b))
  print(type(c))
  print(type(d))
  print(type(e))
  print(type(f))
  ```

## Python Variables

- Python variables do not require explicit declaration of type. The type of the variable is inferred based on the value assigned.

#### Rules for Naming Variables

To use variables effectively, we must follow Python’s naming rules:
- Variable names can only contain letters, digits and underscores (_).
- A variable name cannot start with a digit.
- Variable names are case-sensitive like myVar and myvar are different.
- Avoid using Python keywords like if, else, for as variable names.

- Dynamic Typing: Python variables are **dynamically typed**, meaning the same variable can hold different types of values during execution.
  ```py
  x = 10
  x = "Now a string"
  ```

#### Multiple Assignments

- **Assigning Same Value**: Python allows assigning the same value to multiple variables in a single line, which can be useful for initializing variables with the same value.
- **Assigning Different Values**: We can assign different values to multiple variables simultaneously, making the code concise and easier to read.
  ```py
  x, y, z = 1, 2.5, "Python"
  print(x, y, z)
  ```

#### Type Casting a Variable

Type casting refers to the process of converting the value of one data type into another. Python provides several built-in functions to facilitate casting, including int(), float() and str() among others. Basic casting functions are:

int(): Converts compatible values to an integer.<br>
float(): Transforms values into floating-point numbers.<br>
str(): Converts any data type into a string.<br>

#### Deleting a Variable

We can remove a variable from the namespace using the del keyword. This deletes the variable and frees up the memory it was using.

#### Other example

- Swapping Two Variables:
  ```py
  a,b=5,10
  a,b=b,a
  print(a,b)
  ```
- Counting Characters in a String:
  ```py
  word="python"
  length=len(word)
  print("length of the word:", length)
  ```

## Python Operators

#### Arithmetic Operators

| Operator | Description | x=2, y=3 |
| ---------|------------ |----------|
| `+` | Addition: adds two operands | 5 |
| `-` | Subtraction: subtracts two operands |-1 |
| `*` | Multiplication: multiplies two operands | 6 |
| `/` | Division (float): divides the first operand by the second | 0.6666666666666666 |
| `//` | Division (floor): divides the first operand by the second | 0 |
| `%` | Modulus: returns the remainder when the first operand is divided by the second | 2 |
| `**` | Power: Returns first raised to power second | 8 |

#### Comparison Operators

In Python, Comparison (or Relational) operators compares values. It either returns True or False according to the condition.

#### Logical Operators

Python Logical operators perform Logical AND, Logical OR and Logical NOT operations. It is used to combine conditional statements.

- **Order of Precedence of Logical Operators**: When multiple logical operators are used in a single expression, Python evaluates them from left to right and applies short-circuit evaluation. This means Python stops evaluating further conditions as soon as the result is determined.
```py
def check(x):
    print("Method called for value:", x)
    return x > 0

a = check
b = check
c = check

if a(-1) or b(5) or c(10):
    print("At least one of the numbers is positive")
```
b(5) returns True, so Python stops evaluating further conditions. c(10) is never executed due to short-circuit behavior of or.

#### Bitwise Operators

Python bitwise operators are used to perform bitwise calculations on **integers**. The integers are first converted into binary and then operations are performed on each bit or corresponding pair of bits, hence the name bitwise operators. The result is then returned in decimal format.

| Operator | Description | Syntax |
|----------|-------------|--------|
| `&`      | Bitwise AND | x & y  |
| `\|`     | Bitwise OR  | x | y  |
| `~`      | Bitwise NOT | ~x     |
| `^`      | Bitwise XOR | x ^ y  |
| `>>`     | Bitwise right shift | x>> |
| `<<`     | Bitwise left shift | x<<|

- **Bitwise Operator Overloading**: 
Operator Overloading means giving extended meaning beyond their predefined operational meaning. For example operator + is used to add two integers as well as join two strings and merge two lists. It is achievable because the ‘+’ operator is overloaded by int class and str class. You might have noticed that the same built-in operator or function shows different behavior for objects of different classes, this is called Operator Overloading.<br>
```py
# Python program to demonstrate
# operator overloading
class Geek():
    def __init__(self, value):
        self.value = value

    def __and__(self, obj):
        print("And operator overloaded")
        if isinstance(obj, Geek):
            return self.value & obj.value
        else:
            raise ValueError("Must be a object of class Geek")

    def __or__(self, obj):
        print("Or operator overloaded")
        if isinstance(obj, Geek):
            return self.value | obj.value
        else:
            raise ValueError("Must be a object of class Geek")

    def __xor__(self, obj):
        print("Xor operator overloaded")
        if isinstance(obj, Geek):
            return self.value ^ obj.value
        else:
            raise ValueError("Must be a object of class Geek")

    def __lshift__(self, obj):
        print("lshift operator overloaded")
        if isinstance(obj, Geek):
            return self.value << obj.value
        else:
            raise ValueError("Must be a object of class Geek")

    def __rshift__(self, obj):
        print("rshift operator overloaded")
        if isinstance(obj, Geek):
            return self.value >> obj.value
        else:
            raise ValueError("Must be a object of class Geek")

    def __invert__(self):
        print("Invert operator overloaded")
        return ~self.value


# Driver's code
if __name__ == "__main__":
    a = Geek(10)
    b = Geek(12)
    print(a & b)
    print(a | b)
    print(a ^ b)
    print(a << b)
    print(a >> b)
    print(~a)
```
**Output**
```text
And operator overloaded
8
Or operator overloaded
14
Xor operator overloaded
6
lshift operator overloaded
40960
rshift operator overloaded
0
Invert operator overloaded
-11
```
## Keyword and its funcion

#### Value keyword

- `True`
- `False`
- `None`: None is used to define a null value or Null object in Python. It is not the same as an empty string, a False, or a zero. It is a data type of the class NoneType object. 

#### Operator keyword

- `and`
- `or`
- `not`
- `is`: The “is keyword” is used to test whether two variables belong to the same object. The test will return True if the two objects are the same else it will return False even if the two objects are 100% equal.
  - `is`比较的是两个内存地址，而`==`比较的单纯是内容是否一致
- `in`: The in keyword in Python is a powerful operator used for membership testing and iteration. It helps determine whether an element exists within a given sequence, such as a list, tuple, string, set or dictionary.
> **Example 1**: in Keyword with if Statement
> ```py
> a = ["php", "python", "java"]
> 
> if "php" in a:
    print(True)
> ```
> ```text
> TRUE
> ```

> **Example 2**: in keyword in a for loop
> ```py
> s = "GeeksforGeeks"
> 
>  for char in s:
>    if char == 'f':
>        break  
>    print(char)
> ```
> ```text
> G
> e
> e
> k
> s

#### Control Flow Keywords

- `if`
- `else`
- `elif`(if-elif Statement)(else if)
- `for`
- `while`
- `break`
- `continue`
- `pass`: Examples situations where pass is used are empty functions, classes, loops or conditional blocks.
- `try`&`except`&`finally`: 
> **Example 1**:
> ```py 
> # code
> def divide(x, y):
>   try:
>       # Floor Division : Gives only Fractional Part as Answer
>       result = x // y
>       print("Yeah ! Your answer is :", result)
>   except Exception as e:
>      # By this way we can know about the type of error occurring
>       print("The error is: ",e)
> divide(3, "GFG") 
> divide(3,0)

```text
The error is:  unsupported operand type(s) for //: 'int' and 'str'
The error is:  integer division or modulo by zero
```

  - Else Clause:
  ```text
  try:
    # Some Code
  except:
    # Executed if error in the
    # try block
  else:
    # execute if no exception
  ```
  - Finally Keyword:
  ```text
  try:
    # Some Code
  except:
    # Executed if error in the
    # try block
  else:
    # execute if no exception
  finally:
    # Some code .....(always executed)
  ```
- `raise`: 我不懂
- `assert`: In simpler terms, we can say that assertion is the boolean expression that checks if the statement is True or False. If the statement is true then it does nothing and continues the execution, but if the statement is False then it stops the execution of the program and throws an error.
- 


