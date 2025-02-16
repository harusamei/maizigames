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
    body = []   # 蛇身
    thetas = [] # 计算圆周角度用
    # 72个角度, 分为4个象限/方向
    for i in range(0, 360, 5):
        x_cos = math.cos(math.radians(i))
        y_sin = math.sin(math.radians(i))
        thetas.append((x_cos, y_sin))
    quad_size = int(len(thetas)/4)
    print(f"quad lengh: {len(thetas)}, quad size: {quad_size}")

    def __init__(self, bg_width=400, bg_height=400):
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

        self.size = 5

    def create(self, head=(0, 0), color="black"):
        self.shead.goto(head)

        self.snake.color(color)
        self.snake.penup()
        self.snake.goto(head[0], head[1]-self.step_size)
        self.snake.setheading(270)
        self.body.append((self.snake.stamp(), self.snake.pos()))
        for i in range(self.size):
            self.snake.forward(self.step_size)
            pos = self.snake.pos()
            self.body.append((self.snake.stamp(), pos))
        
        return
    
    def add_tail(self, size=1):
        item = self.body[-1]
        pos = item[1]
        self.snake.goto(pos[0], pos[1])
        fangxiang = int(self.snake.heading())   # 蛇尾的方向
        for i in range(size):
            self.snake.setheading(fangxiang)
            new_pos = self.tiaozheng_pos(self.snake.pos())
            if new_pos != self.snake.pos():
                self.snake.goto(new_pos)
            self.snake.forward(self.step_size)
            pos = self.snake.pos()
            self.body.append((self.snake.stamp(), pos))
            choice = self.choose_direction(fangxiang)
            #print(f"fangxiang: {fangxiang}, choice: {choice}")
            fangxiang = random.choice(list(choice))
        
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

    # 旋转角度, 逆时针为正，顺时针为负
    def rotate_angle(self, angle, rotation):
        new_angle = angle + rotation
        if new_angle < 0:
            new_angle += 360
        elif new_angle >= 360:
            new_angle -= 360
        return new_angle
    
    # 选择方向
    # 去掉当前方向的反方向，顺逆各45度
    def choose_direction(self, angle):
        b_angle = self.rotate_angle(angle, 180)
        b1 = self.rotate_angle(b_angle, 60)
        b2 = self.rotate_angle(b_angle, -60)
        if b1 < b2:
            b_set = set(range(0, b1, 5)).union(set(range(b2, 360, 5)))
        else:
            b_set = set(range(b2, b1, 5))
        return set(range(0, 360, 5))-b_set
    
    def tiaozheng_pos(self, pos):
        x = pos[0]
        y = pos[1]
        if abs(x) > self.bg_width:
            x = abs(x)/x * (self.bg_width-self.step_size)
        if abs(y) > self.bg_height:
            y = abs(y)/y * (self.bg_height-self.step_size)
        return (x, y)

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
    
    def move_forward(self, step=1):
        for i in range(step):
            s_pos = self.shead.pos()
            self.shead.forward(self.step_size*self.diameter)
            self.snake.penup()
            self.snake.goto(s_pos)
            for _ in range(self.step_size):
                self.snake.forward(self.diameter)
                self.snake.dot(self.diameter)
                self.body.insert(0, self.snake.pos())
            self.clear_tail(self.step_size)

    def move_goto(self, t_x, t_y):
        s_pos = self.shead.pos()
        distance = math.sqrt((t_x-s_pos[0])**2 + (t_y-s_pos[1])**2)
        d = self.diameter*0.9
        count = math.floor(distance/d)
        print("Distance: ", distance, "Count: ", count)
        angle = math.degrees(math.atan2(t_y-s_pos[1], t_x-s_pos[0]))
        self.shead.setheading(angle)
        self.shead.pendown()
        self.shead.goto(t_x, t_y)

        self.snake.setheading(angle)
        self.snake.penup()
        self.snake.goto(s_pos)
        self.snake.pendown()
        for i in range(count):
            self.snake.forward(d)
            self.snake.dot(self.diameter)
            self.body.insert(0, self.snake.pos())
        self.clear_tail(count)

    def move_up(self, step=1):
        self.setheading(90)
        self.move_forward(step)
    
    def move_down(self, step=1):
        self.setheading(270)
        self.move_forward(step)

    def move_left(self, step=1):
        self.setheading(180)
        self.move_forward(step)

    def move_right(self, step=1):
        self.setheading(0)
        self.move_forward(step)

    # 以跎头为圆心, 逆时针旋转
    def move_circle(self, center, r):
        steps = 2*math.pi*r/(self.diameter*2)   # 一个圆的步数,一次两个dot长
        theta = []
        for i in range(0, 360, int(360/steps)):
            x_cos = math.cos(math.radians(i))
            y_sin = math.sin(math.radians(i))
            theta.append((x_cos, y_sin))

        for item in theta:
            x = center[0] + r*item[0]
            y = center[1] + r*item[1]
            self.move_goto(x, y)
    
# 创建一个Turtle对象
start = time.time()
snake = Snake()
snake.create((0,0))
snake.add_tail(3000)
snake.clear_tail(50)
end = time.time()
print("Time: ", end-start)
turtle.done()
