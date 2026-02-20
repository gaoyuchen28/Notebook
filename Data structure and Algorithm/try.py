# 写一个程序：判断一个数字是否是完全平方数。

import math
number = int(input())
square_root = math.sqrt(number)
if square_root % 1 == 0:
    print("完全平方数")
else:
    print("非完全平方数")
    