import pygame
import sys
from GameSettings import *
from Utility import Scene

class Menu(Scene):

    def __init__(self, window):
        pass
    
    def show(self, window):
        window.fill(WHITE)
        font = pygame.font.Font(None, 36)
        
        self.StartButton = font.render('Start', True, BLACK)
        self.SettingButton = font.render('Settings', True, BLACK)
        self.HelpButton = font.render('Help', True, BLACK)
        self.QuitButton = font.render('Quit', True, BLACK)
        
        StartRect = self.StartButton.get_rect(center=(WindowSettings.width / 2, WindowSettings.height / 2 - 120))
        SettingRect = self.SettingButton.get_rect(center=(WindowSettings.width / 2, WindowSettings.height / 2 - 40))
        HelpRect = self.HelpButton.get_rect(center=(WindowSettings.width / 2, WindowSettings.height / 2 + 40))
        QuitRect = self.QuitButton.get_rect(center=(WindowSettings.width / 2, WindowSettings.height / 2 + 120))
        
        window.blit(self.StartButton, StartRect)
        window.blit(self.SettingButton, SettingRect)
        window.blit(self.HelpButton, HelpRect)
        window.blit(self.QuitButton, QuitRect)

    def handle(self, event):
        if (event.type == pygame.MOUSEBUTTONDOWN):
            mouse_x, mouse_y = event.pos
            return self.check_mouse_click(mouse_x, mouse_y)

    # 检查鼠标点击
    def check_mouse_click(self, x, y):
        StartRect = self.StartButton.get_rect(center=(WindowSettings.width / 2, WindowSettings.height / 2 - 120))
        SettingRect = self.SettingButton.get_rect(center=(WindowSettings.width / 2, WindowSettings.height / 2 - 40))
        HelpRect = self.HelpButton.get_rect(center=(WindowSettings.width / 2, WindowSettings.height / 2 + 40))
        QuitRect = self.QuitButton.get_rect(center=(WindowSettings.width / 2, WindowSettings.height / 2 + 120))
        
        if StartRect.collidepoint(x, y):
            return 'EnterGame'
        elif SettingRect.collidepoint(x, y):
            return 'EnterSetting'
        elif HelpRect.collidepoint(x, y):
            return 'EnterHelp'
        elif QuitRect.collidepoint(x, y):
            print("See you next time!")
            pygame.quit()
            sys.exit()