import pygame

# This is a dictionary that contains all the settings for the game.
# It allows you to easily change settings without having to change the code repeatedly.

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class WindowSettings():
    width = 1280
    height = 720
    title = "demo"
    fps = 60

class BgmSettings():
    defaultvolume = 0.5
