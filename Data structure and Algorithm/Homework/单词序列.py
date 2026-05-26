from collections import deque

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
        return iter(self.vertList.values())


def buildGraph(wordlist):
    d = {}
    g = Graph()

    # 第一步：建立 bucket
    # bucket 的作用：把“只差一个字母”的单词放到同一组里
    for word in wordlist:

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

def bfs(g, start):
    # 将起始顶点到自己的距离设置为 0
    start.setDistance(0)

    # 起始顶点没有前驱节点
    start.setPred(None)

    start.setColor('gray')

    # 创建一个队列，用于 BFS 的“先进先出”遍历
    vertQueue = deque()

    # 先把起始顶点放入队列
    vertQueue.append(start)

    # 只要队列不为空，就继续搜索
    while len(vertQueue) > 0:

        # 取出队首顶点，作为当前正在访问的顶点
        currentVert = vertQueue.popleft()

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
                vertQueue.append(nbr)

        # 当前顶点的所有邻居都检查完后，将其标记为 black
        # black 表示这个顶点已经彻底处理完成
        currentVert.setColor('black')

start, end = input().split()
wordlist = input().split()

wordlist.append(start)
wordlist.append(end)

wordlist = list(set(wordlist))

g = buildGraph(wordlist)

s = g.getVertex(start)
e = g.getVertex(end)

if s is None or e is None:
    print(0)
else:
    bfs(g, s)

    if e.getDistance() == float('inf'):
        print(0)
    else:
        print(e.getDistance() + 1)