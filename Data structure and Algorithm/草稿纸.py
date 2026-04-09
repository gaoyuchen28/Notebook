# Check for Palindrome
def check(left, right):
    if  left >= right:
        print("True")
        return True
    elif n[left] != n[right]:
        print("False")
        return False
    else:
        check(left+1,right-1)

n = str(input())
left = 0
right = len(n)-1
check(left, right)