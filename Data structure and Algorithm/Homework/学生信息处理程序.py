# 描述
# 实现一个学生信息处理程序，计算一个学生的平均成绩。

# 补充下列程序中的 Student 类以实现上述功能。

# 输入
# 输入数据为一行，包括：
# 姓名,年龄,多门课程的成绩
# 用空格分开
# 输出
# 见样例格式
# 平均成绩输出两位小数

class Student():
    def __init__(self):
        self.name = ""
        self.age = 0
        self.scores = 0
        self.average = 0.00
        self.count =0
    def input(self):
        data = input().split(" ")
        self.name = data[0]
        self.age = data[1]
        for i in range(2,len(data)):
            self.scores +=int(data[i])
            self.count +=1
    def calculate(self):
        self.average = float(self.scores/self.count)
    def output(self):
        print(f"name: {self.name}") #这里要认真看看
        print(f"age: {self.age}")
        print(f"avg score: {self.average:.2f}") #这里要认真看

def main():
    student = Student()
    student.input()
    student.calculate()
    student.output()

if __name__ == "__main__":
    main()