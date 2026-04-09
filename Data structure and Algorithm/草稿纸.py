# Pow(x, n)
def myPow(x, n):
    """
    :type x: float
    :type n: int
    :rtype: float
    """
    if n == 0:
        return 1
    elif n > 0:
        return myPow(x,n-1)*x
    elif 0 > n:
        return myPow(x,n+1)/x

x = float(input())
n = int(input())

print(f"{myPow(x,n):.6f}")