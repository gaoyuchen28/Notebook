# 递归可视化之螺旋

import turtle
t = turtle.Turtle()

def L(len):
    if len > 0 :
        t.forward(len)
        t.right(90)
        return L(len-5)

L(100)
t.done()