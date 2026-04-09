# Binary to Gray code
def convert(s):
    n = len(s)
    if n == 1:
        return str(s[0])
    else:
        result = s[n-1]^s[n-2]
        return convert(s[:(n-1)]) + str(result)
n = str(input())
s = []
for i in range(len(n)):
    s.append(int(n[i]))
print(convert(s))