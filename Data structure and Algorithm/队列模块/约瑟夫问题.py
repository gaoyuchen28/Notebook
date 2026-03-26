def hot_potato(name_list, num):
    queue = []
    for name in name_list:
        queue.append(name)
    while len(queue) > 1:
        for i in range(num):
            queue.append(queue.pop(0))
        queue.pop(0)
    return queue.pop()

n, m = map(int, input().split())
if {n,m} == {0}: 
    print("False")
monkey = [i for i in range(1, n+1)]
print(hot_potato(monkey, m-1)) # 关键点：击鼓传花次数是 m-1