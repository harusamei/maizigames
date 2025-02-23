import numpy as np


class Journey:

    def __init__(self):
        self.trajectory = []
    
    # 设置波浪参数
    
    def wave(self, amplitude=1, wavelength=2*np.pi, phase=0):
        amplitude = amplitude  # 振幅
        wavelength = wavelength  # 波长
        phase = phase  # 相位
        # 生成x, y 坐标
        x = np.linspace(0, 4 * np.pi, 1000)  # x 轴上的点
        # 计算波浪形状
        y = amplitude * np.sin((2 * np.pi / wavelength) * x + phase)
        self.trajectory = list(zip(x, y))
        return self.trajectory
        
    def circle(self, radius=1, angle=2*np.pi):
        x = np.linspace(0, angle, 1000)
        y = radius * np.sin(x)
        self.trajectory = list(zip(x, y))
        return self.trajectory
    
    # 旋转角度, 逆时针为正，顺时针为负
    def rotate_angle(self, angle, rotation):
        angle = angle%360+360
        rotation = rotation%360
        new_angle = angle + rotation
        new_angle = (new_angle + 360) % 360
        return new_angle
    

