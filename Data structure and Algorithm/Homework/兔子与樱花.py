class Vertex:
    def __init__(self, key, value):
        self.id = key
        self.name = value
        self.connectedTo = {}
        self.distance = float('inf')
        self.pred = None
 
    def addNeighbor(self, nbr, weight=0):
        self.connectedTo[nbr] = weight

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.name

    def getWeight(self, nbr):
        return self.connectedTo[nbr]

    def getDistance(self):
        return self.distance

    def setDistance(self, distance):
        self.distance = distance

    def getPred(self):
        return self.pred

    def setPred(self, pred):
        self.pred = pred


class Graph:
    def __init__(self):
        self.vertList = {}
        self.nameMap = {}
        self.numVertices = 0

    def addVertex(self, key, name):
        newVertex = Vertex(key, name)
        self.vertList[key] = newVertex
        self.nameMap[name] = newVertex
        self.numVertices += 1
        return newVertex

    def getVertexByName(self, name):
        return self.nameMap.get(name, None)

    def addEdgeByName(self, f_name, t_name, cost=0):
        f = self.getVertexByName(f_name)
        t = self.getVertexByName(t_name)
        f.addNeighbor(t, cost)

    def __iter__(self):
        return iter(self.vertList.values())

    def reset(self):
        for v in self:
            v.setDistance(float('inf'))
            v.setPred(None)

def dijkstra_no_pq(aGraph, start):
    aGraph.reset()
    # 设置起点到自己的距离为 0
    start.setDistance(0)

    # 已经确定最短路径的顶点集合
    visited = set()

    # 只要还有未访问顶点，就继续循环
    while len(visited) < aGraph.numVertices:

        # 在所有未访问顶点中，找到距离起点最小的顶点
        currentVert = None
        currentDist = float('inf')
        for v in aGraph:
            if v not in visited and v.getDistance() < currentDist:
                currentDist = v.getDistance()
                currentVert = v

        # 如果没有可访问顶点，说明剩余顶点不可达，结束循环
        if currentVert is None:
            break

        # 把当前顶点加入已访问集合
        visited.add(currentVert)

        # 遍历 currentVert 的所有邻接点
        for nextVert in currentVert.getConnections():

            # 计算通过 currentVert 到 nextVert 的新距离
            newDist = currentVert.getDistance() + currentVert.getWeight(nextVert)

            # 如果新距离更短，更新 nextVert 的最短距离
            if newDist < nextVert.getDistance():
                nextVert.setDistance(newDist)
                nextVert.setPred(currentVert)
def getPath(end):
    path = []

    current = end
    while current is not None:
        path.append(current)
        current = current.getPred()

    path.reverse()
    return path

def printPath(path):
    ans = path[0].getId()

    for i in range(1, len(path)):
        weight = path[i-1].getWeight(path[i])
        ans += "->(" + str(weight) + ")->" + path[i].getId()

    print(ans)

g = Graph()
n1 = int(input())

for i in range(n1):
    name = input().strip()
    g.addVertex(i, name)

n2 = int(input())
for _ in range(n2):
    f_name, t_name, weight = input().split()
    weight = int(weight)
    g.addEdgeByName(f_name, t_name, weight)
    g.addEdgeByName(t_name, f_name, weight)

n3 = int(input())
for _ in range(n3):
    s_name, e_name = input().split()
    s = g.getVertexByName(s_name)
    e = g.getVertexByName(e_name)
    dijkstra_no_pq(g, s)
    p = getPath(e)
    printPath(p)
