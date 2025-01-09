"""
这是个用来编辑地图的文件
0 -> 空地
1 -> 道路
2 -> 宝箱

row, col 的顺序和 pygame 坐标系顺序一样
x 轴向右为正方向, y 轴向下为正方向
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

        # 随机生成地图
        # for i in range(80):
        #     x = random.randint(0, self.col - 1)
        #     y = random.randint(4, self.row - 1)
        #     self.map1[y][x] = random.randint(1,2)
        
        # terrain1 几段连续的跳台
        len1 = 5 # 每段 5 块
        cnt1 = 3 # 3 段
        maxHeight1 = 5 # 相邻两端的最大落差
        def GenTerrain1(x):
            lastY = self.row // 2
            for i in range(cnt1):
                l = max(lastY - maxHeight1, 2)
                r = min(lastY + maxHeight1, self.row - 3) # 可以从最低的地面直接通过
                y = random.randint(l, r)
                L = x + i * len1
                R = min(self.col - 1, x + (i + 1) * len1 - 1)
                for j in range(L, R):
                    self.map1[y][j] = 1
                lastY = y
        
        for i in range(0, self.col - 1, len1 * cnt1):
            GenTerrain1(i)

        
        # GenChest 生成宝箱
        def GenChest():
            vec = []
            for i in range(self.row):
                for j in range(self.col):
                    if self.map1[i][j] == 1 and i > 0:
                        vec.append((i, j))
            random.shuffle(vec)
            self.map1[vec[0][0] - 1][vec[0][1]] = 2
        
        for i in range(10):
            GenChest()

        # GenTrap 生成陷阱
        def GenTrap():
            l = random.randint(0, self.col - 1)
            r = random.randint(l, min(l + 3, self.col - 1))
            for i in range(l, r):
                self.map1[self.row - 1][i] = 3

        for i in range(5):
            GenTrap()



