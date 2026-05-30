# 先建一个graph

import sys

import heapq

class Vertex:

    def __init__(self, key):
        self.id = key

        # connectedTo 用来保存当前顶点的所有邻居
        # 格式：
        # {
        #     邻居顶点对象1: 边权1,
        #     邻居顶点对象2: 边权2
        # }
        self.connectedTo = {}

        self.color = 'white'
        self.distance = float('inf')
        self.pred = None

    def addNeighbor(self, nbr, weight=0):
        # 添加一条从 self 到 nbr 的边，权重为 weight
        self.connectedTo[nbr] = weight

    def getConnections(self):
        # 返回所有邻居顶点对象
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getWeight(self, nbr):
        # 返回 self 到 nbr 这条边的权重
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
        # vertList 保存所有顶点
        # 格式：
        # {
        #     顶点编号: 顶点对象
        # }
        self.vertList = {}

        # 顶点数量
        self.numVertices = 0

    def addVertex(self, key):
        # 添加一个新顶点
        self.numVertices += 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self, key):
        # 根据编号获取顶点对象
        if key in self.vertList:
            return self.vertList[key]
        else:
            return None

    def __contains__(self, key):
        # 支持写法：if key in graph
        return key in self.vertList

    def addEdge(self, f, t, cost=0):
        # 如果起点 f 不存在，就先加入图中
        if f not in self.vertList:
            self.addVertex(f)

        # 如果终点 t 不存在，也先加入图中
        if t not in self.vertList:
            self.addVertex(t)

        # 添加一条从 f 到 t 的边
        self.vertList[f].addNeighbor(self.vertList[t], cost)

    def addUndirectedEdge(self, f, t, cost=0):
        # 无向图要加两条边
        # f -> t
        # t -> f
        self.addEdge(f, t, cost)
        self.addEdge(t, f, cost)

    def getVertices(self):
        # 返回所有顶点编号
        return self.vertList.keys()

    def __iter__(self):
        # 支持写法：for v in graph
        # 每次返回的是 Vertex 对象
        return iter(self.vertList.values())

def dijkstra(aGraph, start):
    # 初始化所有点
    for v in aGraph:
        v.setDistance(float('inf'))
        v.setPred(None)

    # 起点距离设为 0
    start.setDistance(0)

    # 小根堆中存放：
    # (当前距离, 顶点编号, 顶点对象)
    heap = []
    heapq.heappush(heap, (0, start.getId(), start))

    while heap:
        currentDist, _, currentVert = heapq.heappop(heap)

        # 如果这个距离不是最新的，跳过
        if currentDist != currentVert.getDistance():
            continue

        # 遍历当前顶点的所有邻居
        for nextVert in currentVert.getConnections():

            # 新路径长度 = 起点到 currentVert 的距离 + currentVert 到 nextVert 的边权
            newDist = currentVert.getDistance() + currentVert.getWeight(nextVert)

            # 如果新路径更短，就更新
            if newDist < nextVert.getDistance():
                nextVert.setDistance(newDist)
                nextVert.setPred(currentVert)

                heapq.heappush(heap, (newDist, nextVert.getId(), nextVert))

def dfs_count_routes(u, memo):
    if u.getId() == 2:
        return 1

    if memo[u.getId()] != -1:
        return memo[u.getId()]

    ans = 0

    for v in u.getConnections():
        if v.getDistance() < u.getDistance():
            ans += dfs_count_routes(v, memo)

    memo[u.getId()] = ans
    return ans

sys.setrecursionlimit(1000000)

while True:
    line = sys.stdin.readline().strip()

    if line == "0":
        break

    n, m = map(int, line.split())

    G = Graph()

    # 先创建 1 到 n 的所有顶点
    for i in range(1, n + 1):
        G.addVertex(i)

    for _ in range(m):
        a, b, d = map(int, sys.stdin.readline().split())
        G.addUndirectedEdge(a, b, d)
    
    dijkstra(G, G.getVertex(2))

    memo = [-1] * (n + 1)

    print(dfs_count_routes(G.getVertex(1), memo))
    

