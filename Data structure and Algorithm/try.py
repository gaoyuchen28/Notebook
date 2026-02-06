def my_generator(m):
    if m==5:
        yield 1
        yield 2

g = my_generator(5)
print(type(g))  
print(my_generator(5)) 
print(my_generator(5))