def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
def infixToPostfix(infixexpr):
    prec = {}
    prec["*"] = 3 # 确定符号的优先级
    prec["/"] = 3
    prec["+"] = 2
    prec["-"] = 2
    prec["("] = 1
    opStack = [] # Stack()
    postfixList = [] # 输出的东西
    tokenList = infixexpr.split()

    for token in tokenList:
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or is_number(token):
            postfixList.append(token)
        elif token == '(':
            opStack.append(token)
        elif token == ')':
            toptoken = opStack.pop()
            while toptoken != '(':
                postfixList.append(toptoken)
                toptoken = opStack.pop()
        else:
            while opStack and prec[(opStack[-1])] >= prec[token]:
                postfixList.append(opStack.pop())
            opStack.append(token)
    while opStack:
        postfixList.append(opStack.pop())
    return " ".join(postfixList)

print(infixToPostfix("A * B + C * D"))
print(infixToPostfix("( A + B ) * C - ( D - E ) * ( F + G )"))

print(infixToPostfix("( A + B ) * ( C + D )"))
print(infixToPostfix("( A + B ) * C"))
print(infixToPostfix("A + B * C"))