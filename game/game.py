import pygame
import sys
from config.settings import *
from models.graph import *
from models.maze import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game) -> None:
        super().__init__()
        self.group = game.all_sprites
        self.game = game
        self.image = pygame.image.load('./image/char.png')
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0
        self.vx, self.vy = 0, 0

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_LEFT]:
            self.vx = -CHARACTERS_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_RIGHT]:
            self.vx = CHARACTERS_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_UP]:
            self.vy = -CHARACTERS_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_DOWN]:
            self.vy = CHARACTERS_SPEED
        # if self.vx != 0 and self.vy != 0:
        #     self.vx *= 0.7071
        #     self.vy *= 0.7071

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
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


class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load('./image/wall.png')
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * BLOCK_SIZE
        self.rect.y = y * BLOCK_SIZE


class Grass(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.grass
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load('./image/grass.png')
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * BLOCK_SIZE
        self.rect.y = y * BLOCK_SIZE


class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * BLOCK_SIZE
        self.height = self.tileheight * BLOCK_SIZE


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
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
        self.camera = pygame.Rect(x, y, self.width, self.height)


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.maze = Maze(MAZE_SIZE)

    def load_data(self):
        self.map = Map("map.txt")

    def new(self):

        self.all_sprites = pygame.sprite.Group()
        self.maze.create()
        self.maze.print_to_file()
        self.walls = pygame.sprite.Group()
        self.grass = pygame.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '0':
                    Wall(self, col, row)
                if tile == '4':
                    self.player = Player(self, col, row)
                if(tile == '1'):
                    Grass(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)

    def draw(self):
        self.screen.fill((20, 20, 20))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pygame.display.flip()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
