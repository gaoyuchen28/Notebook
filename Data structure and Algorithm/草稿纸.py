# 进制转换

def exchange(num, base):
    data = "0123456789ABCDEFG"
    if num < base:
        return data[num]
    else:
        return exchange(num//base,base) + data[num%base]

print(exchange(10,2))