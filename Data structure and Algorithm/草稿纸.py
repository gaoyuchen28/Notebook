# 谢尔宾斯基三角形

import turtle
t = turtle.Turtle()

def DrawTriangle(point, color):
    t.fillcolor(color)
    t.penup()
    t.goto(point['top'])
    t.pendown()
    t.begin_fill()
    t.goto(point['left'])
    t.goto(point['right'])
    t.goto(point['top'])
    t.end_fill()

def getMid(p1,p2):
    return ((p1[0]+p2[0])/2,(p1[1]+p2[1])/2)

def Triangle(degree, point):
    colormap = ['blue','green']
    DrawTriangle(point, colormap(degree%2))
    if degree>0:
        Triangle(degree -1 , {
            'left': (p)
        })