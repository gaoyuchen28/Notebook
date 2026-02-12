# 假设你是一位出色的 AA 餐厅服务员，你的任务是计算每位顾客的应付金额。

# 输入顾客人数，并赋予total_friends变量。
# 输入总发票数值，并分配给total_bill数值。
# 在付款费用上加上20%的税，并计算最终付款费用均摊给付款额，然后打印。
# 输入格式

# 两个整数

total_friends=int(input())
total_bill = int(input())
total_bill = total_bill*(1+0.2)
print(total_bill/total_friends)

