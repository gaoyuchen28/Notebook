import collections

def bfs(maze, M, N, sx,sy,K):

    # 创建队列，相当于 BFS 中的 Open 表
    q = collections.deque()

    # visited[i] 表示位置 i 是否已经访问过
    # 用于判重，避免反复访问同一个位置
    visited = [[[False] * K for i in range(N)]for j in range(M)]

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    q.append((sx,sy,0))

    visited[sx][sy][0] = True

    # 只要队列不为空，就继续 BFS
    while len(q) > 0:
        # 取出队首元素
        x,y,dis = q.popleft()

        # 如果当前位置已经是目标位置 K，输出步数并结束
        if maze[x][y] == 'E':
            return dis
        
        for dx, dy in directions:
            nx = x + dx
            ny = y + dy

            if nx < 0 or nx >= M or ny < 0 or ny >= N:
                continue

            if visited[nx][ny][(dis+1)%K] == True:
                continue

            if maze[nx][ny] == '#' and (dis+1)%K != 0:
                continue

            visited[nx][ny][(dis+1)%K] = True

            q.append((nx,ny,dis+1))
    return -1

n = int(input())

while n:
    M,N,K = map(int, input().split())
    maze = []
    for i in range(M):
        row = input().strip()
        maze.append(row)

        for j in range(N):
            if row[j] == 'S':
                sx, sy = i, j

    ans= bfs(maze, M, N, sx, sy,K)
    if ans == -1:
        print("Oop!")
    else:
        print(ans)
    n-=1