# Maze
OBSTACLE = '+'
TRIED = '.'
DEAD_END = '-'
PART_OF_PATH = 'O'
class Maze:
    def __init__(self, mazeData):  # 修改：现在接收二维列表而不是文件名
        rowsInMaze = 0
        self.columnsInMaze = 0
        self.mazelist = []

        for row in mazeData:  # 修改：直接遍历传入的二维列表
            rowList = []
            col = 0

            for ch in row:  # 修改：列表行里已经是字符，不再按文件字符串处理
                rowList.append(ch)

                if ch == 'S':
                    self.startRow = rowsInMaze
                    self.startCol = col

                col = col + 1

            rowsInMaze = rowsInMaze + 1
            self.mazelist.append(rowList)
            self.columnsInMaze = len(rowList)
        self.rowsInMaze = rowsInMaze  # 修改：保存行数，供 isExit 使用
    def __getitem__(self, idx):
        return self.mazelist[idx]

    # 更新位置（标记路径）
    def updatePosition(self, row, col, val=None):
        if val is not None:  # 修改：避免传入假值时无法更新
            self.mazelist[row][col] = val

    # 判断是否出口（边界）
    def isExit(self, row, col):
        return row == 0 or row == self.rowsInMaze - 1 or \
               col == 0 or col == self.columnsInMaze - 1

    # 打印迷宫
    def drawMaze(self):
        for row in self.mazelist:
            print(" ".join(row))
        print()

def searchFrom(maze, startRow, startColumn):
    maze.updatePosition(startRow, startColumn)
    if maze[startRow][startColumn] == OBSTACLE:
        return False
    if maze[startRow][startColumn] == TRIED or \
        maze[startRow][startColumn] == DEAD_END:
        return False
    if maze.isExit(startRow, startColumn):
        maze.updatePosition(startRow, startColumn, PART_OF_PATH)
        return True
    maze.updatePosition(startRow, startColumn, TRIED)
    
    found = searchFrom(maze, startRow+1, startColumn) or \
            searchFrom(maze, startRow-1, startColumn) or \
            searchFrom(maze, startRow, startColumn+1) or \
            searchFrom(maze, startRow, startColumn-1)
    if found:
        maze.updatePosition(startRow, startColumn, PART_OF_PATH)
    else:
        maze.updatePosition(startRow, startColumn, DEAD_END)  # 修改：死路应标记为 DEAD_END
    return found

mazeData = [
    ['+', '+', '+', '+', '+', '+', '+'],
    ['+', 'S', ' ', ' ', ' ', ' ', '+'],
    ['+', ' ', '+', ' ', '+', ' ', '+'],
    ['+', ' ', '+', ' ', ' ', ' ', ' '],
    ['+', '+', '+', '+', '+', '+', '+'],
]

maze = Maze(mazeData)

print("原始迷宫：")
maze.drawMaze()

found = searchFrom(maze, maze.startRow, maze.startCol)

print("是否找到出口：", found)
print("搜索后的迷宫：")
maze.drawMaze()
