class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None
    def put(self,key):
        if self.root:
            self._put(key, self.root)
        else:
            self.root = TreeNode(key)
    def _put(self, key, currentNode):
        if key < currentNode.key:
            if currentNode.left:
                self._put(key,currentNode.left)
            else:
                currentNode.left = TreeNode(key)
        elif key > currentNode.key:
            if currentNode.right:
                self._put(key, currentNode.right)
            else:
                currentNode.right = TreeNode(key)
def bfs(root,ans):
    if not root:
        return
    else:
        queue = [root]
        while queue:
            node = queue.pop(0)
            ans.append(str(node.key))
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return ans

lis = list(map(int,input().split()))
hp = BinarySearchTree()
for n in lis:
    hp.put(n)
ans = []
bfs(hp.root, ans)
print(" ".join(ans))

