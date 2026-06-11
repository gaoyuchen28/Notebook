#波兰表达式是一种把运算符前置的算术表达式，例如普通的表达式2 + 3的波兰表示法为+ 2 3。
# 波兰表达式的优点是运算符之间不必有优先级关系，也不必用括号改变运算次序，
# 例如(2 + 3) * 4的波兰表示法为* + 2 3 4。
# 本题求解波兰表达式的值，其中运算符包括+ - * /四个。

def is_number(token):
    try:
        float(token)  # 尝试将字符串转换为浮点数
        return True
    except ValueError:
        return False
    
# 由于这道题输入的是浮点数，所以需要有这个判断

def calculate(s):
    operandStack = []
    tokenlist = s.split()

    for i in range(len(tokenlist)-1,-1,-1):
        if is_number(tokenlist[i]) :
            operandStack.append(float(tokenlist[i]))
        else:
            operand1 = operandStack.pop()
            operand2 = operandStack.pop()
            result = doMath(tokenlist[i],operand1,operand2)
            operandStack.append(result) # 这一步很重要，算完要返回去
    return operandStack.pop()

def doMath(op, op1, op2):
    if op == "+":
        return op1 + op2
    elif op == "-":
        return op1 - op2
    elif op == "*":
        return op1 * op2
    else:
        return op1 / op2

s = input()  
print(f"{float(calculate(s)):.1f}")