# 反转字符串

def reverse(arr):
    if len(arr) == 1:
        return arr[0]
    else:
        return reverse(arr[1:]) + arr[0]

arr = list(input().split(", "))

print(reverse(arr))
