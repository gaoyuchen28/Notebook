# 例题: 爬楼梯
# 树老师爬楼梯，他可以每次走1级或者2级，输入楼梯的级数，求不同的走法数
# 例如：楼梯一共有3级，他可以每次都走一级，或者第一次走一级，第二次走两级，
# 也可以第一次走两级，第二次走一级，一共3种方法。



def count(n): # i 表示已经压入了多少个数，stack_size 表示当前栈内元素个数
    if n == 0:
        return 1
    elif n == 1:
        return 1
    elif n == 2:
        return 2
    else:
        return count(n-1) + count(n-2)
    

n = int(input())
print(count(n))
    
