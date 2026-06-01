class Treenode:
    def __init__(self, val = 0, left = None, right = None):
        self.val = val
        self.left = left
        self.right = right
def buildtree(s,i):
    if s[i] == "*":
        return None, i+1
    root = Treenode(s[i])
    i += 1
    if i < len(s) and s[i] == "(":
        i+=1
        root.left, i = buildtree(s, i)
        if i < len(s) and s[i] == ",":
            i += 1
            root.right, i = buildtree(s,i)

        if i < len(s) and s[i] == ")":
            i+=1

    return root,i

def preorder(root, ans):
    if root:
        ans.append(root.val)
        preorder(root.left, ans)
        preorder(root.right, ans)

def inorder(root, ans):
    if root:
        inorder(root.left, ans)
        ans.append(root.val)
        inorder(root.right, ans)

n = int(input())
for i in range(n):
    s = input()
    root, j= buildtree(s,0)
    ans1 = []
    ans2 = []
    preorder(root, ans1)
    inorder(root, ans2)
    print("".join(ans1))
    print("".join(ans2))
