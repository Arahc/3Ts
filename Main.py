import pygame
import sys
from Settings import *
from GameManager import GameManager


def main():
    global manager
    pygame.init()
    window = pygame.display.set_mode((WindowSettings.width, WindowSettings.height))
    pygame.display.set_caption(WindowSettings.title)
    manager = GameManager(window)
    while True:
        manager.update()
        manager.render()


if __name__ == "__main__":
    main()
