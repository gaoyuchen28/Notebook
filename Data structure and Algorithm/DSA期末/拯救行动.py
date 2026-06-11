import heapq


n = int(input())

for _ in range(n):

    maze = []

    M,N = map(int,input().split())

    # 找起点和终点
    for i in range(M):
        row = input().strip()
        maze.append(row)
        for j in range(N):
            if maze[i][j] == 'r':
                sx, sy = i, j
            elif maze[i][j] == 'a':
                ex, ey = i, j

    # 优先队列 (steps, x, y)
    pq = []
    heapq.heappush(pq, (0, sx, sy))

    # 记录每个格子最短时间
    dist = [[float('inf')] * N for _ in range(M)]
    dist[sx][sy] = 0

    directions = [(-1,0), (1,0), (0,-1), (0,1)]

    found = False

    while pq:
        steps, x, y = heapq.heappop(pq)

        # 如果当前步数比记录的还大，说明已经有更短路径了
        if steps > dist[x][y]:
            continue

        # 到达终点
        if x == ex and y == ey:
            print(steps)
            found = True
            break

        # 扩展邻居
        for dx, dy in directions:
            nx = x + dx
            ny = y + dy

            if 0 <= nx < M and 0 <= ny < N:
                if maze[nx][ny] == '#':
                    continue

                # 走普通格子: +1, 守卫: +2
                if maze[nx][ny] == 'x':
                    nt = steps + 2
                else:
                    nt = steps + 1

                # 如果这条路径更短，就加入队列
                if nt < dist[nx][ny]:
                    dist[nx][ny] = nt
                    heapq.heappush(pq, (nt, nx, ny))

    if not found:
        print("Impossible")