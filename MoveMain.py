'''
这是地图移动的主函数
'''

import pygame
import sys
import Map
from GameSettings import *
import Move

pygame.init()

fps = WindowSettings.fps
clock = pygame.time.Clock()

# 设置背景
width = WindowSettings.width
height = WindowSettings.height
screen = pygame.display.set_mode((width, height))
background = pygame.image.load(r".\assets\background.png")
background = pygame.transform.scale(background, (width, height))

# Move初始化
Move.init()

# 移动主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    Move.move()

    screen.blit(background, (0, 0))
    Move.draw(screen)

    pygame.display.flip()
    clock.tick(fps)