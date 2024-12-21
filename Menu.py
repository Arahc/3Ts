import pygame
import sys
from GameManager import Listener
from Settings import *

class Menu(Listener):

    def __init__(self, window):
        font = pygame.font.Font(None, 36)
        window.fill(WHITE)
        
        self.StartButton = font.render('Start', True, BLACK)
        self.QuitButton = font.render('Quit', True, BLACK)
        
        StartRect = self.StartButton.get_rect(center=(WindowSettings.width / 2, WindowSettings.height / 2 - 50))
        QuitRect = self.QuitButton.get_rect(center=(WindowSettings.width / 2, WindowSettings.height / 2 + 50))
        
        window.blit(self.StartButton, StartRect)
        window.blit(self.QuitButton, QuitRect)
        
    
    def handle(self, event):
        if (event.type == pygame.MOUSEBUTTONDOWN):
            mouse_x, mouse_y = event.pos
            self.check_mouse_click(mouse_x, mouse_y)

    # 检查鼠标点击
    def check_mouse_click(self, x, y):
        StartRect = self.StartButton.get_rect(center=(WindowSettings.width / 2, WindowSettings.height / 2 - 50))
        QuitRect = self.QuitButton.get_rect(center=(WindowSettings.width / 2, WindowSettings.height / 2 + 50))
        
        if StartRect.collidepoint(x, y):
            print("开始游戏被选中")
            # 这里可以添加开始游戏的代码
        elif QuitRect.collidepoint(x, y):
            print("退出游戏被选中")
            pygame.quit()
            sys.exit()