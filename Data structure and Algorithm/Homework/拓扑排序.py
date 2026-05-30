# 这道题的重点是因为他需要在距离一致的时候用较小的序号插入，所以需要用堆排序

import heapq


def topoSort(G, n):
    # inDegree[i] 表示顶点 i 的入度
    # 这里顶点编号从 1 到 n，所以数组开 n + 1
    inDegree = [0] * (n + 1)

    # 统计每个顶点的入度
    for u in range(1, n + 1):
        for v in G[u]:
            inDegree[v] += 1

    # 小根堆，用来存当前所有入度为 0 的顶点
    # heapq 每次会弹出编号最小的顶点
    heap = []

    # 把一开始所有入度为 0 的顶点加入堆
    for i in range(1, n + 1):
        if inDegree[i] == 0:
            heapq.heappush(heap, i)

    # 保存拓扑排序结果
    seq = []

    # 只要堆不为空，就继续取点
    while heap:
        # 取出当前所有入度为 0 的点中编号最小的那个
        u = heapq.heappop(heap)

        # 加入拓扑序列
        seq.append(u)

        # 删除 u 指向的所有边
        for v in G[u]:
            inDegree[v] -= 1

            # 如果 v 的入度变成 0，说明它可以被选择了
            if inDegree[v] == 0:
                heapq.heappush(heap, v)

    # 如果没有输出所有顶点，说明图中有环
    if len(seq) != n:
        return None

    return seq


# 读入顶点数和弧数
n, a = map(int, input().split())

# G[u] 存放所有从 u 出发的点
# 顶点编号从 1 到 n
G = [[] for _ in range(n + 1)]

# 读入 a 条有向边
for _ in range(a):
    u, v = map(int, input().split())
    G[u].append(v)

# 求拓扑排序
ans = topoSort(G, n)

# 按题目要求输出 v1 v3 v2 ...
if ans is not None:
    print(" ".join("v" + str(x) for x in ans))