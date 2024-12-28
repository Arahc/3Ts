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

row = WindowSettings.height // WindowSettings.blockSize
col = WindowSettings.width // WindowSettings.blockSize
col *= 3

# map1 是一个自定义地图，可以手动设置
map1 = [[0 for i in range(col)] for j in range(row)] # 生成一个n*m的二维数组
for j in range(col):
    map1[row - 1][j] = 1

for i in range(80):
    x = random.randint(0, col - 1)
    y = random.randint(4, row - 1)
    map1[y][x] = random.randint(1, 3)