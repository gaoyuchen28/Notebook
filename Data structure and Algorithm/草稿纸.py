# 骑士周游问题

# --------基本定义——-------
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

# --------建图--------
def legalCoord(x, bsize):
    if x >=0 and x < bsize:
        return True
    else:
        return False
    
def genLegalMoves(x, y , bsize):
    newMoves = []
    moves = [
        (-1,-2),
        (1,-2),
        (-1,2),
        (1,-2),
        (2,-1),
        (2,1),
        (-2,1),
        (-2,-1)
    ]
    for i in moves:
        newx = x + i[0]
        newy = y + i[1]
        if legalCoord(newx) and legalCoord(newy):
            newMoves.append((newx,newy))
    return newMoves
    
def tonumber(row, col, bsize):
    return row*bsize + col

def graph(bsize):
    ktGraph = Graph()
    for row in range(bsize):
        for col in range(bsize):
            Id = tonumber(row,col,bsize)
            newMove = genLegalMoves(row,col,bsize):
            for i in newMove:
                id = tonumber(i[0],i[1],bsize)
                ktGraph.addEdge(Id,id)
    return ktGraph

# -------深度优先搜索-------

def knight(n,path,u,limit):
    u.setColor('gray')
    path.append(u)

    if n < limit:
        nrlist = list(u.getConnections())
        i = 0
        done = False

        while i < len(nrlist) and not done:
            if nrlist[i].getColor() == 'white':
                done = knight(n+1,path,nrlist[i],limit)
            i = i+1
        if not done:
            path.pop()
            u.setColor('white')
    else:
        done = True

    return done