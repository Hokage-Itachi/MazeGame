import pygame as pg
from config.settings import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.imgs = []
        self.imgs.append(pg.image.load("./image/right_char.png").convert_alpha())

        self.current_img = 0;
        self.game = game
        self.image = self.imgs[self.current_img]
        # self.image.blit(YELLOW)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * BLOCK_SIZE
        self.y = y * BLOCK_SIZE

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if(not self.game.is_winner and not self.game.is_loser):
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.vx = -CHARACTERS_SPEED
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.vx = CHARACTERS_SPEED
            if keys[pg.K_UP] or keys[pg.K_w]:
                self.vy = -CHARACTERS_SPEED
            if keys[pg.K_DOWN] or keys[pg.K_s]:
                self.vy = CHARACTERS_SPEED
        # if self.vx != 0 and self.vy != 0:
        #     self.vx *= 0.7071
        #     self.vy *= 0.7071

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def update(self):
        self.get_keys()
        if(self.vx < 0):
            self.image = (pg.image.load("./image/left_char.png").convert_alpha())
        if (self.vx > 0):
            self.image = (pg.image.load("./image/right_char.png").convert_alpha())
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        if(self.y < 0):
            self.y = 0
        
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("./image/wall_1.jpg")
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * BLOCK_SIZE
        self.rect.y = y * BLOCK_SIZE
        
class Grass(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.grasses
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("./image/grass.jpg")
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * BLOCK_SIZE
        self.rect.y = y * BLOCK_SIZE
class Footprint(pg.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        self.groups = game.all_sprites, game.footprints
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if(direction == "w"):
            self.image = pg.image.load("./image/footprint_up.png")
        elif (direction == "s"):
            self.image = pg.image.load("./image/footprint_down.png")
        elif (direction == "a"):
            self.image = pg.image.load("./image/footprint_left.png")
        else:
            self.image = pg.image.load("./image/footprint_right.png")
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * BLOCK_SIZE
        self.rect.y = y * BLOCK_SIZE
class End(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("./image/end.png").convert_alpha()
        # self.image.blit(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x * BLOCK_SIZE
        self.y = y * BLOCK_SIZE
        self.rect.x = self.x
        self.rect.y = self.y

class Start(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("./image/start.jpg").convert_alpha()
        # self.image.blit(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x * BLOCK_SIZE
        self.y = y * BLOCK_SIZE
        self.rect.x = self.x
        self.rect.y = self.y