# 二叉树的遍历

### 深度优先遍历

使用类（class）来定义树的节点。每个节点包含三个属性：节点的值 (`val`)、指向左子节点的引用 (`left`) 和指向右子节点的引用 (`right`)。

```python
class Treenode:
    def __init__(self, val = 0, left = None, right = None):
    self.val = val
    self.left = left
    self.right = right
```

- 前序遍历
  
```python
def preorder(root):
    if root:
        print(root.val)
        preorder(root.left)
        preorder(root.right)
```

- 中序遍历

```python
def inorder(root):
    if root:
        inorder(root.left)
        print(root.val)
        inorder(root.right)
```

- 后序遍历

```python
def postorder(root):
    if root:
        postorder(root.left)
        postorder(root.right)
        print(root.val)
```

> example:
> https://leetcode.cn/problems/binary-tree-inorder-traversal/
>

> example: 
> 用stack模拟的“颜色填充法”
>

### 广度优先遍历

```python
def bfs(root):
    if not root:
        return
    else:
        queue = [root]
        while queue:
            node = queue.pop(0)
            print(node.val)
            if node.left():
                queue.append(node.left())
            if node.right():
                queue.append(node.right())