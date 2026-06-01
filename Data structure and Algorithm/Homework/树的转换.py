class TreeNode:
    def __init__(self, key):
        self.key = key
        self.children = []
        self.parent = None   # 普通树：可以有多个孩子


class BinaryNode:
    def __init__(self, key):
        self.key = key
        self.left = None     # 左儿子
        self.right = None # 右兄弟


def convert(root):
    if root is None:
        return None

    # 创建对应的二叉树结点
    b_root = BinaryNode(root.key)

    # 如果没有孩子，直接返回
    if len(root.children) == 0:
        return b_root

    # 第一个孩子变成左儿子
    b_root.left = convert(root.children[0])

    # 其余孩子依次变成右兄弟
    current = b_root.left

    for child in root.children[1:]:
        current.right = convert(child)
        current = current.right

    return b_root

def height(root):
    if root is None:
        return -1
    else:
        height_left = height(root.left)
        height_right = height(root.right)
        return max(height_left, height_right) + 1

def length(root):
    if root is None:
        return -1
    if len(root.children) == 0:
        return 0
    max_height = 0
    for child in root.children:
        max_height = max(max_height, length(child))
    return max_height + 1

n = input().strip()
count = 0
root = TreeNode(0)
current = root
for i in n:
    if i == 'd':
        count += 1
        nd = TreeNode(count)
        current.children.append(nd)
        nd.parent = current
        current = nd
    elif i == 'u':
        current = current.parent

b_root = convert(root)
print(f"{length(root)} => {height(b_root)}")
