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
    fps = 60
    playerHeight = 70 # ����߶�
    playerWidth = 35 # ������
    speed = 6 # �����ƶ��ٶ�
    gravity = 900 # �������ٶ�
    initialSpeed = 600 # �������ٶ�
    blockSize = 50 # ��ͼ�����С
    edgeDist = 4 * blockSize # ����ʵ�ʻ��Χ�������ұ߽�ľ��루����������룬�ͱ�ɵ�ͼ�ƶ������ﲻ����

class BgmSettings():
    defaultvolume = 0.5
