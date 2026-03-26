def par_checker(symbol_string):
    s = []
    balance = True
    index = 0
    while index<len(symbol_string) and balance:
        symbol = symbol_string[index]
        if symbol == "(":
            s.append(symbol)
        else:
            if not s: #判断栈是否为空
                balance = False
            else:
                s.pop() # 直接pop就可以
        index += 1

    if balance and not s:
        balance = True

    else:
        balance = False
    
    return balance

print(par_checker('((()))'))
print(par_checker('(()'))