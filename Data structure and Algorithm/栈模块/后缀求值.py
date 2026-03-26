def postfixEval(postfixExpr):
    operandStack = []
    tokenList = postfixExpr.split()
    for token in tokenList:
        if is_number(token):
            operandStack.append(float(token))
        else:
            operand1 = operandStack.pop()
            operand2 = operandStack.pop()
            result = doMath(token, operand1, operand2)
            operandStack.append(result)
    return operandStack.pop()

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
def doMath(s,op1,op2):
    if s == "*":
        return op1 * op2
    elif s == "/":
        return op2 / op1
    elif s == "+":
        return op1 + op2
    else:
        return op2 - op1

print(postfixEval('7 8 + 3 2 + /'))