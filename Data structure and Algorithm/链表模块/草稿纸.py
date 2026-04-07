# 整数转换为任意进制

def exchange(number, base):
    data = "0123456789ABCDEF"
    if number < base:
        return data[number]
    else:
        return exchange(number//base, base) + data[number%base] # 要注意这里给的data是什么意思！！！

print(exchange(1453, 16))