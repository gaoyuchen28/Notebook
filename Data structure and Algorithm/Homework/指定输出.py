x, y = 5, 5
def outer_function():
    x = 10

    def inner_function():
        nonlocal x
        global y
        x = 15
        y = 15
    inner_function()

    print(f"outer x: {x}, outer y: {y}")

outer_function()
print(f"global x: {x}, global y: {y}")