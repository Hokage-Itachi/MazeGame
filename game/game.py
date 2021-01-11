import pygame
import sys
from config.settings import *
from models.graph import *
from models.maze import *
from game.tilesmap import *
from game.sprites import *

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.maze = Maze(MAZE_SIZE)
        self.maze.create()
        self.maze.print_to_file()
        self.map = Map('map.txt')
        

    def new(self):

        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        # self.grass = pygame.sprite.Group()
        for row in range(len(self.map.data)):
            for col in range(len(self.map.data)):
                if self.map.data[row][col] == '0':
                    self.all_sprites.add(Wall(col, row))
                    self.walls.add(Wall(col, row))
                if self.map.data[row][col] == '4':
                    # self.grass.add(Grass(col, row))
                    self.all_sprites.add(Grass(col, row))
                if(self.map.data[row][col] == '1'):
                    # self.grass.add(Grass(col, row))
                    self.all_sprites.add(Grass(col, row))
        self.player = Player(self, 1, 0)
        self.all_sprites.add(self.player)
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
            self.update()
            self.draw()
