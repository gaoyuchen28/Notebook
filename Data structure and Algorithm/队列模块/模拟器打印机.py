import random

# --- 基础数据结构：队列 ---
class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []
    
    def enqueue(self, item):
        self.items.insert(0, item)
    
    def dequeue(self):
        return self.items.pop()
    
    def size(self):
        return len(self.items)


# --- 角色 1：打印机 ---
class Printer:
    def __init__(self, ppm):
        self.pagerate = ppm
        self.currentTask = None
        self.timeRemaining = 0 # 当前任务还需要多少秒才能打完

    def tick(self):
        if self.currentTask != None:
            self.timeRemaining = self.timeRemaining - 1
            if self.timeRemaining <= 0:
                self.currentTask = None
    
    def busy(self):
        return self.currentTask is not None
    
    def startNext(self, newtask):
        self.currentTask = newtask
        self.timeRemaining = newtask.getPages()*60/self.pagerate # 计算这个任务需要多少秒才能打完


# --- 角色 2：打印任务 ---
class Task:
    def __init__(self, time):
        self.timestamp = time # 任务产生的时间
        self.pages = random.randrange(1,21)

    def getStamp(self):
        return self.timestamp
    
    def getPages(self):
        return self.pages
    
    def waitTime(self, currenttime):
        return currenttime - self.timestamp

# --- 模拟逻辑核心 ---
def simulation(numSeconds, pagesPerMinute):
    labprinter = Printer(pagesPerMinute)
    printQueue = Queue() # 初始化打印任务队列
    waitingtimes = []

    for currentSecond in range(numSeconds):
        if newPrintTask():
            task = Task(currentSecond)
            printQueue.enqueue(task)

        if (not labprinter.busy()) and not (printQueue.is_empty()):
            newtask = printQueue.dequeue()
            waitingtimes.append(newtask.waitTime(currentSecond))
            labprinter.startNext(newtask)

        labprinter.tick()

    if len(waitingtimes) > 0:
        averageWait = sum(waitingtimes)/len(waitingtimes)
        print("Average Wait %6.2f secs %3d tasks remaining." % (averageWait, printQueue.size()))
    
    else:
        print("No tasks completed.")

# --- 概率生成器 ---
def newPrintTask():
    num = random.randrange(1,181)
    return num == 180


# --- 运行模拟 ---
# 连续运行 10 次模拟，观察在不同随机情况下的平均等待时间
for i in range(10):
    simulation(3600, 10) # 模拟一小时（3600秒），打印速度为 10页/分钟