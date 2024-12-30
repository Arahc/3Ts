import pygame

# This is a dictionary that contains all the settings for the game.
# It allows you to easily change settings without having to change the code repeatedly.

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class WindowSettings():
    width = 1000
    height = 650
    title = "demo"
    fps = 120

class MoveSettings():
    playerHeight = 70 # 人物高度
    playerWidth = 35 # 人物宽度
    speed = 6 # 人物移动速度
    gravity = 900 # 重力加速度
    initialSpeed = 550 # 起跳初速度
    blockSize = 50 # 地图方块大小
    edgeDist = 4 * blockSize # 人物实际活动范围距离左右边界的距离（超过这个距离，就变成地图移动，人物不动）

class BgmSettings():
    defaultvolume = 0.5

class FontSettings():
    FontPath = 'C:\\Windows\\Fonts\\simsun.ttc'  # 华文宋体字体路径