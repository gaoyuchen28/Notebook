def Select_sort(arr):
    n = len(arr)
    for i in range(n):
        m = arr[i]
        for j in range(0,n-i):
            if arr[j] > m:
                m = arr[j]
                p = j
        if p < n-i-1:
            arr[p], arr[n-i-1] = arr[n-i-1], arr[p]

if __name__ == "__main__":
    arr = list(map(int,input().split(",")))
    Select_sort(arr)
    print(", ".join(map(str,arr)))
