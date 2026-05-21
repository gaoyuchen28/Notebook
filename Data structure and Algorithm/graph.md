# 图的基本概念及相关术语

- 顶点Vertex（也称“节点Node”）：是图的基本组成部分，顶点具有名称标识Key，也可以携带数据项payload
- 边Edge（也称“弧Arc”）：作为2个顶点之间关系的表示，边连接两个顶点；边可以是无向或者有向的，相应的图称作“无向图”和“有向图”
- 权重Weight：为了表达从一个顶点到另一个顶点的“代价”，可以给边赋权；例如公交网络中两个站点之间的“距离”、“通行时间”和“票价”都可以作为权重。

一个图G可以定义为G=(V, E)，其中V是顶点的集合，E是边的集合，E中的每条边e=(v, w)，v和w都是V中的顶点
（如果是赋权图，则可以在e中添加权重分量）

![](3.png)

- 有向图：边有方向(有起点和终点)，无向图：边没有方向, 边只是逻辑上表示两个顶点有直接关系，边是直的还是弯的，边有没有交叉，都没有意义。
- 顶点的度数：和顶点相连的边的数目。(无所谓于方向)
- 顶点的出度：有向图中，以该顶点作为起点的边的数目 
- 顶点的入度：有向图中，以该顶点作为终点的边的数目
- 顶点的出边：有向图中，以该顶点为起点的边
- 顶点的入边：有向图中，以该顶点为终点的边
- 路径Path：图中的路径，是由边依次连接起来的顶点序列，无权路径的长度为边的数量；带权路径的长度为所有边权重的和
- 回路（环）：起点和终点相同的路径
- 简单路径：除了起点和终点可能相同外，其它顶点都不相同的路径
- 完全图：
  - 完全无向图：任意两个顶点都有边相连
  - 完全有向图：任意两个顶点都有两条方向相反的边
- 连通：如果存在从顶点u到顶点v的路径，则称u到v连通，或u可达v。无向图中，u可达v,必然v可达u。有向图中，u可达v，并不能说明v可达u。
  - 连通无向图：无向图中任意两个顶点u和v互相可达。
  - 强连通有向图：有向图中任意两个顶点u和v互相可达。
- 子图：从图中抽取部分或全部边和点构成的图
- 连通分量（极大连通子图）：无向图的一个子图，是连通的，且再添加任何一些原图中的顶点和边，新子图都不再连通。（以下那张图一共有3个连通分量）
  
  ![](4.png)

- 强连通分量：有向图的一个子图，是强连通的，且再添加任何一些原图中的顶点和边，新子图都不再强连通。
- 网络：带权无向连通图
- 圈Cycle
  - 如果有向图中不存在任何圈，则称作“有向无圈图directed acyclic graph: DAG”

# 图抽象数据类型

抽象数据类型ADT Graph定义如下：
- Graph()：创建一个空的图；
- addVertex(vert)：将顶点vert加入图中
- addEdge(fromVert, toVert)：添加有向边
- addEdge(fromVert, toVert, weight)：添加带权的有向边
- getVertex(vKey)：查找名称为vKey的顶点
- getVertices()：返回图中所有顶点列表
- in：按照vert in graph的语句形式，返回顶点是否存在图中True/False

ADT Graph的实现方法有两种主要形式：
- 邻接矩阵adjacency matrix
- 邻接表adjacency list

### 邻接矩阵adjacency matrix

矩阵的每行和每列都代表图中的顶点
如果两个顶点之间有边相连，设定行列值

![](5.png)

  - 无向图的邻接矩阵为对称矩阵
  - 有向图的邻接矩阵为非对称矩阵

pros: 可以很容易得到顶点是如何相连
cons: 边数很少，成为“稀疏sparse”矩阵，而大多数问题所对应的图都是稀疏的，边远远少于|V|^2这个量级

### 邻接列表Adjacency List

主列表中的每个顶点，再关联一个与自身有边连接的所有顶点的列表

![](6.png)

嵌套列表

邻接列表法的存储空间紧凑高效，很容易获得顶点所连接的所有顶点，以及连接边的信息

# 图抽象数据类型的Python实现

呈现案例：

