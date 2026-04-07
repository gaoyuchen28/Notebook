# 递归可视化之二叉树

import turtle
t = turtle.Turtle()

def Tree(len):
    if len > 1 :
        t.forward(len)
        t.right(20)
        Tree(len - 5)
        t.left(40)
        Tree(len - 5)
        t.right(20)
        t.backward(len)
t.left(90) # 初始方向默认朝右（0°）,将海龟旋转 90°，也就是 向上。

Tree(25)
t.done()