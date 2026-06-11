from collections import deque

def max_blood_bfs(maze, M, N, sx, sy, B):
    q = deque()
    max_blood = [[-1]*N for _ in range(M)]
    q.append((sx, sy, B))
    max_blood[sx][sy] = B

    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    while q:
        x, y, blood = q.popleft()

        for dx, dy in directions:
            nx, ny = x+dx, y+dy
            if nx<0 or nx>=M or ny<0 or ny>=N:
                continue
            cell = maze[nx][ny]
            if cell == '#':
                continue

            new_blood = blood
            if cell.isdigit():
                dmg = int(cell)
                new_blood -= dmg
                if new_blood <=0:
                    continue

            if new_blood > max_blood[nx][ny]:
                max_blood[nx][ny] = new_blood
                q.append((nx, ny, new_blood))

    # 找到公主位置
    for i in range(M):
        for j in range(N):
            if maze[i][j] == '+':
                return max_blood[i][j] if max_blood[i][j] != -1 else 0

M, N, B = map(int, input().split())
maze = []
sx, sy = -1, -1

for i in range(M):
    row = input().strip()
    maze.append(row)

    for j in range(N):
        if row[j] == '*':
            sx, sy = i, j

print(max_blood_bfs(maze, M, N, sx, sy,B))