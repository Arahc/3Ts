import pygame
import sys
from GameSettings import *
from GameManager import Scene
from BgmPlayer import BgmPlayer

class SettingPage(Scene):
    def __init__(self):
        self.volume = 0.5
        # 定义音量条的属性
        self.volume_bar_x = 50
        self.volume_bar_y = 50
        self.volume_bar_width = 200
        self.volume_bar_height = 20
        self.volume_bar_color = (0, 0, 0)  # 音量条的颜色
        self.volume_bar_fill_color = (255, 0, 0)  # 音量条填充的颜色

    def show(self, window):
        pygame.display.set_caption("Settings")
        window.fill(WHITE)
        pygame.mixer.music.set_volume(self.volume)

        # 定义音量条的当前位置
        self.volume_bar_pos = int(self.volume_bar_width * self.volume)
        self.draw_volume_bar(window, self.volume)

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 检查鼠标点击是否在音量条上
            if (self.volume_bar_x <= event.pos[0] <= self.volume_bar_x + self.volume_bar_width
                and self.volume_bar_y <= event.pos[1] <= self.volume_bar_y + self.volume_bar_height ):
                # 计算新的音量值
                new_volume = (event.pos[0] - self.volume_bar_x) / self.volume_bar_width
                
                pygame.mixer.music.set_volume(new_volume)

                self.volume = new_volume
                self.volume_bar_pos = int(self.volume_bar_width * self.volume)
                print("volume: ", self.volume)
    
    def draw_volume_bar(self, window, volume):
        # 绘制音量条
        pygame.draw.rect(window, self.volume_bar_color, (self.volume_bar_x, self.volume_bar_y, self.volume_bar_width, self.volume_bar_height))
        self.volume_bar_pos = int(self.volume_bar_width * volume)
        pygame.draw.rect(window, self.volume_bar_fill_color, (self.volume_bar_x, self.volume_bar_y, self.volume_bar_pos, self.volume_bar_height))
    