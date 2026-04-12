# Find geometric sum of the series
def Calculate(n):
  if n == 0:
    return 1
  else:
    return 1 / pow(3, n) + Calculate(n-1)

print(Calculate(5))
    