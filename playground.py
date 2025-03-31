import numpy as np
import random
from snake import Snake, Canvas
import turtle
import networkx as nx
from networkx.algorithms.approximation import traveling_salesman_problem

# 游乐园
class Playground:

    def __init__(self, aSnake):
        self.snake = aSnake
        self.canvas = aSnake.canvas
        self.width = self.canvas.width
        self.height = self.canvas.height
        self.snake.create(color='blue')
        self.route = []
    
    def play(self):
        for pos in self.route:
            self.snake.move_goto(pos)

    # 浪一浪
    def wave(self, amplitude=1, wavelength=2*np.pi, phase=0):
        amplitude = amplitude  # 振幅
        wavelength = wavelength  # 波长
        phase = phase  # 相位
        x_enlarge = self.width/(10*np.pi)  # 放大倍数
        y_enlarge = self.height/(4*amplitude)
        # 生成x, y 坐标
        x = np.linspace(-4 * np.pi, 4 * np.pi, 200)  # x 轴上的点
        # 计算波浪形状
        y = amplitude * np.sin((2 * np.pi / wavelength) * x + phase)

        self.route = list(zip(x*x_enlarge, y*y_enlarge))
        return self.route
        
    def circle(self, radius=100, angle=2*np.pi):
        x = np.cos(np.linspace(0, angle, 200))
        y = np.sin(np.linspace(0, angle, 200))
        self.route = list(zip(x*radius, y*radius))
        return self.route
    
    def spiral(self, radius=100, angle=8*np.pi, step=0.5):
        theta = np.linspace(0, angle, 200)
        # 计算螺旋的 x 和 y 坐标
        x = np.cos(theta) * (radius + step * theta)
        y = np.sin(theta) * (radius + step * theta)
        # 将坐标组合成路径
        self.route = list(zip(x, y))
        return self.route
    
    def move(self, steps= 100, model= 'travel'):
        head = 0
        for _ in range(steps):
            sc_pos = self.canvas.turtle2screen(self.snake.snake.pos())
            if model.lower() == 'travel':
                head = self.travel(sc_pos, head)
            elif model.lower() == 'random':
                head = self.random(sc_pos, head)
            self.snake.move_forword(head)

    #遍历式 
    def travel(self, sc_pos, head):
        # 粗略分为8个方向
        head = int(head//45*45)%360
        grid_size = self.canvas.grid_size
        x = int(sc_pos[0]//grid_size)
        y = int(sc_pos[1]//grid_size)
        # 当前weizhi构成的9宫格，逆时针
        wz = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        # fangxiang
        fx = [0, 45, 90, 135, 180, 225, 270, 315]
        old_fx = int((head+180)//45*45)%360  #回头方向
        hits = [0] * len(wz)
        maxHit = 10000
        for i, item in enumerate(wz):
            x1 = x + item[0]
            y1 = y + item[1]
            sc_pos = (x1*grid_size, y1*grid_size)
            sc_pos1 = self.canvas.test_wall(sc_pos)
            if sc_pos1 != sc_pos:
                hits[i] = maxHit
            else:
                hits[i] = self.canvas.grid[y1][x1]

        minHit = min(hits)
        choice = [fx[i] for i, hit in enumerate(hits) if hit <= minHit]
        choice = set(choice)-set([old_fx])
        if int(head) in choice or len(choice) == 0:
            return head
        return random.choice(list(choice))

    #没头苍蝇式
    def random(self, sc_pos, head):
        # 粗略分为4个方向
        angle = 360//4
        ohead = int((head+180)//angle*angle)%360
        heads = set(range(0, 360, angle))
        fx = heads-set([ohead])
        return random.choice(list(fx))
    
    # 旅行商问题
    def tsp(self):
        G = nx.Graph()
        for i in range(len(self.canvas.beans)):
            pos = self.canvas.beans[i][1]
            id_name = str(i)
            for j in range(i+1, len(self.canvas.beans)):
                pos1 = self.canvas.beans[j][1]
                id1_name = str(j)
                weight = np.linalg.norm(np.array(pos)-np.array(pos1))
                G.add_edge(id_name, id1_name, weight=weight)

        tsp_path = traveling_salesman_problem(G, weight='weight')
        for i in tsp_path:
            pos = self.canvas.beans[int(i)][1]
            self.route.append(pos)
        return self.route

if __name__ == '__main__':
    aCanvas = Canvas()
    aGame = Playground(Snake(aCanvas))
    aGame.snake.grow(10)
    aGame.spiral(radius=50, step=5)
    aGame.play()
    aGame.wave(amplitude=50, wavelength=2*np.pi, phase=0)
    aGame.play()
    aGame.move(steps=1000, model='travel')
    aGame.tsp()
    aGame.play()

    turtle.done()
