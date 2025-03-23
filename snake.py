import turtle
import random
import time
import bisect
import math


# 设置画布
class Screen:
    # 背景和网络的坐标系原点在左下角
    def __init__(self, width=800, height=600, bgcolor="white", grid_size=10):
        self.screen = turtle.Screen()
        self.screen.bgcolor(bgcolor)
        self.screen.setup(width=width, height=height)
        self.width = int(width)
        self.height = int(height)
        # 需要以中心为原点时的偏移量
        self.offset = (int(width/2), int(height/2))
        print("background: ", self.width, self.height)
        self.grid_size = grid_size
        self.grid = [[0 for _ in range(self.width//self.grid_size)] for _ in range(self.height//self.grid_size)]
        # 行数是高，列数是宽
        print("Grid: ", len(self.grid[0]), len(self.grid))

    # 撞墙检测，如果撞墙返回新位置
    def hit_wall(self, pos):
        x, y = pos
        # 没有撞墙
        if x> 0 and x< self.width and y> 0 or y< self.height:
            return pos
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
    
    # 推荐下一步的走的方向
    # model: random, traval, keephead
    def suggest_head(self, pos, head=0, model='random'):
        # 保持原方向
        model = model.lower()
        if model == 'keephead':
            return head
        # 随机不走回头路
        if model == 'random':
            head = (head+180)%(360//90)*90
            choice = set([0, 90, 180, 270])-set([head])
            return random.choice(list(choice))
        # 遍历式，选择最少走过的方向
        if model == 'travel':  
            return self.travel(pos, head)
        
        # 完全随机
        return (head+random.randint(0,360))%360
    

    #遍历式    
    def travel(self, pos, head):
        pos = self.shiftXY(pos)
        x = int(pos[0]//self.grid_size)
        y = int(pos[1]//self.grid_size)
        if x<0 or y<0 :
            print("Error: ", x, y)
        # 当前weizhi构成的9宫格，逆时针
        wz = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        # fangxiang
        fx = [0, 45, 90, 135, 180, 225, 270, 315]
        old_fx = int(((head+180)//45*45)%360)  #回头方向
        hits = [0] * len(wz)
        maxHit = 10000
        for i, item in enumerate(wz):
            x1 = x + item[0]
            y1 = y + item[1]
            if x1 >= len(self.grid[0]) or y1 >= len(self.grid):
                hits[i] = maxHit
            else:
                hits[i] = self.grid[y1][x1]
        minHit = min(hits)
        choice = [fx[i] for i, hit in enumerate(hits) if hit <= minHit]
        if head in choice:
            return head
        if len(choice) == 1:
            return choice[0]
        choice = set(choice)-set([old_fx])
        return random.choice(list(choice))

    # 坐标系转换
    def shiftXY(self, pos):
        x, y = pos
        return (x+self.offset[0], y+self.offset[1])
    #
    def get_angle(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        
        dy = y2 - y1
        dx = x2 - x1
        tan = math.atan2(dy, dx)
        angle = math.degrees(tan)
        return angle


class Snake:
    diameter = 1
    step_size = 10*diameter    # 一个身位的长度
    snake = turtle.Turtle()    # 蛇身
    shead = turtle.Turtle()    # 蛇头
    body = []   # 蛇身

    def __init__(self, bg_width=400, bg_height=400):
        
        self.screen = Screen(bg_width, bg_height)

        self.shead.shape("arrow")       # 蛇头是个上三角
        self.shead.color("green")
        self.shead.setheading(90)
        self.shead.shapesize(self.diameter/2, self.diameter/2, 5)   # 三角形
        self.shead.speed(0)

        self.snake.shape("circle")      # 蛇身是个圆
        self.snake.color("blue")
        self.snake.shapesize(self.diameter/2, self.diameter/2, 1)
        self.snake.speed(0)
        
        self.length = 5         # 初始长度
        self.minLen = 5         # 最小长度
        self.maxLen = 200       # 最大长度

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
    
    # 生长
    def grow(self, size=1):
        # 需要画出来的长度
        add_size = min(self.length+size, self.maxLen) - min(self.length, self.maxLen)
        self.length += size
        
        item = self.body[-1]    # 当前蛇尾的信息
        pos = item[1]
        self.snake.goto(pos[0], pos[1])
        head = self.snake.heading()
        
        for _ in range(add_size):
            new_head = self.screen.suggest_head(pos, head, model='travel')
            self.snake.setheading(new_head)
            self.snake.forward(self.step_size)
            pos = self.snake.pos()
            self.body.append((self.snake.stamp(), pos))
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

    def setheading(self, angle):
        self.snake.setheading(angle)
        self.shead.setheading(angle)
    
    def getheading(self):
        return self.shead.heading()
    

# 创建一个Turtle对象
start = time.time()
snake = Snake()
snake.create((100,100), "red")

snake.grow(300)
snake.shrink(200)
end = time.time()
print("Time: ", end-start)
turtle.done()
