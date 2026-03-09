# 3, 1, 4, 2
# 1, 3, 4, 2
# 1, 3, 4, 2
# 1, 3, 2, 4

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swap = False
        for j in range(0,n-i-1): #这里必须是n-i-1
            if arr[j]>arr[j+1]:
                arr[j],arr[j+1]=arr[j+1],arr[j]
                swap = True
        if swap==False:
            break

if __name__=="__main__":
    arr = list(map(int, input().split(","))) # 接收一行用空格隔开的数字
    bubble_sort(arr)
    print(', '.join(map(str, arr))) # 将一个列表（list）中的数字快速打印成一行，并用空格隔开
