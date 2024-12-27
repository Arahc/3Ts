import pygame, sys, Menu
from GameSettings import *
from SettingPage import SettingPage
from Utility import BgmPlayer, Scene

class GameManager():


    def __init__(self, window):
        global events, listeners
        self.window = window
        self.clock = pygame.time.Clock()
        self.menu = Menu.Menu(window)
        self.bgmplayer = BgmPlayer()
        self.settingpage = SettingPage(self.bgmplayer)
        listeners = [ self.menu ]
        events = []
        
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
                    elif value == 'QuitSetting':
                        listeners = [ self.menu ]

    def render(self):
        pygame.display.flip()