```python
g = Graph()

for i in range(6):
    g.addVertex(i)

g.addEdge(0, 1, 5)
g.addEdge(0, 5, 2)
g.addEdge(1, 2, 4)
g.addEdge(2, 3, 9)
g.addEdge(3, 4, 7)
g.addEdge(3, 5, 3)
g.addEdge(4, 0, 1)
g.addEdge(5, 4, 8)
g.addEdge(5, 2, 1)

for v in g:
    for w in v.getConnections():
        print("(%s, %s)" % (v.getId(), w.getId()))
```

### 顶点Vertex类

```python
class Vertex:
    def __init__(self, key):
        self.id = key
        self.connectedTo = {}
        self.color = 'white' # 顶点访问状态（white=未访问，gray=正在访问，black=已完成）
        self.distance = float('inf') # 当前顶点到起始点的距离，初始设为无穷大
        self.pred = None # 处理这个顶点的前驱，用于记录路径
 
    def addNeighbor(self, nbr, weight=0):
        self.connectedTo[nbr] = weight # 是字典，nbr是顶点对象的key

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getWeight(self, nbr):
        return self.connectedTo[nbr]
```

### 图graph类

```python
class Graph:

    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self, key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self, n): # 通过key查找顶点
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self, n):
        return n in self.vertList
    
    def addEdge(self, f, t, cost=0): # f起点，t终点
        if f not in self.vertList:
            nv = self.addVertex(f)

        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], cost)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        eturn iter(self.vertList.values())
```

### 邻接矩阵版本: 顶点Vertex类

```python
class Vertex_adj_mat:

    def __init__(self, key):
        self.id = key
        self.color = 'white'          # BFS/DFS 初始颜色
        self.distance = float('inf')  # 初始距离设为无穷大
        self.pred = None              # 前驱节点

    def addNeighbor(self, nbr, weight=0):
        self.connectedTo[nbr] = weight

    def getId(self):
        return self.id

    def getWeight(self, nbr):
        return self.connectedTo[nbr]

    def getPred(self):
        return self.pred

    def setPred(self, pred):
        self.pred = pred

    def getColor(self):
        return self.color

    def setColor(self, color):
        self.color = color

    def getDistance(self):
        return self.distance

    def setDistance(self, distance):
        self.distance = distance
```

### 邻接矩阵版本: 图Graph类

```python
class Graph_adj_mat:

    def __init__(self, num_vertices=8): # 需事先设置节点数量
        self.vertList = {}
        self.adj_matrix = [[0] * num_vertices for _ in range(num_vertices)] # 二维数据存储邻接矩阵
        self.numVertices = num_vertices

    def addVertex(self, key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex_adj_mat(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self, n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self, n):
        return n in self.vertList

    def addEdge(self, v1, v2, weight=1):
        if 0 <= v1 < self.num_vertices and 0 <= v2 < self.num_vertices:
            self.adj_matrix[v1][v2] = weight
            self.adj_matrix[v2][v1] = weight  # 无向图（有向图删掉这一行）

    def get_neighbors(self, idx):
        neighbors = []

        for j in range(self.num_vertices):
            if self.adj_matrix[idx][j] != 0:
                neighbors.append(j)

        return neighbors

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())
```

# 图的应用：词梯问题

### 词梯Word Ladder问题

【目标】: 是找到最短的单词变换序列
【解决步骤】: 
- 将可能的单词之间的演变关系表达为图
- 采用“广度优先搜索 BFS”，来搜寻从开始单词
- 到结束单词之间的所有有效路径
- 选择其中最快到达目标单词的路径
【备注】: 此时的边是没有权重的，所以用了广度优先算法

1. 构建单词关系图：将所有单词作为顶点加入图中，再设法建立顶点之间的边，将单词作为顶点的标识Key，如果两个单词之间仅相差1个字母，就在它们之间设一条边
  > 改进算法：
  > 1. 创建大量的桶，每个桶可以存放若干单词: 桶标记是去掉1个字母，通配符“_”占空的单词
  > 2. 所有匹配标记的单词都放到这个桶里
  > 3. 所有单词就位后，再在同一个桶的单词之间建立边即可
  > 
  > ![](7.png)
  >

采用字典建立桶

