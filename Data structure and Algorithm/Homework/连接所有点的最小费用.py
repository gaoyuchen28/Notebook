import ast

import heapq
import sys


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
    
    def setDistance(self, dist):
        self.distance = dist

    def getDistance(self):
        return self.distance

    def setPred(self, pred):
        self.pred = pred

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


def prim(G, start):
    # heapq 实现的优先队列
    pq = []

    # 记录哪些顶点已经加入最小生成树
    inTree = set()

    # 初始化所有顶点
    for v in G:
        v.setDistance(sys.maxsize)
        v.setPred(None)

    # 起点距离设为 0
    start.setDistance(0)

    # 修改：heapq 里面放三元组
    # (当前最小边权, 顶点编号, 顶点对象)
    # 加顶点编号是为了防止两个 Vertex 对象不能比较而 Runtime Error
    heapq.heappush(pq, (0, start.getId(), start))

    totalCost = 0

    while pq:
        # 相当于 pq.delMin()
        currentDistance, currentId, currentVert = heapq.heappop(pq)

        # 修改：如果这个点已经加入生成树，就跳过
        # 因为 heapq 没有 decreaseKey，旧的较大距离可能还留在堆里
        if currentVert in inTree:
            continue

        # 当前顶点正式加入最小生成树
        inTree.add(currentVert)

        # 当前边权加入答案
        totalCost += currentDistance

        # 遍历邻接点
        for nextVert in currentVert.getConnections():

            newCost = currentVert.getWeight(nextVert)

            # 修改：原来是 if nextVert in pq
            # heapq 不能直接判断某个点是否还在队列中
            # 所以改成判断 nextVert 是否还没加入生成树
            if nextVert not in inTree and newCost < nextVert.getDistance():

                nextVert.setPred(currentVert)

                nextVert.setDistance(newCost)

                # 修改：heapq 没有 decreaseKey
                # 所以直接把新的更小距离重新压入堆
                heapq.heappush(pq, (newCost, nextVert.getId(), nextVert))

    return totalCost



input_str = input().strip()
points = ast.literal_eval(input_str)

g = Graph()

for i in range(len(points)):
    for j in range(i, len(points)):
        w = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
        g.addEdge(i,j,w)
        g.addEdge(j,i,w)

result = prim(g, g.getVertex(0))

print(result)