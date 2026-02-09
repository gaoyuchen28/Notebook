a = 15 # global variable

# function to change a global value
def change():
    # increment value of a by 5
    b = a + 5
    a = b
    print(a)


change()