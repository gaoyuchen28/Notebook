# 归并排序是一种递归算法，它不断地将数组分成两半，直到无法再分割为止，
# 即数组只剩下一个元素（只有一个元素的数组总是已排序的）。
# 然后，将已排序的子数组合并成一个已排序的数组。

def Merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr)//2
        L = arr[:mid]
        R = arr[mid:]
        Merge_sort(L)
        Merge_sort(R)

        i = j = k = 0
        while i< len(L) and j< len(R): # 这个是最基本的判断方法
            if L[i]<=R[j]:
                arr[k] = L[i]
                i+=1
            else:
                arr[k] = R[j]
                j+=1
            k+=1
        
        while i<len(L): # i和j的比较都是基于L和R！！！
            arr[k] = L[i]
            i+=1
            k+=1
        
        while j<len(R):
            arr[k] = R[j]
            j+=1
            k+=1

if __name__ == "__main__":
    arr = list(map(int, input().split(", ")))
    Merge_sort(arr)
    print(", ".join(map(str, arr)))
        
