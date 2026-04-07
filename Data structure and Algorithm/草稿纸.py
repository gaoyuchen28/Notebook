# 谢尔宾斯基三角形

import turtle
t = turtle.Turtle()

def DrawTriangle(point,color):
    t.fillcolor(color)
    t.penup()
    t.goto(point['top'])
    t.begin_fill()
    t.goto(point['left'])
    t.goto(point['right'])
    t.goto(point["top"])
    t.end_fill()

def getMid(p1, p2):
    return((p1[0]+p2[0])/2, (p1[1]+p2[1])/2)

def Triangle(degree, point):
    colormap = ['blue','green','red','yellow','purple','orange']
    DrawTriangle(point,colormap[degree])
    if degree > 0 :
        Triangle(degree-1,
                {  'left': getMid(point['top'],point['left']),
                    'right': getMid(point['top'],point['right']),
                    'top' : point['top']})
        Triangle(degree-1,
                {  'left' : point['left'],
                    'right': getMid(point['left'],point['right']),
                    'top' : getMid(point['left'],point['top'])})
        Triangle(degree-1,
                {  'left' : getMid(point['left'],point['right']),
                    'right': point['right'],
                    'top' : getMid(point['right'],point['top'])})

point = {
    'left': (-200, -100),
    'right':(200, -100),
    'top':(0, 200) }

Triangle(5, point)

turtle.done()