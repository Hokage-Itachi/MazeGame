from models.maze import Maze
import pygame
import sys
from pygame.locals import *
pygame.init()
FPS = 60
fpsClock = pygame.time.Clock()

WINDOWWIDTH = 500
WINDOWHEIGHT = 500

BG = pygame.image.load('./image/background.png')
BG = pygame.transform.scale(BG, (1000, 500))
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('SCROLL')
grass = pygame.image.load('./image/grass.png')
wall = pygame.image.load('./image/wall.png')
char = pygame.image.load('./image/char.png')


class Background():
    def __init__(self, matrix):
        self.x = 0
        self.y = 0
        self.img = pygame.Surface((len(matrix), len(matrix)))
        self.width = len(matrix) * 70
        self.height = len(matrix) * 70
        self.speed = 3

    def draw(self, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 0:
                    DISPLAYSURF.blit(wall, (j * 70, i * 70))
                else:
                    DISPLAYSURF.blit(grass, (j * 70, i * 70))

    def update(self, player):
        x_camera = player.x - (WINDOWWIDTH/2 - player.width/2)
        if x_camera < 0:
            x_camera = 0
        if x_camera + WINDOWWIDTH > self.width:
            x_camera = self.width - WINDOWWIDTH
        self.x = -x_camera


class Player():
    def __init__(self):
        self.width = 50
        self.height = 40
        self.x = 0
        self.y = 400
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((255, 0, 0))
        self.speed = 5

    def draw(self, bg):
        DISPLAYSURF.blit(
            self.surface, (int(self.x + bg.x), int(self.y + bg.y)))

    def update(self, bg, left, right):
        if left == True:
            self.x -= self.speed
        if right == True:
            self.x += self.speed
        if self.x < 0:
            self.x = 0
        if self.x + self.width > bg.width:
            self.x = bg.width - self.width


def main():
    maze = Maze(10)
    maze.create()
    bg = Background(maze.matrix)
    player = Player()
    left = False
    right = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left = True
                if event.key == pygame.K_RIGHT:
                    right = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left = False
                if event.key == pygame.K_RIGHT:
                    right = False
        bg.draw(maze.matrix)
        player.draw(bg)

        player.update(bg, left, right)
        bg.update(player)
        print(player.x)

        pygame.display.update()
        fpsClock.tick(FPS)


if __name__ == '__main__':
    main()
