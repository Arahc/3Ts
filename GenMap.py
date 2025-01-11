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
            self.Map[2][self.row - 1][j] = 1
        
        # 多级向上 AD 跳
        for i in range(self.row - 3):
            self.Map[2][i][3] = 1
        self.Map[2][self.row - 4][4] = 1
        self.Map[2][self.row - 7][4] = 1
        self.Map[2][self.row - 10][4] = 1
        self.Map[2][self.row - 11][4] = 2
        
        self.Map[2][self.row - 2][9] = 1
        for i in range(self.row - 3,self.row):
            self.Map[2][i][10] = 1
        for i in range(self.row - 5,self.row - 2):
            self.Map[2][i][11] = 1
        
        # 顶格跳 + 冲刺
        self.Map[2][0][15] = 1  # 顶格跳起点
        self.Map[2][3][18] = 1  # 冲刺平台
        self.Map[2][3][21] = 1  # 冲刺平台
        self.Map[2][3][24] = 1  # 冲刺平台
        self.Map[2][3][27] = 2  # 宝箱
        
        # 远跳 + 冲刺
        self.Map[2][self.row - 3][12] = 1
        self.Map[2][self.row - 6][15] = 1
        self.Map[2][self.row - 6][23] = 1
        
        self.Map[2][self.row - 7][23] = 2
        
        self.Map[2][self.row - 6][24] = 1
        self.Map[2][self.row - 7][24] = 3
        

        self.Map[2][self.row - 5][27] = 1
        self.Map[2][self.row - 6][27] = 3
        self.Map[2][self.row - 5][28] = 1
        self.Map[2][self.row - 5][29] = 1
        self.Map[2][self.row - 6][29] = 3

        self.Map[2][self.row - 10][29] = 1
        self.Map[2][self.row - 7][31] = 1
        
        self.Map[2][self.row - 11][35] = 1
        self.Map[2][self.row - 11][36] = 1

        for i in range(self.row - 9, self.row - 1):
            self.Map[2][i][41] = 1
        self.Map[2][self.row - 6][42] = 1
        self.Map[2][self.row - 4][43] = 1

        for i in range(46,52):
            self.Map[2][self.row - 5][i] = 1
            self.Map[2][self.row - 8][i] = 1
        self.Map[2][self.row - 6][51] = 1
        self.Map[2][self.row - 7][51] = 1
        self.Map[2][self.row - 6][50] = 2
        for i in range(51,54):
            self.Map[2][self.row - 8][i] = 1

        for i in range(45,48):
            self.Map[2][self.row - 2][i] = 3
        
        self.Map[2][self.row - 2][53] = 2
        self.Map[2][self.row - 2][52] = 2
        for i in range(self.row):
            self.Map[2][i][54] = 1

        self.Map[2][self.row - 9][52] = 4
        self.Map[2][self.row - 9][53] = 5

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