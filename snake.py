import turtle
import random
import time
import bisect

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
        
        w1 = bg_width//(self.grid_size)+1
        h1 = bg_height//(self.grid_size)+1
        # 创建一个背景网格, 行数是高， 列数是宽
        self.grid = [[0 for _ in range(w1)] for _ in range(h1)]
        self.g_offset = (len(self.grid[0])//2, len(self.grid)//2)
        print("Grid: ", len(self.grid[0]),len(self.grid))
        print("Offset: ", self.g_offset)

        self.bg_width = bg_width/2
        self.bg_height = bg_height/2
        print("bg_width: ", self.bg_width, "bg_height: ", self.bg_height)

        self.snake = turtle.Turtle()    # 蛇身
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
        self.maxLen = 10000  # 最大长度
        

    # 创建一条蛇
    def create(self, head=(0, 0), color="green"):
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
    
    # random, nocrowded
    def add_tail(self, size=1, Mode= 'nocrowded'):
        # 只计数，不画出来
        if self.length >= self.maxLen:
            self.length = self.length + size
            return
        size = min(size, self.maxLen-self.length)
        item = self.body[-1]    # 当前蛇尾的位置
        pos = item[1]
        self.snake.goto(int(pos[0]), int(pos[1]))
        fx = int(self.snake.heading())   # 蛇尾的方向
        for i in range(size):
            new_step = self.moveNext(pos, fx, Mode=Mode)
            if isinstance(new_step, tuple):
               print("change pos: ", new_step)
               self.snake.goto(new_step)
               fx = random.choice([0, 90, 180, 270])
            else:
                fx = new_step
                print("New Fx: ", fx)
                self.snake.setheading(fx)
                self.snake.forward(self.step_size)

            pos = self.snake.pos()
            grid_x = int(pos[0]//self.grid_size)+self.g_offset[0]
            grid_y = int(pos[1]//self.grid_size)+self.g_offset[1]
            print("pos: ", pos)
            print("Grid: ", grid_x, grid_y)
            grid_x = max(0, grid_x)
            grid_y = max(0, grid_y)
            if grid_x < len(self.grid[0]) and grid_y < len(self.grid):
                self.grid[grid_y][grid_x] += 1
            self.body.append((self.snake.stamp(), pos))

        # 蛇长增加
        self.length += size
        return
    
    def clear_tail(self, size=1):
        if self.length - size > self.maxLen:
            self.length = self.length - size
            return
        elif len(self.body) < size:
            size = len(self.body)-1
        else:
            size = len(self.body)-(self.length-size)
            
        for _ in range(size):
            item = self.body.pop()
            stamp = item[0]
            self.snake.clearstamp(stamp)
        pos = self.shead.pos()
        self.snake.goto(pos[0], pos[1]-self.step_size)

    # 选择下步走法，有两种输出，一种是直接返回下一步的坐标，另一种是返回下一步的方向
    def moveNext(self, pos, fx='90', Mode='random'):
        # 撞墙情况直接返回新位置
        x, y = int(pos[0]), int(pos[1])
        qiang = False
        if abs(x) > self.bg_width:
            if x< 0: x = x + self.step_size*1.5
            if x> 0: x = x - self.step_size*1.5
            qiang = True
        if abs(y) > self.bg_height:
            if y< 0: y = y + self.step_size*1.5
            if y> 0: y = y - self.step_size*1.5
            qiang = True
        if qiang:
            return (int(x), int(y))
        
        fx = int(fx)
        Mode = Mode.lower()
        if Mode == 'random':        # 上下左右随机,但不走返回
            fx = self.by_random(pos, fx)
        elif Mode == 'nocrowded':   # 选没走过的，不拥挤
            fx = self.by_nocrowded(pos, fx)
        return fx

    def by_random(self, pos, fx):
        
        fx = ((fx+180)//90)*90    #逆向方向
        fx = fx % 360
        choice = set([0, 90, 180, 270])-set([fx])
        return random.choice(list(choice))   # 选择一个方向

    def by_nocrowded(self, pos, fx):
        grid_x = int(pos[0]//self.grid_size)+self.g_offset[0]
        grid_y = int(pos[1]//self.grid_size)+self.g_offset[1]
        
        # 当前位置构成的9宫格，逆时针
        wz = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        fangxiang = [0, 45, 90, 135, 180, 225, 270, 315]
        wz = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        fangxiang = [0, 90, 180, 270]
        old_index = bisect.bisect_left(fangxiang, fx)
        if fx == 90:
           old_index
        count = [0] * 4
        maxHit = 10000
        for i, item in enumerate(wz):
            grid_x1 = grid_x + item[0]
            grid_y1 = grid_y + item[1]
            grid_x1 = max(0, grid_x1)
            grid_y1 = max(0, grid_y1)
            if grid_x1 >= len(self.grid[0]) or grid_y1 >= len(self.grid):
                count[i] = maxHit
            else:
                count[i] = self.grid[grid_y1][grid_x1]
            #print(f"grid_x1: {grid_x1}, grid_y1: {grid_y1}, count: {count[i]}")

        minHit = min(count)
        if count[old_index] == minHit:
            return fangxiang[old_index]
        
        candidates = []
        for i, hit in enumerate(count):
            if hit <= minHit:
                candidates.append(i)  # 修正这里的错误
        minIndex = random.choice(candidates)
        return fangxiang[minIndex]


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
snake.create((0,0), "red")

snake.add_tail(3000)
snake.clear_tail(3000)
end = time.time()
print("Time: ", end-start)
turtle.done()
