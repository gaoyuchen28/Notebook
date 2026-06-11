from collections import deque

# 定义节点
class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

# 构建二叉树
def build_tree_level(level_list):
    if not level_list:
        return None
    root_val = level_list[0]
    root = Node(int(root_val))
    queue = deque([root])
    i = 1
    while queue and i < len(level_list):
        node = queue.popleft()
        # 左孩子
        if i < len(level_list):
            if level_list[i] != '#':
                node.left = Node(int(level_list[i]))
                queue.append(node.left)
            i += 1
        # 右孩子
        if i < len(level_list):
            if level_list[i] != '#':
                node.right = Node(int(level_list[i]))
                queue.append(node.right)
            i += 1
    return root

# 验证 BST
def is_bst(node, low=-float('inf'), high=float('inf')):
    if node is None:
        return True
    val = node.val
    if val <= low or val >= high:
        return False
    return is_bst(node.left, low, val) and is_bst(node.right, val, high)

# 主程序
level_input = input().split()
root = build_tree_level(level_input)

if is_bst(root):
    print("YES")
else:
    print("NO")