```python
def buildGraph(wordFile):
    d = {}
    g = Graph()

    # 打开单词文件，每一行通常是一个单词
    wfile = open(wordFile, 'r')

    # 第一步：建立 bucket
    # bucket 的作用：把“只差一个字母”的单词放到同一组里
    for line in wfile:
        # 去掉每一行末尾的换行符
        word = line[:-1]

        # 依次把单词的每一个位置替换成 "_"
        # 例如 fool:
        # _ool, f_ol, fo_l, foo_
        for i in range(len(word)):
            bucket = word[:i] + '_' + word[i + 1:]

            # 如果这个 bucket 已经存在，就把当前单词加入这个 bucket
            if bucket in d:
                d[bucket].append(word)

            # 如果这个 bucket 不存在，就创建一个新的列表
            else:
                d[bucket] = [word]

    # 第二步：根据 bucket 建图
    # 同一个 bucket 中的单词，说明它们只差一个字母
    # 因此这些单词之间应该有边
    for bucket in d.keys():
        for word1 in d[bucket]:
            for word2 in d[bucket]:

                # 避免自己和自己连边
                if word1 != word2:
                    g.addEdge(word1, word2)

    # 返回构建好的图
    return g
```

# 实现广度优先搜索/遍历

![](8.png)

- 深度优先（能往前走就往前走）1-2-4-8-5-6-3-7 这里会涉及一个会退过程
- 广度优先（按距离起点的距离，即最小边数从小到大遍历）1-2-3-4-5-6-7-8

在单词关系图建立完成以后，需要继续在图中寻找词梯问题的最短序列，因为广度优先算是按照距离进行遍历，所以比较符合广度优先搜索
> BFS搜索所有从s可到达顶点的边，而且在达到更远的距离k+1的顶点之前，BFS会找到全部距离为k的顶点
> 可以想象为以s为根，构建一棵树的过程，从顶部向下逐步增加层次, 广度优先搜索能保证在增加层次之前，添加了所有兄弟节点到树中

从新回顾一下定义的时候引入的三个特性：
- 距离distance：从起始顶点到此顶点路径长度；
- 前驱顶点predecessor：可反向追溯到起点；
- 颜色color：标识了此顶点是尚未发现（白色）、已经发现（灰色）、还是已经完成探索（黑色）

还需要用一个队列Queue来对已发现的顶点进行排列：决定下一个要探索的顶点（队首顶点）

1. 从队首取出一个顶点作为当前顶点；
2. 遍历当前顶点的邻接顶点，如果是尚未发现的白色顶点，则将其颜色改为灰色（已发现），**距离增加1**，前驱顶点为当前顶点，加入到队列中
3. 遍历完成后，将当前顶点设置为黑色（所有的邻接节点都已经是灰色了，已探索过），循环回到步骤1的队首取当前顶点

补充需要放入`Vertex` 类中：

```python
def getPred(self):
    # 返回当前顶点的前驱节点
    return self.pred


def setPred(self, pred):
    # 设置当前顶点的前驱节点
    self.pred = pred


def getColor(self):
    # 返回当前顶点的颜色状态
    return self.color


def setColor(self, color):
    # 设置当前顶点的颜色状态
    self.color = color


def getDistance(self):
    # 返回当前顶点到起始顶点的距离
    return self.distance


def setDistance(self, distance):
    # 设置当前顶点到起始顶点的距离
    self.distance = distance
```

BFS算法：

```python
def bfs(g, start):
    # 将起始顶点到自己的距离设置为 0
    start.setDistance(0)

    # 起始顶点没有前驱节点
    start.setPred(None)

    # 创建一个队列，用于 BFS 的“先进先出”遍历
    vertQueue = Queue()

    # 先把起始顶点放入队列
    vertQueue.enqueue(start)

    # 只要队列不为空，就继续搜索
    while vertQueue.size() > 0:

        # 取出队首顶点，作为当前正在访问的顶点
        currentVert = vertQueue.dequeue()

        # 遍历当前顶点的所有邻接点
        for nbr in currentVert.getConnections():

            # 如果邻接点还是 white，说明它还没有被访问过
            if nbr.getColor() == 'white':

                # 将邻接点标记为 gray，表示已经发现，但还没有完全处理完
                nbr.setColor('gray')

                # 邻接点距离 = 当前顶点距离 + 1
                # 因为 BFS 每走一条边，距离增加 1
                nbr.setDistance(currentVert.getDistance() + 1)

                # 记录邻接点的前驱节点
                # 说明 nbr 是从 currentVert 访问到的
                nbr.setPred(currentVert)

                # 把这个邻接点加入队列，等待之后继续访问它的邻居
                vertQueue.enqueue(nbr)

        # 当前顶点的所有邻居都检查完后，将其标记为 black
        # black 表示这个顶点已经彻底处理完成
        currentVert.setColor('black')
    
```

