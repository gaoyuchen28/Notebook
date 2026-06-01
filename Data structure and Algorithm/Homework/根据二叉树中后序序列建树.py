class Treenode:
    def __init__(self, val = 0, left = None, right = None):
        self.val = val
        self.left = left
        self.right = right

def Buildtree(postorder, inorder):
    if not postorder: # 这个判断是非常有意义的
        return 
    root_val = postorder[-1] # 赋值
    root = Treenode(root_val) # 赋一个结点

    x = inorder.index(root_val)

    ino_left = inorder[:x]
    ino_right = inorder[x+1:]

    l = len(ino_left)

    post_left = postorder[0:l]
    post_right = postorder[l:-1]

    root.left = Buildtree(post_left, ino_left)
    root.right = Buildtree(post_right, ino_right)

    return root

def preorder(root, ans):
    if root:
        ans.append(root.val)
        preorder(root.left,ans)
        preorder(root.right,ans)
    return ans

io = input()
po = input()
ans = []
root = Buildtree(po,io)

ans = preorder(root,ans)

print("".join(ans))