import pygame
import sys

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

import Menu
from GameSettings import *
from SettingPage import SettingPage
# from BgmPlayer import BgmPlayer

class GameManager():

    global events, listeners

    def __init__(self, window):
        global events, listeners
        self.window = window
        self.clock = pygame.time.Clock()
        menu = Menu.Menu(window)
        self.settingpage = SettingPage()
        listeners = [menu]
        events = []
        
        bgm = pygame.mixer.music.load('./assets/bgm/Time Flows Ever Onward - Evan Call.mp3')
        pygame.mixer.music.play(-1)

    def AddEvent(self, event):
        events.append(event)

    def update(self):
        global events, listeners
        loadevents = pygame.event.get()
        for event in loadevents:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                self.AddEvent(event)

        # show scenes
        for listener in listeners:
            if (isinstance(listener, Scene)):
                listener.show(self.window)
        
        # handle events
        while len(events) > 0:
            event = events.pop(0)
            for listener in listeners:
                value = listener.handle(event)
                if value != None:
                    if value == 'EnterGame':
                        print("EnterGame")
                    elif value == 'EnterSetting':
                        print("EnterSetting")
                        listeners = [ self.settingpage ]
                    elif value == 'EnterHelp':
                        print("EnterHelp")
                    else:
                        print("Unknown command")

    def render(self):
        pygame.display.flip()
