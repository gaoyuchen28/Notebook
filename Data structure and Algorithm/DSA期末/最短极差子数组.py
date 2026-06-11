from collections import deque

n = int(input())
nums = list(map(int, input().split()))
k = int(input())

min_len = n + 1
left = 0

max_q = deque()  # 单调递减队列
min_q = deque()  # 单调递增队列

for right in range(n):
    # 维护最大值队列
    while max_q and nums[right] > nums[max_q[-1]]:
        max_q.pop()
    max_q.append(right)

    # 维护最小值队列
    while min_q and nums[right] < nums[min_q[-1]]:
        min_q.pop()
    min_q.append(right)

    # 缩小窗口
    while max_q and min_q and nums[max_q[0]] - nums[min_q[0]] >= k:
        min_len = min(min_len, right - left + 1)
        if max_q[0] == left:
            max_q.popleft()
        if min_q[0] == left:
            min_q.popleft()
        left += 1

print(-1 if min_len == n + 1 else min_len)