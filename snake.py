import turtle
import random
import time
import math
# 设置画布
screen = turtle.Screen()
screen.bgcolor("white")
screen.setup(width=800, height=600)


class Snake:
    diameter = 1
    step_size = 10*diameter
    grid_size = 10*diameter
    body = []   # 蛇身
    grid = []   # 背景网格

    def __init__(self, bg_width=400, bg_height=400):
        
        w1 = bg_width//(self.grid_size)
        h1 = bg_height//(self.grid_size)
        # 创建一个背景网格
        self.grid = [[0 for _ in range(w1)] for _ in range(h1)]
        print("Grid: ", len(self.grid), len(self.grid[0]))

        self.bg_width = bg_width/2
        self.bg_height = bg_height/2

        self.snake = turtle.Turtle()
        self.shead = turtle.Turtle()    # 蛇头
        self.shead.shape("arrow")       # 蛇头朝上
        self.shead.color("green")
        self.shead.setheading(90)
        self.shead.shapesize(self.diameter/2, self.diameter/2, 5)   # 三角形
        self.shead.speed(0)

        self.snake.speed(0)
        self.snake.shape("circle")
        self.snake.shapesize(self.diameter/2, self.diameter/2, 1)

        self.length = 5       # 初始长度
        

    # 创建一条蛇
    def create(self, head=(0, 0), color="black"):
        self.shead.goto(head)

        self.snake.color(color)
        self.snake.penup()
        self.snake.goto(head[0], head[1]-self.step_size)
        self.snake.setheading(270)
        self.body.append((self.snake.stamp(), self.snake.pos()))
        for i in range(self.length-1):
            self.snake.forward(self.step_size)
            pos = self.snake.pos()
            self.body.append((self.snake.stamp(), pos))
        
        return
    
    def add_tail(self, size=1, Mode = 'random'):
        item = self.body[-1]    # 当前蛇尾的位置
        pos = item[1]
        self.snake.goto(pos[0], pos[1])
        fangxiang = int(self.snake.heading())   # 蛇尾的方向
        for i in range(size):
            new_move = self.chooseNext(pos, fangxiang, Mode=Mode)
            if isinstance(new_move, tuple):
                self.snake.goto(new_move)
            else:
                fangxiang = new_move
                self.snake.setheading(fangxiang)
                self.snake.forward(self.step_size)

            pos = self.snake.pos()
            self.body.append((self.snake.stamp(), pos))
        
        return
    
    def clear_tail(self, size=1):
        if len(self.body) < size:
            size = len(self.body)
        for _ in range(size):
            item = self.body.pop()
            stamp = item[0]
            self.snake.clearstamp(stamp)
        pos = self.shead.pos()
        self.snake.goto(pos[0], pos[1]-self.step_size)

    # 选择下步走法，有两种输出，一种是直接返回下一步的坐标，另一种是返回下一步的方向
    def chooseNext(self, pos, fangxiang='90', Mode='random'):
        # 撞墙情况直接返回新位置
        x, y = pos[0],pos[1]
        qiang = False
        if abs(x) > self.bg_width:
            x = abs(x)/x * (abs(x)-self.step_size)
            qiang = True
        if abs(y) > self.bg_height:
            y = abs(y)/y * (abs(y)-self.step_size)
            qiang = True
        if qiang:
            return (x, y)

        Mode = Mode.lower()
        fangxiang = fangxiang
        if Mode == 'random':       #上下左右随机,但不走返回
            fangxiang1 = self.by_random(pos, fangxiang)
        elif Mode == 'nocrowded':   # 选没走过的，不拥挤
            fangxiang1 = self.by_nocrowded(pos, fangxiang)
        else:
            fangxiang1 = fangxiang
        return fangxiang1
            
    def by_random(self, pos, fangxiang):
        fangxiang = ((fangxiang+180)//90)*90    #返回方向
        fangxiang = fangxiang % 360
        choice = set([0, 90, 180, 270])-set([fangxiang])
        return random.choice(list(choice))   # 选择一个方向

    def by_nocrowded(self, pos, fangxiang):
        x, y = pos
        grid_x = (x+self.bg_width)/self.grid_size
        grid_y = (y+self.bg_height)/self.grid_size
        min = -1
        hit = 0
        # 当前位置构成的9宫格，逆时针
        wz = [(1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1), (0,1), (1,1)]
        fangxiang = [0, 45, 90, 135, 180, 225, 270, 315]

        for i, item in enumerate(wz):
            grid_x += item[0]
            grid_y += item[1]
            if grid_x >= len(self.grid[0]) or grid_y >= len(self.grid):
                continue
            if hit >= self[grid_y][grid_x]:
                min = i
                hit = self[grid_y][grid_x]
        if min < 0:
            min = random.randint(0, 8)
        return fangxiang[min]


    def move_random(self, head=(0, 0), size=1, color="black"):
        self.size = size

        self.shead.penup()
        self.shead.goto(head)
        self.shead.pendown()

        self.snake.color(color)
        self.snake.penup()
        self.snake.goto(head)
        self.snake.pendown()
        d = self.diameter*0.9
        thetas = self.thetas[0:self.quad_size]

        quad = 0    # 0: 第一象限, 1: 第二象限, 2: 第三象限, 3: 第四象限
        for i in range(self.size):
            pos = self.snake.pos()
            theta = random.choice(thetas)
            x = pos[0] + d*theta[0]
            y = pos[1] + d*theta[1]
            if abs(x) > self.bg_width or abs(y) > self.bg_height:
                tset = {0, 1, 2, 3}-{quad}
                quad = random.choice(list(tset))
                thetas = self.thetas[quad*self.quad_size:(quad+1)*self.quad_size]
            if abs(x) > self.bg_width:
                x = abs(x)/x * (self.bg_width-d)
            if abs(y) > self.bg_height:
                y = abs(y)/y * (self.bg_height-d)
            
            self.snake.goto(x, y)
            self.snake.dot(self.diameter, color)
            self.body.append(self.snake.pos())

    
    def setheading(self, angle):
        self.snake.setheading(angle)
        self.shead.setheading(angle)
    
    def getheading(self):
        return self.shead.heading()
    
# 创建一个Turtle对象
start = time.time()
snake = Snake()
snake.create((0,0))
snake.add_tail(3000)
#snake.clear_tail(30)
end = time.time()
print("Time: ", end-start)
turtle.done()
