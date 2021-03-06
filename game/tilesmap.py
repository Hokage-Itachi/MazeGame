import pygame as pg
from config.settings import *

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip().split())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * BLOCK_SIZE
        self.height = self.tileheight * BLOCK_SIZE

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(SURFACE_WIDTH / 2)
        y = -target.rect.y + int(SURFACE_HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - SURFACE_WIDTH), x)  # right
        y = max(-(self.height - SURFACE_HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)