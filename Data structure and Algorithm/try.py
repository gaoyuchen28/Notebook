# 编写一个程序来计算一个人的BMI。

# BMI计算公式：

# BMI = 体重/身高^2
# 输入一个浮点数表示人的体重（单位：公斤），并把它赋给体重指标weight。
# 输入一个浮点数表示人的身高（以米为单位），赋予其分配给身高指标height。
# 使用公式来计算BMI，并输出。

weight = float(input())
height = float(input())
print(weight/(height*height))

