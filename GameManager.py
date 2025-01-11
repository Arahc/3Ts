import pygame, sys, Menu, ChatBox
from GameSettings import *
from SettingPage import SettingPage
from MapPage import MapPage
from Utility import BgmPlayer, Scene
from Player import Player

class GameManager():

    def __init__(self, window):
        global events, listeners
        self.window = window
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.menu = Menu.Menu(window)
        self.bgmplayer = BgmPlayer()
        self.settingpage = SettingPage(self.bgmplayer)
        self.mappage = MapPage(self.player)
        self.chatboxes = { 'Seer': ChatBox.ChatBox('Seer') }
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

        for i in range(len(listeners)):
            listener = listeners[i]
            # show scenes
            if (isinstance(listener, Scene)):
                listener.show(self.window)
            
            # deal with scenes
            if ((isinstance(listener, MapPage)) and (i == len(listeners) - 1)):
                listener.move()

        # handle events
        while len(events) > 0:
            event = events.pop(0)
            listener = listeners[-1]
            value = listener.handle(event)
            if value != None:
                if value == 'EnterMap':
                    print('EnterMap')
                    listeners=[ self.mappage ]
                    self.bgmplayer.switch('Map')
                elif value == 'EnterSetting':
                    print('EnterSetting')
                    listeners = [ self.settingpage ]
                elif value == 'EnterHelp':
                    print('EnterHelp')
                elif value == 'EnterMenufromSettings':
                    listeners = [ self.menu ]
                elif value == 'EnterMenufromMap':
                    self.bgmplayer.switch('Menu')
                    listeners = [ self.menu ]
                elif (isinstance(value, tuple)) and (value[0] == 'EnterChat'):
                    listeners.append(self.chatboxes[value[1]]) # ChatBox 的渲染应该在最后
                    print('EnterChat')
                elif (isinstance(value, tuple)) and (value[0] == 'EndChat'):
                    listeners.remove(self.chatboxes[value[1]])
                    print('EndChat')

    def render(self):
        pygame.display.flip()
