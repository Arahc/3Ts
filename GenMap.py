"""
这是个用来编辑地图的文件
0 -> 空地
1 -> 道路
2 -> 宝箱
3 -> 地刺
4,5 -> 传送门（下）

row, col 的顺序和 pygame 坐标系顺序一样
x 轴向右为正方向, y 轴向下为正方向
"""

import random
from GameSettings import *

class GenMap():
    def __init__(self):
        self.row = WindowSettings.height // MoveSettings.blockSize
        self.col = WindowSettings.width // MoveSettings.blockSize
        self.col *= 3   # 屏幕外的地图
        # row = 13, col = 60
        
        r = self.row
        c = self.col
        self.Map = [[[0 for i in range(c)] for j in range(r)] for k in range(3)] # n*m*3

        # 铺地板
        for j in range(c):
            self.Map[1][r - 1][j] = 1
        
        self.ChestMoney = [[[0 for i in range(c)] for j in range(r)] for k in range(3)] # n*m*3
        
        # 多级向上 AD 跳
        for i in range(r - 3):
            self.Map[1][i][3] = 1
        self.Map[1][r - 4][4] = 1
        self.Map[1][r - 7][4] = 1
        self.Map[1][r - 10][4] = 1
        self.Map[1][r - 11][4] = 2
        self.ChestMoney[1][r - 11][4] = random.randint(20, 30)
        
        self.Map[1][r - 2][9] = 1
        for i in range(r - 3,r):
            self.Map[1][i][10] = 1
        for i in range(r - 5,r - 2):
            self.Map[1][i][11] = 1
        
        # 远跳 + 冲刺
        self.Map[1][r - 3][12] = 1
        self.Map[1][r - 6][20] = 1
        self.Map[1][r - 6][28] = 1
        
        self.Map[1][r - 7][28] = 2
        self.ChestMoney[1][r - 7][28] = random.randint(20, 30)
        
        self.Map[1][r - 6][29] = 1
        self.Map[1][r - 7][29] = 3
        

        self.Map[1][r - 5][32] = 1
        self.Map[1][r - 6][32] = 3
        self.Map[1][r - 5][33] = 1
        self.Map[1][r - 5][34] = 1
        self.Map[1][r - 6][34] = 3

        self.Map[1][r - 10][34] = 1
        self.Map[1][r - 7][36] = 1
        
        self.Map[1][r - 11][40] = 1
        self.Map[1][r - 11][41] = 1

        for i in range(r - 9, r - 1):
            self.Map[1][i][46] = 1
        self.Map[1][r - 6][47] = 1
        self.Map[1][r - 4][48] = 1

        for i in range(51,57):
            self.Map[1][r - 5][i] = 1
            self.Map[1][r - 8][i] = 1
        self.Map[1][r - 6][56] = 1
        self.Map[1][r - 7][56] = 1
        self.Map[1][r - 6][55] = 2
        self.ChestMoney[1][r - 6][55] = random.randint(20, 30)

        for i in range(56,59):
            self.Map[1][r - 8][i] = 1

        for i in range(50,53):
            self.Map[1][r - 2][i] = 3
        
        self.Map[1][r - 2][58] = 2
        self.ChestMoney[1][r - 2][58] = random.randint(20, 30)
        self.Map[1][r - 2][57] = 2
        self.ChestMoney[1][r - 2][57] = random.randint(20, 30)

        for i in range(r):
            self.Map[1][i][59] = 1

        self.Map[1][r - 9][57] = 4
        self.Map[1][r - 9][58] = 5

        # 铺地板
        for j in range(self.col):
            self.Map[2][r - 1][j] = 1
        
        self.Map[2][r - 4][3] = 1
        self.Map[2][r - 7][3] = 1
        self.Map[2][r - 10][3] = 1
        self.Map[2][r - 10][4] = 1

        for i in range(3, r - 4):
            self.Map[2][i][5] = 1
        self.Map[2][r - 2][5] = 3

        for i in range(3, r - 4):
            self.Map[2][i][12] = 1
        self.Map[2][r - 2][12] = 3
        self.Map[2][r - 2][14] = 2
        self.ChestMoney[2][r - 2][14] = random.randint(20, 30)

        for i in range(18,30):
            self.Map[2][r - 2][i] = 3

        self.Map[2][r - 4][20] = 1
        self.Map[2][r - 4][26] = 1
        self.Map[2][r - 5][26] = 2
        self.ChestMoney[2][r - 5][26] = random.randint(20, 30)
        self.Map[2][r - 4][30] = 1
        
        self.Map[2][r - 6][29] = 1
        self.Map[2][r - 8][32] = 1
        self.Map[2][r - 8][33] = 1
        for i in range(0, 3):
            self.Map[2][i][34] = 1
        for i in range(r - 8, r - 1):
            self.Map[2][i][34] = 1
        self.Map[2][r - 7][35] = self.Map[2][r - 11][35] = 1
        self.Map[2][r - 6][36] = self.Map[2][r - 10][36] = 1
        self.Map[2][r - 5][37] = self.Map[2][r - 9][37] = 1
        self.Map[2][r - 4][38] = self.Map[2][r - 8][38] = 1
        self.Map[2][r - 5][38] = 3
        self.Map[2][r - 3][39] = self.Map[2][r - 8][39] = 1
        self.Map[2][r - 2][40] = 2
        self.ChestMoney[2][r - 5][33] = random.randint(20, 30)
        self.Map[2][r - 2][41] = 3
        self.Map[2][r - 2][42] = 3
        self.Map[2][r - 2][43] = 3
        self.Map[2][r - 2][44] = 3
        self.Map[2][r - 2][45] = 3
        
        # 随机生成地图
        # # terrain1 几段连续的跳台
        # len1 = 5 # 每段 5 块
        # cnt1 = 3 # 3 段
        # maxHeight1 = 3 # 相邻两端的最大落差
        # def GenTerrain1(x):
        #     lastY = r // 2
        #     for i in range(cnt1):
        #         l = max(lastY - maxHeight1, 2)
        #         r = min(lastY + maxHeight1, r - 3) # 可以从最低的地面直接通过
        #         y = random.randint(l, r)
        #         L = x + i * len1
        #         R = min(c - 1, x + (i + 1) * len1 - 1)
        #         for j in range(L, R):
        #             self.Map[1][y][j] = 1
        #         lastY = y
        
        # for i in range(0, c - 1, len1 * cnt1):
        #     GenTerrain1(i)

        # # GenChest 生成宝箱
        # def GenChest():
        #     vec = []
        #     for i in range(r):
        #         for j in range(c):
        #             if self.Map[1][i][j] == 1 and i > 0:
        #                 vec.append((i, j))
        #     random.shuffle(vec)
        #     self.Map[1][vec[0][0] - 1][vec[0][1]] = 2
        #     self.ChestMoney[1][vec[0][0] - 1][vec[0][1]] = random.randint(20, 30)
        
        # for i in range(10):
        #     GenChest()

        # # GenTrap 生成陷阱
        # def GenTrap():
        #     l = random.randint(0, c - 1)
        #     r = random.randint(l, min(l + 3, c - 1))
        #     for i in range(l, r):
        #         self.Map[1][r - 1][i] = 3

        # for i in range(5):
        #     GenTrap()