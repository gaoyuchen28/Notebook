from collections import deque

# 输入
R, C = map(int, input().split())
N, moves = input().split()
N = int(N)
F = int(input())
foods = [tuple(map(int, input().split())) for _ in range(F)]

# 方向映射
dir_map = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

# 初始化蛇
snake = deque([(0, 0)])  # 蛇身体
snake_set = set(snake)   # 用于快速判断撞到自己

food_index = 0
steps = 0

for move in moves:
    head_r, head_c = snake[0]
    dr, dc = dir_map[move]
    new_r, new_c = head_r + dr, head_c + dc
    
    # 检查边界
    if not (0 <= new_r < R and 0 <= new_c < C):
        break  # 撞墙死亡
    
    # 检查自己身体
    new_head = (new_r, new_c)
    tail = snake[-1]
    if new_head in snake_set and new_head != tail:
        break  # 撞自己
    
    # 吃食物
    if food_index < F and new_head == foods[food_index]:
        snake.appendleft(new_head)
        snake_set.add(new_head)
        food_index += 1
        # 尾巴不动
    else:
        # 正常移动
        snake.appendleft(new_head)
        snake_set.add(new_head)
        removed_tail = snake.pop()
        snake_set.remove(removed_tail)
    
    steps += 1

print(steps)

