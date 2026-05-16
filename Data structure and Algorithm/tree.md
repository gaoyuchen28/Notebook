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
```

### 重建二叉树

基本原则：
1) P[0]是树的树根
2) 找到树根P[0]在中序序列中的位置X，并将中序序列以树根为界分为左子树的中序序列Q[:X]和右子树的中序序列Q[X+1:]
3) P[1:X+1]是左子树的前序序列,P[X+1:]是右子树的前序序列，递归建两棵子树  

```python
def Buildtree(preorder, inorder):
    if not preorder: # 这个判断是非常有意义的
        return 
    root_val = preorder[0] # 赋值
    root = Treenode(root_val) # 赋一个结点

    x = inorder.index(root_val)

    ino_left = inorder[1:x]
    ino_right = inorder[x:]

    l = len(root_left)

    pre_left = preorder[1:1+l]
    pre_right = preoder[1+l:]

    root.left = Buildtree(pre_left, ino_left)
    root.right = Buildtree(pre_right, ino_right)

    return root
```

> example: 后序遍历_表达式求值
> ```python
> def post(tree):
>     opers = {
>         "+": operator.add,
>         "-": operator.sub,
>         "*": operator.mul,
>         "/": operator.truediv
>     }
> 
>     if tree:
>         res1 = post(tree.left) # 这里传入的应该是一个结点
>         res2 = post(tree.right)
>         if res1 is not None and res2 is not None:
>             return opers[tree.val](res1, res2)
>         else:
>             return tree.val
> ```
>
> 进一步地：
> 前序遍历得到前缀表达式：
> \- + 3 * 2 9 / 6 4
> 后序遍历得到后缀表达式：
> 3 2 9 * + 6 4 / -
> 中序遍历得到运算符中置表达式：
> 3 + 2 * 9 – 6 / 4

### 非递归遍历二叉树

- 前序遍历

```python
class Binarytree:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    def preorder(self):
        stack = [self]
        while len(stack) > 0:
            node = stack.pop()
            print(node.val)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
```

- 中序遍历

```python
# 前面忽略

def inorder(self):
    stack = [[self,0]]
    while stack:
        node = stack[-1]
        if node[0] == None:
            stack.pop()
            continue
        if node[1] == 0:
            stack.append([node[0].left, 0])
            node[1] = 1
        elif node[1] == 1:
            print(node[0].val)
            stack.pop()
            stack.append([node[0].right, 0])
```

# 优先队列和二叉堆

优先队列（Priority Queue）是一种每次出队都取“优先级最高”的元素，而不是最早进入元素的数据结构。

实现优先队列的经典方案是采用二叉堆数据结构，二叉堆可以通过非嵌套列表来实现

ADT BinaryHeap的操作定义如下：
- `BinaryHeap()`：创建一个空二叉堆对象；
- `insert(k)`：将新key加入到堆中；
- `findMin()`：返回堆中的最小项，最小项仍保留在堆中；
- `delMin()`：返回堆中的最小项，同时从堆中删除；
- `isEmpty()`：返回堆是否为空；
- `size()`：返回堆中key的个数；
- `buildHeap(list)`：从一个key列表创建新堆

要使操作始终保持在对数数量级上，就必须始终保持二叉树的“平衡”，即左右子树拥有相同数量的节点

“完全二叉树”的结构来近似实现“平衡”
- 完全二叉树，叶节点最多只出现在最底层和次底层，而且最底层的叶节点都连续集中在最左边，每个内部节点都有两个子节点，最多可有1个节点例外
- 如果节点的下标为p，那么其左子节点下标为2p，右子节点为2p+1，其父节点下标为p//2

![](1.png){width = 60%}

堆次序Heap Order：任何一个节点x，其父节点p中的key均小于x中的key


# 二叉堆的Python实现

- 二叉堆初始化

```python
class BinHeap:
    def __init__(self):
        self.heaplist = [0]
        self.size = 0
```
- insert(key)方法
  - 需要将新key沿着路径来“上浮”到其正确位置

```python
def percUp(self, i):
    while i//2 > 0:
        if self.heaplist[i] > self.heaplist[i//2]:
            self.heaplist[i], self.heaplist[i//2] = self.heaplist[i//2], self.heaplist[i]
        i = i//2
def insert(self, k):
    self.heaplist.append(k)
    self.size += 1
    self.percUp(self.size)
```

- delMin()方法
  - 移走整个堆中最小的key: 根节点heapList[1]，为了保持“完全二叉树”的性质，只用最后一个节点来代替根节点
  - 将新的根节点沿着一条路径“下沉”，直到比两个子节点都小

```python
def FindMin(self,i):
    if i*2+1>self.size:
        return i*2
    else:
        if self.heaplist[i*2] < self.heaplist[i*2+1]:
            return i*2
        else:
            return i*2+1
def percDown(self,i):
    while i*2 <= self.size:
        mc = FidMin(i)
        if self.heaplist[i] > self.heaplist[mc]:
            self.heaplist[i], self.heaplist[mc] = self.heaplist[mc], self.heaplist[i]
        i = mc
def delMin(self):
    val = self.heaplist[1]
    self.heaplist[1] = self.heaplist[size] # 注意这里size和实际队列长度的区别
    self.size -= 1
    self.heaplist.pop()
    self.percDown(1) # 这里是要往下沉的所以是1
    return val
```

- buildHeap(lst)方法：从无序表生成“堆”
```python
def buildheap(self,alist):
    i = len(alist)//2
    self.size = len(alist)
    self.heaplist = [0] + alist[:]
    while(i>0):
        self.percDown(i)
        i -= 1
```
