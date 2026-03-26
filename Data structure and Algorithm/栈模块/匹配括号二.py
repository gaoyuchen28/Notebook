# 混合使用不同的符号的配对问题

def par_checker(symbol_string):
    s = []
    balance = True
    index = 0
    while index < len(symbol_string) and balance:
        symbol = symbol_string[index]
        if symbol in "([{":
            s.append(symbol)
        else:
            top = s.pop()
            if not match(top, symbol):
                balance = False
        index += 1

        if balance and not s:
            return True
        else:
            return False
        
def match(open, close):
    opens = "([{"
    closes = ")]}"
    if opens.index(open) == closes.index(close): # 确定两个括号的索引位置相同
        return True
    else:
        return False
    
print(par_checker('{{}}[]]'))

