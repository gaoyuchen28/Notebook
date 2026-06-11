class BinaryNode:
    def __init__(self, key):
        self.key = key
        self.left = None     # 左儿子
        self.right = None # 右兄弟
def height(root):
    if root is None:
        return 0
    else:
        height_left = height(root.left)
        height_right = height(root.right)
        return max(height_left, height_right) + 1

n = int(input())
nodes = [None] * (n + 1)
for i in range(1, n + 1):
    nodes[i] = BinaryNode(i)
for i in range(1, n + 1):
    a, b = map(int, input().split())
    if a != -1:
        nodes[i].left = nodes[a]
    if b != -1:
        nodes[i].right = nodes[b]
root = nodes[1]

print(height(root))
