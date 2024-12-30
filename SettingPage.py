import pygame
import sys
from GameSettings import *
from Utility import Scene

class SettingPage(Scene):

    def __init__(self, bgmplayer):
        self.bgmplayer = bgmplayer
        self.volume = BgmSettings.defaultvolume
        # 定义音量条的属性
        self.volume_bar_width = 200
        self.volume_bar_height = 20
        self.volume_bar_x = WindowSettings.width // 2 - self.volume_bar_width // 2
        self.volume_bar_y = WindowSettings.height // 2 - 40
        self.volume_bar_color = BLACK  # 音量条的颜色
        self.volume_bar_fill_color = GREEN  # 音量条填充的颜色

    def show(self, window):
        pygame.display.set_caption("Settings")
        window.fill(WHITE)

        self.volume_bar_pos = int(self.volume_bar_width * self.volume)
        self.draw_volume_bar(window, self.volume)

        font = pygame.font.Font(None, 36)
        self.VolumeButton = font.render('Quit', True, BLACK)
        self.VolumeRect = self.VolumeButton.get_rect(center=(WindowSettings.width / 2, WindowSettings.height / 2 - 80))
        self.QuitButton = font.render('Quit', True, BLACK)
        self.QuitRect = self.QuitButton.get_rect(center=(WindowSettings.width / 2, WindowSettings.height / 2 + 40))
        window.blit(self.QuitButton, self.QuitRect)

    def handle(self, event):
        global bgmplayer
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 检查鼠标点击是否在音量条上
            mouse_x, mouse_y = event.pos
            if (self.volume_bar_x <= mouse_x <= self.volume_bar_x + self.volume_bar_width
                and self.volume_bar_y <= mouse_y <= self.volume_bar_y + self.volume_bar_height ):
                # 计算新的音量值
                new_volume = (mouse_x - self.volume_bar_x) / self.volume_bar_width
                
                self.bgmplayer.set_volume(new_volume)

                self.volume = new_volume
                self.volume_bar_pos = int(self.volume_bar_width * self.volume)

                # just for debug
                print("volume: ", self.volume)
                return None
            elif (self.QuitRect.collidepoint(mouse_x,mouse_y)):
                return 'EnterMenu'
                
    
    def draw_volume_bar(self, window, volume):
        # 绘制音量条
        pygame.draw.rect(window, self.volume_bar_color, (self.volume_bar_x, self.volume_bar_y, self.volume_bar_width, self.volume_bar_height))
        self.volume_bar_pos = int(self.volume_bar_width * volume)
        pygame.draw.rect(window, self.volume_bar_fill_color, (self.volume_bar_x, self.volume_bar_y, self.volume_bar_pos, self.volume_bar_height))
    