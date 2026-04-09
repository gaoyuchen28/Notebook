# Print Fibonacci Series in reverse order
def Fib_rev(n, a, b):
    if(n>0):

        Fib_rev(n-1, b, a+b)
        print(a, end = ", ")

n = int(input())
Fib_rev(n,0,1)