# Program for nCr
def Calculate(n, r):
  if n == r:
    return 1
  elif n < r:
    return 0
  else:
    if r == 0:
        return 1
    if r == 1:
        return n 
    else:
        return Calculate(n-1,r) + Calculate(n-1,r-1)

print(Calculate(6,3))