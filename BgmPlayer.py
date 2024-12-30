import pygame
import sys

class BgmPlayer():
    def __init__(self):
        pygame.mixer.init()
    
    def handle(self,event):
        bgm = pygame.mixer.music.load('./assets/Time Flows Ever Onward - Evan Call.mp3')
        pygame.mixer.music.play(-1)
    
    def post(self):
        pass