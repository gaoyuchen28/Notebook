import heapq

def optimal_binary_tree(weights):
    # 1. 开始 n 个结点位于集合 S
    heapq.heapify(weights)

    total_wpl = 0

    # 2. 每次取出两个权值最小的结点
    while len(weights) > 1:
        n1 = heapq.heappop(weights)
        n2 = heapq.heappop(weights)

        # 构造新结点 r
        r = n1 + n2

        # 这一次合并产生的代价
        total_wpl += r

        # 将 r 加回集合 S
        heapq.heappush(weights, r)

    # 3. total_wpl 就是最小 WPL
    return total_wpl

t = int(input())
for _ in range(t):
    n = int(input())
    weights = list(map(int, input().split()))  # 这一行读入 n 个权值
    print(optimal_binary_tree(weights))