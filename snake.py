import turtle
import random
import time
import math
import sys

# 设置画布
class Canvas:
    # 背景和网络的坐标系原点在左下角, 注意坐标系与turtle的坐标系不同
    # turtle的坐标系原点在中心，向右是x正方向，向上是y正方向
    # 默认使用screen的坐标系，需要转换
    def __init__(self, width=800, height=600, bgcolor="white", grid_size=10):
        self.screen = turtle.Screen()
        self.screen.bgcolor(bgcolor)
        self.screen.setup(width=width, height=height)

        self.pen = turtle.Turtle()
        self.pen.shape('square')
        self.pen.shapesize(0.5, 0.5, 2)
        self.pen.speed(0)
        self.beans = []

        self.width = int(width)
        self.height = int(height)
        # 需要以中心为原点时的偏移量
        self.offset = (int(width/2), int(height/2))
        print("background: ", self.width, self.height)
        self.grid_size = grid_size      # 网格大小
        self.grid = [[0 for _ in range(self.width//self.grid_size)] for _ in range(self.height//self.grid_size)]
        # 行数是高，列数是宽
        print("Grid: ", len(self.grid[0]), len(self.grid))
        self.place_beans(10)

    # 撞墙检测，如果撞墙返回新位置
    def test_wall(self, sc_pos):
        x, y = sc_pos
        # 没有撞墙
        if x> 0 and x< self.width and y> 0 and y< self.height:
            return sc_pos
        # 撞墙
        x = min(max(x, 0)+5, self.width-5)
        y = min(max(y, 0)+5, self.height-5)
        return (x, y)
    
    # 记录网格被经历的次数
    def record_grid(self, pos):
        x = int(pos[0]//self.grid_size)
        y = int(pos[1]//self.grid_size)
        self.grid[y][x] += 1
        return
    
    def place_beans(self, count=10):
        
        for i in range(count):
            x = random.randint(-self.width*0.45, self.width*0.45)
            y = random.randint(-self.height*0.45, self.height*0.45)
            color = random.choice(['red', 'blue', 'green', 'yellow', 'purple', 'orange'])
            self.pen.color(color)
            self.pen.penup()
            self.pen.goto(x, y)
            self.beans.append((self.pen.stamp(), (x, y)))
        return
    
    def turtle2screen(self, pos):
        x, y = pos
        sc_x = x + self.offset[0]
        sc_y = y + self.offset[1]
        return (sc_x, sc_y)
    
    def screen2turtle(self, sc_pos):
        sc_x, sc_y = sc_pos
        x = sc_x - self.offset[0]
        y = sc_y - self.offset[1]
        return (x,y)
    

# 蛇的行为
class Snake:
    diameter = 1
    step_size = 10*diameter    # 一个身位的长度
    snake = turtle.Turtle()    # 蛇身
    shead = turtle.Turtle()    # 蛇头
    body = []   # 记录走过的路径

    def __init__(self, myCanvas):
        
        self.canvas = myCanvas

        self.shead.shape("arrow")       # 蛇头是个上三角
        self.shead.color("green")
        self.shead.setheading(90)
        self.shead.shapesize(self.diameter/2, self.diameter/2, 5)   # 三角形
        self.shead.speed(0)

        self.snake.shape("circle")      # 蛇身是个圆
        self.snake.color("red")
        self.snake.shapesize(self.diameter/2, self.diameter/2, 1)
        self.snake.speed(0)
        
        self.length = 5         # 初始长度
        self.minLen = 5         # 最小长度
        self.maxLen = 200       # 最大长度

    # 向前移动一步
    def move_forword(self, head=0):

        self.shead.setheading(head)
        pos = self.shead.pos()
        self.shead.forward(self.step_size)
        self.snake.goto(pos[0], pos[1])
        self.body.insert(0, (self.snake.stamp(), self.snake.pos()))
        item = self.body.pop()
        stamp = item[0]
        self.snake.clearstamp(stamp)
    
    def move_goto(self, pos):
        pos1 = self.test_wall(pos)
        if pos1 != pos:
            pos = pos1
        head = self.get_angle(self.shead.pos(), pos)
        steps = int(self.shead.distance(pos)/self.step_size)
        for _ in range(steps):
            self.move_forword(head)

    # 推荐下一步的走的方向，像导航一样
    # model: random, keephead
    def ask_head(self, pos, head=0, model='random'):
        # 保持原方向
        model = model.lower()
        if model == 'keephead':
            return head
        # 随机不走回头路
        if model == 'random':
            # 粗略分为4个方向
            head = int((head+180)//90*90)%360
            choice = set([0, 90, 180, 270])-set([head])
            return random.choice(list(choice))
        # 完全随机
        return (head+random.randint(0,360))%360
       
    # 创建一条蛇
    def create(self, start=(0, 0), color="green"):
        self.shead.penup()
        self.shead.goto(start)
        self.snake.color(color)
        self.snake.penup()
        self.snake.goto(start[0], start[1]-self.step_size)
        self.snake.setheading(270)
        self.body.append((self.snake.stamp(), self.snake.pos()))
        for i in range(self.length-1):
            self.snake.forward(self.step_size)
            pos = self.snake.pos()
            self.body.append((self.snake.stamp(), pos)) # 记录蛇身的信息

        return
    
    def test_wall(self, pos):
        # 坐标变换
        sc_pos = self.canvas.turtle2screen(pos)
        sc_pos1 = self.canvas.test_wall(sc_pos)
        if sc_pos1 != sc_pos:   # 撞墙了, 返回新的位置
            return self.canvas.screen2turtle(sc_pos1)
        return pos
    
    # 生长
    def grow(self, size=1, model='random'):
        # 需要画出来的长度
        add_size = min(self.length+size, self.maxLen) - min(self.length, self.maxLen)
        self.length += size
        
        item = self.body[-1]    # 当前蛇尾的信息
        pos = item[1]
        self.snake.goto(pos[0], pos[1])
        head = self.snake.heading()
        
        for _ in range(add_size):
            new_head = self.ask_head(pos, head, model)
            self.snake.setheading(new_head)
            self.snake.forward(self.step_size)
            pos = self.snake.pos()
            self.body.append((self.snake.stamp(), pos))
            pos1 = self.test_wall(pos)
            # 撞墙了, 调整到新位置
            if pos1 != pos:
                new_head = self.get_angle(pos, pos1)
                self.snake.setheading(new_head)
                self.snake.goto(pos1)
                self.body.append((self.snake.stamp(), pos1))
                pos = self.snake.pos()
            head = new_head
        
        return
    
    # 缩小
    def shrink(self, size=1):
        if self.length - size < self.minLen:
            size = self.length - self.minLen
        reduce_size = min(self.length, self.maxLen) - min(self.length-size, self.maxLen)
        self.length = self.length - size

        for _ in range(reduce_size):
            item = self.body.pop()
            stamp = item[0]
            self.snake.clearstamp(stamp)
        pos = self.shead.pos()
        self.snake.goto(pos[0], pos[1]-self.step_size)

    def get_angle(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        
        dy = y2 - y1
        dx = x2 - x1
        tan = math.atan2(dy, dx)
        angle = math.degrees(tan)
        return angle
    
    def setheading(self, angle):
        self.snake.setheading(angle)
        self.shead.setheading(angle)
    
    def getheading(self):
        return self.shead.heading()
    

if __name__ == '__main__':

    # 创建一个Turtle对象
    start = time.time()
    myCanvas = Canvas()
    
    snake = Snake(myCanvas)
    snake.create((100,100), "red")

    snake.grow(200, 'keephead')
    snake.shrink(50)
    head = 90
    for i in range(200):
        if i% 50 == 0:
            head += 90
            head = head % 360
        snake.move_forword(head)
    snake.move_goto((10, 400))
    end = time.time()
    print("Time: ", end-start)

    turtle.done()
