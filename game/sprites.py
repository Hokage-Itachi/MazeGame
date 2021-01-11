import pygame
import sys
from config.settings import *
from models.graph import *
from models.maze import * 


class Player(pygame.sprite.Sprite):
    def __init__(self,game, x, y) -> None:
        super().__init__()
        self.game = game
        self.image = pygame.image.load('./image/char.png')
        self.rect = self.image.get_rect()
        self.x = x * BLOCK_SIZE
        self.y = y * BLOCK_SIZE
        self.vx, self.vy = 0, 0

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.vx = -CHARACTERS_SPEED
        if keys[pygame.K_RIGHT]:
            self.vx = CHARACTERS_SPEED
        if keys[pygame.K_UP]:
            self.vy = -CHARACTERS_SPEED
        if keys[pygame.K_DOWN]:
            self.vy = CHARACTERS_SPEED
        # if self.vx != 0 and self.vy != 0:
        #     self.vx *= 0.7071
        #     self.vy *= 0.7071

    def update(self):
        self.get_keys()
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
        print("Log:",self.rect.x, self.rect.y)
        
    
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # self.groups = game.all_sprites, game.walls
        super().__init__()
        self.image = pygame.image.load('./image/wall.png')
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * BLOCK_SIZE
        self.rect.y = y * BLOCK_SIZE
        
class Grass(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # self.groups = game.all_sprites, game.grass
        super().__init__()
        self.image = pygame.image.load('./image/grass.png')
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * BLOCK_SIZE
        self.rect.y = y * BLOCK_SIZE
