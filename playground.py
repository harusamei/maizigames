import numpy as np
import random
from snake import Snake, Canvas

# 游乐园
class Playground:

    def __init__(self, aSnake):
        self.snake = aSnake
        self.canvas = aSnake.canvas
        self.width = self.canvas.width
        self.height = self.canvas.height
        self.route = []
    
    def play(self):
        for pos in self.route:
            self.snake.move_goto(pos)

    # 设置波浪参数
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
        
    def circle(self, radius=1, angle=2*np.pi):
        x = np.cos(np.linspace(0, angle, 200))
        y = np.sin(np.linspace(0, angle, 200))
        self.route = list(zip(x*radius, y*radius))
        return self.route
    
    # 旋转角度, 逆时针为正，顺时针为负
    def rotate_angle(self, angle, rotation):
        angle = angle%360+360
        rotation = rotation%360
        new_angle = angle + rotation
        new_angle = (new_angle + 360) % 360
        return new_angle
    
    #遍历式    
    def traval(self, sc_pos, head):
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
                print(x1, y1)
                hits[i] = self.canvas.grid[y1][x1]

        minHit = min(hits)
        choice = [fx[i] for i, hit in enumerate(hits) if hit <= minHit]
        choice = set(choice)-set([old_fx])
        if int(head) in choice or len(choice) == 0:
            return head
        return random.choice(list(choice))


if __name__ == '__main__':
    aCanvas = Canvas()
    aGame = Playground(Snake(aCanvas))
    aGame.snake.create()
    for i in range(5):
        aGame.wave()
        aGame.play()
        aGame.circle(200)
        aGame.play()
