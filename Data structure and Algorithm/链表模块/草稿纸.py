# 数字求和
def arraySum(arr):
	# code here
	if len(arr) == 1:
		return arr[0]
	else:
		return arr[0] + arraySum(arr[1:])

arr = list(map(int, input().split()))
Sum = arraySum(arr)
print(Sum)