# 编写一个程序：将N个巧克力均分给M个儿童。

# 从输入获取一个整数：巧克力数量，并将其分配给 chocolates 变量。
# 从输入获取一个整数：孩子数量，并将其分配给 children 变量。
# 计算每个孩子在除法后得到的巧克力数量并打印出来。
# 计算剩余巧克力的数量并打印出来。

chocolates = int(input())

children = int(input())

print(chocolates // children)
print(chocolates % children)
