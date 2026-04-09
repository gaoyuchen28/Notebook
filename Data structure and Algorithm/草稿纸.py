# 例题:  Add Two Numbers


def addTwoNumbers(l1, l2):
    if len(l1) == 1 or len(l2) == 1:
        result = l1[0] + l2[0]
        n.append(result)
        return
    else:
        if l1[0] + l2[0] >= 10:
            result = (l1[0] + l2[0])%10
        else:
            result = l1[0] + l2[0]
        addTwoNumbers(l1[1:],l2[1:])
        n.append(result)

n = []
l1 = list(map(int, input().split(",")))
l2 = list(map(int, input().split(",")))

addTwoNumbers(l1, l2)
    
print(n)
