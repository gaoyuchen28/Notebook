# Minimum and Maximum elements Using Recursion

def Max(arr):
    if len(arr) == 1:
        return arr[0]
    else:
        if arr[len(arr)-2] > arr[len(arr)-1]:
            arr[len(arr)-2], arr[len(arr)-1] = arr[len(arr)-1],arr[len(arr)-2]
        return Max(arr[:len(arr)-1])

arr = list(map(int,input().split(", ")))
arr1 = Max(arr)
print(arr1)
