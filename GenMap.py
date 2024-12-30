"""
这是个用来编辑地图的文件
0 -> 空地
1 -> 土
2 -> 草地
3 -> 石头

row, col 的顺序和 pygame 坐标系顺序一样
"""

import random
from GameSettings import *

class GenMap():
    def __init__(self):
        self.row = WindowSettings.height // MoveSettings.blockSize
        self.col = WindowSettings.width // MoveSettings.blockSize
        self.col *= 3

        # map1 是一个自定义地图，可以手动设置
        self.map1 = [[0 for i in range(self.col)] for j in range(self.row)] # 生成一个n*m的二维数组
        for j in range(self.col):
            self.map1[self.row - 1][j] = 1

        for i in range(80):
            x = random.randint(0, self.col - 1)
            y = random.randint(4, self.row - 1)
            self.map1[y][x] = random.randint(1, 3)