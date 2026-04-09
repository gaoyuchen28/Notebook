# Count Set-bits of number
def count(n):
    if n == 0:
        return 0
    if (n & 1) == 1:
        return 1 + count(n>>1)
    else:
        return count(n>>1)

n = int(input())
print(count(n))