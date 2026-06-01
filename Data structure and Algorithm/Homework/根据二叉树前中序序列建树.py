class Treenode:
    def __init__(self, val = 0, left = None, right = None):
        self.val = val
        self.left = left
        self.right = right

def Buildtree(preorder, inorder):
    if not preorder:
        return None

    root_val = preorder[0]
    root = Treenode(root_val)

    x = inorder.index(root_val)

    # 中序遍历：左子树 根 右子树
    ino_left = inorder[:x]
    ino_right = inorder[x + 1:]

    # 左子树结点个数
    l = len(ino_left)

    # 前序遍历：根 左子树 右子树
    pre_left = preorder[1:1 + l]
    pre_right = preorder[1 + l:]

    root.left = Buildtree(pre_left, ino_left)
    root.right = Buildtree(pre_right, ino_right)

    return root

def postorder(root,ans):
    if root:
        postorder(root.left, ans)
        postorder(root.right, ans)
        ans.append(root.val)

while True:
    try:
        line1 = input()
        line2 = input()
        root = Buildtree(line1, line2)
        ans = []
        postorder(root, ans)
        print(''.join(ans))
    except EOFError:
        break