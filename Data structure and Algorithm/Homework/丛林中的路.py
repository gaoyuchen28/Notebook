import heapq
import sys

class Graph_adj_mat:

    def __init__(self, num_vertices):
        self.numVertices = num_vertices
        self.adj_matrix = [[0] * num_vertices for _ in range(num_vertices)]

    def addEdge(self, v1, v2, weight):
        self.adj_matrix[v1][v2] = weight
        self.adj_matrix[v2][v1] = weight   # 无向图

    def get_neighbors(self, idx):
        neighbors = []
        for j in range(self.numVertices):
            if self.adj_matrix[idx][j] != 0:
                neighbors.append(j)
        return neighbors

    def getWeight(self, v1, v2):
        return self.adj_matrix[v1][v2]


def prim(G, start):
    # pq 中存的是：边权、顶点编号
    pq = []

    # visited[i] 表示顶点 i 是否已经加入最小生成树
    visited = [False] * G.numVertices

    # 从起点 start 开始，代价为 0
    heapq.heappush(pq, (0, start))

    totalCost = 0

    while pq:
        # 取出当前边权最小的顶点
        currentCost, currentVert = heapq.heappop(pq)

        # 如果这个点已经加入生成树，就跳过
        if visited[currentVert]:
            continue

        # 把当前点加入最小生成树
        visited[currentVert] = True

        # 加上连接这个点的边权
        totalCost += currentCost

        # 遍历 currentVert 的所有邻居
        for nextVert in G.get_neighbors(currentVert):
            if not visited[nextVert]:
                newCost = G.getWeight(currentVert, nextVert)
                heapq.heappush(pq, (newCost, nextVert))

    return totalCost

while True:
    n = int(input())
    if n == 0:
        break

    G = Graph_adj_mat(n)

    for _ in range(n - 1):
        data = input().split()

        start = data[0]
        k = int(data[1])

        v1 = ord(start) - ord('A')

        index = 2
        for i in range(k):
            end = data[index]
            weight = int(data[index + 1])

            v2 = ord(end) - ord('A')

            G.addEdge(v1, v2, weight)

            index += 2
    m = prim(G,0)
    print(m)