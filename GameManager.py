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
    def __init__(self):
        pass

    def handle(self, event):
        pass

    def render(self):
        pass


import Menu
from Settings import *
from BgmPlayer import BgmPlayer


class GameManager:

    global events, listeners

    def __init__(self, window):
        global events, listeners
        self.window = window
        self.clock = pygame.time.Clock()
        menu = Menu.Menu(window)
        listeners = [menu]
        events = []

    def AddEvent(self, event):
        events.append(event)

    def update(self):
        loadevents = pygame.event.get()
        for event in loadevents:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                self.AddEvent(event)

        while len(events) > 0:
            event = events.pop(0)
            for listener in listeners:
                listener.handle(event)

    def render(self):
        pygame.display.flip()
