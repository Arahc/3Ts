import pygame
import sys
from GameSettings import *

pygame.init()

fps = WindowSettings.fps
clock = pygame.time.Clock()

# 设置背景
width = WindowSettings.width
height = WindowSettings.height
window = pygame.display.set_mode((width, height))

# 移动主循环
while True:
    lst=pygame.event.get()
    for event in lst:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if (len(lst)>0):
        print(lst)