可以通过一个回途追溯函数来确定FOOL到任何单词顶点的最短词梯

```python
def traverse(y):
    # 从目标节点 y 开始
    x = y

    # 只要当前节点 x 有前驱节点，就继续向前回溯
    while x.getPred():
        # 打印当前节点的 id
        print(x.getId())

        # 让 x 变成它的前驱节点
        # 也就是沿着 BFS 记录的路径往回走一步
        x = x.getPred()

    # 打印最后一个节点
    # 一般是起始节点，因为起始节点的 pred 是 None
    print(x.getId())
```

BFS算法主体是两个循环的嵌套: 
- while循环对每个顶点访问一次，所以是O(|V|)
- 而嵌套在while中的for，由于每条边只有在其起始顶点u出队的时候才会被检查一次,而每个顶点最多出队1次，所以边最多被检查1次，一共是O(|E|)
- 综合起来BFS的时间复杂度为O(|V|+|E|)

词梯问题还包括两个部分算法:
- 建立BFS树之后，回溯顶点到起始顶点的过程，最多为O(|V|)
- 创建单词关系图也需要时间，最多为O(|V|2)

补充：邻接矩阵版本的广度优先搜索

```python
def bfs_adj_mat(graph, start):
    # 把起点到自己的距离设为 0
    start.setDistance(0)

    # 起点没有前驱节点
    start.setPred(None)

    # 创建队列，用于 BFS
    vertQueue = Queue()

    # 把起点加入队列
    vertQueue.enqueue(start)

    # 只要队列不为空，就继续搜索
    while vertQueue.size() > 0:

        # 取出队首顶点，作为当前正在处理的点
        currentVert = vertQueue.dequeue()

        # 根据邻接矩阵，找到 currentVert 的所有邻居编号
        for neighbor_idx in graph.get_neighbors(currentVert.get_id()):

            # 根据邻居编号，取出真正的 Vertex 对象
            nbr = graph.getVertex(neighbor_idx)

            # 如果这个邻居还没有被访问过
            if nbr.getColor() == 'white':

                # 标记为 gray，表示已经发现但还没完全处理完
                nbr.setColor('gray')

                # 邻居的距离 = 当前点的距离 + 1
                nbr.setDistance(currentVert.getDistance() + 1)

                # 记录邻居的前驱节点
                nbr.setPred(currentVert)

                # 把邻居加入队列，等待之后继续扩展
                vertQueue.enqueue(nbr)

        # 当前节点的所有邻居都处理完了，标记为 black
        currentVert.setColor('black')
```

时间复杂度为O(|V|2)

# 广度优先搜索的应用 

### 抓住那头牛

农夫知道一头牛的位置，想要抓住它。农夫和牛都位于数轴上，农夫起始位于点N(0<=N<=100000)，牛位于点K(0<=K<=100000)。农夫有两种移动方式：
- 从X移动到X-1或X+1，每次移动花费一分钟
- 从X移动到2*X，每次移动花费一分钟
假设牛没有意识到农夫的行动，站在原地不动。农夫最少要花多少时间才能抓住牛？

【解决策略】：
1. 把问题抽象成图搜索问题：如果两个数字之间可以一步到达，就在它们之间连一条边。
2. 确定起点和终点
3. 使用广度优先搜索 BFS
4. 第一次找到终点时停止

