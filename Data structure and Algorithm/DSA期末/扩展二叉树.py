class Treenode:
    def __init__(self, val = 0, left = None, right = None):
        self.val = val
        self.left = left
        self.right = right

preorder = input().strip()

def build_tree(seq):
    """根据扩展二叉树的先序序列递归建树"""
    idx = 0  # 用于记录当前处理的位置
    def helper():
        nonlocal idx
        if idx >= len(seq):
            return None

        val = seq[idx]
        idx += 1

        # 遇到 '.' 表示空节点
        if val == '.':
            return None

        # 创建当前节点
        node = Treenode(val)

        # 递归构建左子树
        node.left = helper()
        # 递归构建右子树
        node.right = helper()

        return node

    return helper()

def inorder(root, ans):
    if root:
        inorder(root.left,ans)
        ans.append(root.val)
        inorder(root.right,ans)
    return ans

def postorder(root, ans):
    if root:
        postorder(root.left,ans)
        postorder(root.right,ans)
        ans.append(root.val)
    return ans


# 构建二叉树
root = build_tree(preorder)
ans1 = []
ans2 = []
ans1 = inorder(root, ans1)
ans2 = postorder(root, ans2)
print(''.join(ans1))
print(''.join(ans2))

