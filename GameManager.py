import pygame, sys, Menu
from GameSettings import *
from SettingPage import SettingPage
from MapPage import MapPage
from Utility import BgmPlayer, Scene

class GameManager():

    def __init__(self, window):
        global events, listeners
        self.window = window
        self.clock = pygame.time.Clock()
        self.menu = Menu.Menu(window)
        self.bgmplayer = BgmPlayer()
        self.settingpage = SettingPage(self.bgmplayer)
        self.mappage = MapPage()
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

        for listener in listeners:
            # show scenes
            if (isinstance(listener, Scene)):
                listener.show(self.window)
            
            # deal with scenes
            if (isinstance(listener, MapPage)):
                listener.move()

        # handle events
        while len(events) > 0:
            event = events.pop(0)
            for listener in listeners:
                value = listener.handle(event)
                if value != None:
                    if value == 'EnterMap':
                        print("EnterMap")
                        listeners=[ self.mappage ]
                    elif value == 'EnterSetting':
                        print("EnterSetting")
                        listeners = [ self.settingpage ]
                    elif value == 'EnterHelp':
                        print("EnterHelp")
                    elif value == 'EnterMenu':
                        listeners = [ self.menu ]

    def render(self):
        pygame.display.flip()