用队列进行BFS:
(1) 把初始顶点S0放入Open表中；
(2) 如果Open表为空，则问题无解，失败退出；
(3) 把Open表的第一个顶点取出放入Closed表，并记该顶点为n；
(4) 考察顶点n是否为目标顶点。若是，则得到问题的解，成功退出；
(5) 若顶点n不可扩展，则转第(2)步；
(6) 扩展顶点n，将其不在Closed表和Open表中的子顶点(判重）放入Open表的尾部，并为每一个子顶点设置指向父顶点的指针(或记录顶点的层次），然后转第(2)步。

![](9.png)

![](10.png)

```python
import collections


class Step:
    def __init__(self, x, steps):
        self.x = x          # 当前所在位置
        self.steps = steps  # 从起点 N 到当前位置 x 所需要的步数


MAXN = 100000

# 输入农夫起点 N 和牛的位置 K
N, K = map(int, input().split())

# 创建队列，相当于 BFS 中的 Open 表
q = collections.deque()

# visited[i] 表示位置 i 是否已经访问过
# 用于判重，避免反复访问同一个位置
visited = [False] * (MAXN + 10)

# 将起点 N 加入队列，起点步数为 0
q.append(Step(N, 0))

# 标记起点已经访问过
visited[N] = True


# 只要队列不为空，就继续 BFS
while len(q) > 0:
    # 取出队首元素
    s = q.popleft()

    # 如果当前位置已经是目标位置 K，输出步数并结束
    if s.x == K:
        print(s.steps)
        break

    # 情况 1：从当前位置 x 走到 x - 1
    if s.x - 1 >= 0 and not visited[s.x - 1]:
        q.append(Step(s.x - 1, s.steps + 1))
        visited[s.x - 1] = True

    # 情况 2：从当前位置 x 走到 x + 1
    if s.x + 1 <= MAXN and not visited[s.x + 1]:
        q.append(Step(s.x + 1, s.steps + 1))
        visited[s.x + 1] = True

    # 情况 3：从当前位置 x 走到 2 * x
    if s.x * 2 <= MAXN and not visited[s.x * 2]:
        q.append(Step(s.x * 2, s.steps + 1))
        visited[s.x * 2] = True
```

### 迷宫问题

【问题】
定义一个矩阵： 
0 1 0 0 0 
0 1 0 1 0 
0 0 0 0 0 
0 1 1 1 0 
0 0 0 1 0 

它表示一个迷宫，其中的1表示墙壁，0表示可以走的路，只能横着走或竖着走，不能斜着走，要求编程序找出从左上角到右下角的最短路线。

【解题思路】
1. 基础广搜。先将起始位置入队列
2. 每次从队列拿出一个元素，扩展其相邻的4个元素入队列（要用二维标志列表判重），直到队头元素为终点为止。队列里的元素记录了指向父顶点（上一步）的指针
> 队列元素：(r,c,father)
> r,c:  顶点的坐标
> father : 父顶点在队列中的下标(从a走到b,则a是b的父顶点)
> 判重的二维列表：flags[i][j]表示 (i,j)那个位置是否走过，即是否入过队列

page78

### 迷宫变形问题

【问题】给定一个二维网格地图，地图中的每个位置均可移动，但部分位置为特殊障碍区域。一个人在地图上从起点出发，每次只能向上、下、左、右四个方向移动一格，每移动一格花费 1 单位时间。该人拥有有限次数的特殊能力，可以消除障碍并进入障碍区域，每次进入障碍区域会消耗一次能力次数；当能力次数耗尽后，将无法再进入障碍区域。已知地图、起点、终点以及可使用的能力次数，求从起点到终点所需的最短时间。

【解题思路】解题时，将每个状态定义为当前位置和剩余能力次数的组合，即 ((r, c, k))，其中 (r) 和 (c) 表示当前所在的行和列，(k) 表示当前还剩多少次消除障碍的机会。搜索从起点状态开始，使用广度优先搜索逐层扩展，每次可以向上下左右四个方向移动。如果下一个位置是普通位置，则可以直接进入，状态中的 (k) 不变；如果下一个位置是障碍位置，则只有在 (k>0) 时才能进入，并将 (k) 减 1。由于同一个位置在剩余能力次数不同时代表不同状态，因此判重时不能只记录位置，而应记录 ((r,c,k)) 是否已经访问过。BFS 第一次到达终点时，对应的移动次数就是最短时间。

【问题】给定一个二维迷宫地图，地图中的每个位置可能是可通行区域、不可通过的障碍区域，或带有额外代价的特殊区域。一个人从起点出发，需要移动到终点位置，每次只能向上、下、左、右四个方向移动一格。进入普通可通行区域需要花费 1 单位时间，而进入特殊区域时，除了移动所需时间外，还需要额外支付一定代价。障碍区域无法进入。求从起点到终点所需的最少时间。

【解题思路】
1. 定义搜索状态：
   1. (r, c, kill, t)
   2. r, c：当前位置的行和列；kill：是否已经杀死过守卫；t：到达当前位置所花费的时间
2. 使用 BFS 逐层搜索
3. 分类讨论下一格的情况
   1. 下一格是墙壁 #，墙壁不能进入，因此直接跳过，不加入队列。
   2. 下一格是普通道路 @ 或终点 a，可以直接进入，时间增加 1，kill 状态不变：
   3. 下一格是守卫 x，且 kill = 0，说明还没有杀死过守卫，因此可以进入该格并杀死守卫。移动一步花 1 分钟，杀死守卫额外花 1 分钟，所以总时间增加 2：
   4. 下一格是守卫 x，且 kill = 1，之后再次遇到守卫时，守卫已经可以视为可通过状态。此时只需要移动一步，时间增加 1：
4. 判重数组
   1. int flag[M][N][2];
   2. flag[r][c][0]表示在坐标(r,c)，尚未杀死守卫的情况
   3. flag[r][c][1]表示在坐标(r,c)，已经杀死守卫的情况

【解题思路二】
由于该问题中不同位置的移动代价并不相同：进入普通位置只需要花费 1 单位时间，而进入守卫所在位置除了移动时间外还需要额外花费 1 单位时间，因此不同路径之间的总代价不再仅由“步数”决定，普通 BFS 按层扩展的方法已经无法保证第一次到达终点时得到的就是最优解。为了解决这一问题，可以将队列中的状态定义为 ((r,c,steps))，其中 (r,c) 表示当前位置坐标，`steps` 表示到达该位置所花费的总时间。当扩展到普通位置时，总代价增加 1；当扩展到守卫位置时，总代价增加 2。由于搜索过程中必须始终优先扩展总代价较小的状态，因此普通先进先出的队列需要改为优先队列，使得当前总代价最小的状态始终位于队首并优先出队。这样才能保证搜索过程始终按照最小总代价进行扩展，从而正确求得从起点到终点的最短时间。本质上，该问题已经从普通 BFS 转化为了带权最短路径问题，其思想与 Dijkstra 算法一致。

【问题】给定一个二维迷宫地图，地图中的每个位置可能是普通道路、墙壁、守卫、起点、终点或带有钥匙的道路。一个人从起点出发，需要移动到终点；每次只能向上、下、左、右四个方向移动一格，每移动一格花费 1 单位时间。墙壁不能进入；遇到守卫时，必须额外花费 1 单位时间将其处理后才能继续前进。地图上存在若干种钥匙，必须按照编号顺序依次获取：只有已经拥有第 (k-1) 种钥匙时，才能获取第 (k) 种钥匙；未满足条件时，经过有钥匙的位置也不能获得该钥匙。到达终点时，必须至少获得每一种钥匙各一把，才算完成任务。求从起点完成任务并到达终点所需的最少时间。

【解题思路】
1. 状态设计
   (r, c, keys, fighted, steps, layout)
   r, c：当前位置
    keys：当前已经拿到第几种钥匙
    fighted：当前位置的守卫是否已经处理过
    steps：当前已经花费的总时间
    layout：当前迷宫中守卫的状态
2. 判重数组设计
   flags[r][c][k][x][f]
   在位置 (r,c)
    已经拿到 k 种钥匙
    守卫局面为 x
    当前格子的守卫处理状态为 f
3. 扩展规则
   1. 如果下一格是墙壁，不能进入；
   2. 如果下一格是普通道路，可以进入，steps + 1；
   3. 如果下一格是钥匙，判断是否满足拿钥匙顺序，若满足则更新 keys；
   4. 如果下一格是守卫，判断该守卫是否已经被打过：
      1. 如果已经被打过，可以直接进入，steps + 1；
      2. 如果还没被打过，进入后需要额外处理，时间增加更多，并更新守卫局面。
4. 当到达终点，并且已经收集完所有需要的钥匙时，任务完成。

# 图遍历的应用

### 骑士周游问题

【问题】在一个国际象棋棋盘上，一个棋子“马”（骑士），按照“马走日”的规则，从一个格子出发，要走遍所有棋盘格恰好一次。把一个这样的走棋序列称为一次“周游”

【解决思路】
1. 首先将合法走棋次序表示为一个图
   将棋盘格作为顶点
    按照“马走日”规则的走棋步骤作为连接边，建立每一个棋盘格的所有合法走棋步骤能够到达的棋盘格关系图

```python
def genLegalMoves(x, y, bdsize):
    # 用来保存所有合法的下一步位置
    newMoves = []

    # 马可以走的 8 个方向
    # 每一个元组表示 (x方向变化量, y方向变化量)
    moveOffsets = [
        (-1, -2), (-1, 2),
        (-2, 1), (-2, -1),
        (1, -2), (1, 2),
        (2, -1), (2, 1)
    ]

    # 遍历马的 8 种可能移动方式
    for i in moveOffsets:
        # 计算移动后的新坐标
        newX = x + i[0]
        newY = y + i[1]

        # 判断新坐标是否仍然在棋盘范围内
        if legalCoord(newX, bdsize) and legalCoord(newY, bdsize):
            # 如果合法，就加入结果列表
            newMoves.append((newX, newY))

    # 返回所有合法移动位置
    return newMoves


def legalCoord(x, bdsize):
    # 判断坐标 x 是否在棋盘范围内
    # 合法范围是：0 <= x < bdsize
    if x >= 0 and x < bdsize:
        return True
    else:
        return False
```

```python
def knightGraph(bdsize):
    # 创建一个空图，用来表示整个棋盘上“马”的移动关系
    ktGraph = Graph()

    # 遍历棋盘中的每一行
    for row in range(bdsize):

        # 遍历棋盘中的每一列
        for col in range(bdsize):

            # 将二维坐标 (row, col) 转换成一维顶点编号
            nodeId = posToNodeId(row, col, bdsize)

            # 计算当前位置 (row, col) 上马可以走到的所有合法位置
            newPositions = genLegalMoves(row, col, bdsize)

            # 遍历所有合法的新位置
            for e in newPositions:

                # 将新位置的二维坐标转换成一维顶点编号
                nid = posToNodeId(e[0], e[1], bdsize)

                # 在图中添加一条边：
                # 表示马可以从 nodeId 这个位置一步走到 nid 这个位置
                ktGraph.addEdge(nodeId, nid)

    # 返回构建好的马走日图
    return ktGraph


def posToNodeId(row, col, bdsize):
    # 将二维坐标 (row, col) 转换成一维编号
    # 例如 bdsize = 8 时：
    # (0,0) -> 0
    # (0,1) -> 1
    # ...
    # (1,0) -> 8
    # 公式：行号 * 棋盘宽度 + 列号
    return row * bdsize + col
```

2. 采用图搜索算法搜寻一个长度为（行×列-1）的路径，路径上包含每个顶点恰一次

需要通过深度优先搜索进行遍历：
   - 深度优先搜索是沿着树的单支尽量深入向下搜索，如果到无法继续的程度还未找到问题解，就回溯上一层再搜索下一支
   - 如果沿着单支深入搜索到无法继续（所有合法移动都已经被走过了）时路径长度还没有达到预定值（8×8棋盘为63），那么就清除颜色标记，返回到上一层换一个分支继续深入搜索
   - 引入一个栈来记录路径，并实施返回上一层的回溯操作

```python
def knightTour(n, path, u, limit):
    # 将当前顶点 u 标记为 gray
    # gray 表示：这个点已经在当前路径中，不能重复访问
    u.setColor('gray')

    # 把当前顶点 u 加入路径
    path.append(u)

    # 如果当前路径长度还没有达到目标长度，就继续搜索
    if n < limit:

        # 取出当前顶点 u 的所有邻接点
        # 对于骑士周游问题来说，就是马从当前位置下一步能跳到的位置
        nbrList = list(u.getConnections())

        # i 用来遍历邻接点列表
        i = 0

        # done 表示是否已经找到一条完整路径
        done = False

        # 只要还有邻接点没有尝试，并且还没有找到完整路径，就继续尝试
        while i < len(nbrList) and not done:

            # 如果这个邻接点还没有被访问过
            if nbrList[i].getColor() == 'white':

                # 递归搜索这个邻接点
                # n + 1 表示路径长度增加 1
                done = knightTour(n + 1, path, nbrList[i], limit)

            # 无论当前邻接点是否成功，都尝试下一个邻接点
            i = i + 1

        # 如果所有邻接点都尝试完了，仍然没有找到完整路径
        # 说明从当前点继续走不通，需要回溯
        if not done:
            # 从路径中移除当前顶点
            path.pop()

            # 把当前顶点重新标记为 white
            # 表示它可以在其他路径尝试中再次被访问
            u.setColor('white')

    else:
        # 如果 n 已经达到 limit
        # 说明已经找到一条覆盖目标数量顶点的路径
        done = True

    # 返回是否成功找到完整路径
    return done
```
