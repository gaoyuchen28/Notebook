# 在某个字符串（长度不超过100）中有左括号、右括号和大小写字母；
# 规定（与常见的算数式子一样）任何一个左括号都从内到外与在它右边且距离最近的右括号匹配。
# 写一个程序，找到无法匹配的左括号和右括号，输出原来字符串，
# 并在下一行标出不能匹配的括号。
# 不能匹配的左括号用"$"标注,不能匹配的右括号用"?"标注.

# 怎样一直接受信息
lines = []

while True:
    try:
        line = input()
        if line == "": # 如果用户直接按回车，line 就是空字符串
            break
        lines.append(line)
    except EOFError:
        break

ans = []

for s in lines: # 遍历lines
    index = 0
    stack = []
    Mark = []
    while index<len(s):
        if s[index] == "(":
            stack.append(index) #stack用来存坐标!!!!
            Mark += ' ' 
        elif s[index] == ')':
            if not stack: #注意s和stack
                Mark += '?'
            else:
                stack.pop()
                Mark +=' '
        else:
            Mark += ' '
        index += 1
    
    while len(stack):
        Mark[stack[-1]] = '$' # 因为是从末尾pop，所以这样逻辑比较通畅
        stack.pop()

    print(s)
    print(''.join(map(str, Mark)))