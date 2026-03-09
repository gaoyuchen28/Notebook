# 快速排序是一种排序算法。
# 该算法选择一个基准元素，然后重新排列数组元素，
# 使得所有小于基准元素的元素移动到基准元素的左侧，
# 所有大于基准元素的元素移动到基准元素的右侧。
# 最后，该算法递归地对基准元素左右两侧的子数组进行排序。

def Quick_sort(arr, left, right):
    if left<right : # 确定排到哪里就停止了
        position = Pos(arr,left,right)
        Quick_sort(arr, left, position-1)
        Quick_sort(arr, position+1, right)

def Pos(arr, left, right):
    i = right-1
    j = left
    base = arr[right]
    while j <= i:
        while j <= right and arr[j]<base: # j负责找比基准大的数（找到大数就停下了）
            j+=1
        while i >= left and arr[i]>=base: # j负责找比基准小的数（找到小数就停下了）
            i-=1
        if i > j:
            arr[i], arr[j] = arr[j], arr[i]
    if arr[j] > arr[right]: #负责换的指针字母一定是那个负责找比基准更大的数的 
        arr[right], arr[j] = arr[j], arr[right]
    return j

arr = list(map(int, input().split(", ")))
Quick_sort(arr, 0, len(arr) - 1)
print(' ,'.join(map(str, arr)))