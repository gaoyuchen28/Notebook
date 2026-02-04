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
## 

