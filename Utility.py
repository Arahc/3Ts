import pygame
import sys
from GameSettings import *

class Listener:
    def __init__(self):
        pass

    def handle(self, event):
        pass

    def post(self):
        pass

class Entity(Listener):
    def __init__(self, image, rect):
        self.image = image
        self.rect = rect

    def handle(self, event):
        pass

    def render(self):
        pygame.windows.blit(self.image, self.rect)

class Scene(Listener):
    def __init__(self):
        pass

    def handle(self, event):
        pass

    def render(self):
        pass

class BgmPlayer():
    def __init__(self):
        pygame.mixer.init()
        bgm = pygame.mixer.music.load('./assets/bgm/Time Flows Ever Onward - Evan Call.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(BgmSettings.defaultvolume)
    
    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def post(self):
        pass