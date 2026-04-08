# 出栈序列统计
# 你已经知道栈的操作有两种：push和pop，前者是将一个元素进栈，后者是将栈顶元素弹出。
# 现在要使用这两种操作，由一个操作序列可以得到一系列的输出序列。
# 请你编程求出对于给定的n，计算并输出由操作数序列1，2，…，n，经过一系列操作可能得到的输出序列总数。


def count(i, stack_size): # i 表示已经压入了多少个数，stack_size 表示当前栈内元素个数
    if i == n: # 这个时候唯一的办法就是把剩下的元素挨个弹出
        return 1
    else:
        result = 0
        if stack_size > 0:
            result += count(i, stack_size - 1)
            result += count(i + 1, stack_size + 1)
        else:
            result = count(i + 1, stack_size + 1)
        return result

n = int(input())
print(count(0,0))
    
