import pygame as pg
import sys
from os import path
from config.settings import *
from game.sprites import *
from game.tilesmap import *
from models.maze import *
import pygame_menu

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.maze_size = 10
        
        

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map = Map('map.txt')

    def new(self):
        self.maze = Maze(self.maze_size)
        self.maze.create()
        self.load_data()
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.grasses = pg.sprite.Group()
        self.footprints = pg.sprite.Group()
        matrix = self.maze.matrix
        for row in range(len(matrix)):
            for col in range(len(matrix)):
                if(matrix[row][col] == 0):
                    Wall(self, col, row)
                else:
                    Grass(self, col, row)
        
        self.hint = False
        self.player = Player(self, 1, 0)
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw(self):
        # self.draw_grid()
        
        
            # self.player = Player(self, self.player.x // 70, self.player.y // 70)
        for wall in self.walls:
            self.screen.blit(wall.image, self.camera.apply(wall))
        for grass in self.grasses:
            self.screen.blit(grass.image, self.camera.apply(grass))
        if(self.hint == True):
            for footprint in self.footprints:
                self.screen.blit(footprint.image, self.camera.apply(footprint))
        self.screen.blit(self.player.image, self.camera.apply(self.player))
        
        # for sprite in self.all_sprites:
        #     self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
                
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.show_start_screen()
                if event.key == pg.K_h:
                    self.show_hint()
    
    def show_start_screen(self):
        # print(pg.font.get_fonts())
        menu = pygame_menu.Menu(300, 500, 'Welcome to Maze Runner',
                       theme=pygame_menu.themes.THEME_BLUE)

        # menu.add_text_input('Name :', default='John Doe')
        menu.add_selector('Difficulty :', [('Easy', 1), ('Medium', 2), ('Hard', 3)], onchange=self.set_difficulty)
        menu.add_button('Play', self.start_the_game)
        menu.add_button('Help', self.show_help_screen)
        menu.add_button('Quit', pygame_menu.events.EXIT)
        menu.mainloop(self.screen)

    def show_help_screen(self):
        self.screen = pg.display.set_mode((500, 300))
        self.screen.fill(WHITE)
        font = pg.font.SysFont("arialblack", 15)
        text = font.render('GeeksForGeeks', True, BLACK, WHITE)
        textRect = text.get_rect()
        textRect.center = (100, 10)
        while True:
            self.screen.blit(text, textRect)
            pg.display.update()
            self.events()

    def set_difficulty(self, value, difficulty):
   
        print("Difficulty:", difficulty)
        if(difficulty == 1):
            self.maze_size = 10
        elif(difficulty == 3):
            self.maze_size = 30
        else:
            self.maze_size = 20
        print("Maze Size:", self.maze_size)
    
    def show_hint(self):
        current_pos = [self.player.x // BLOCK_SIZE, self.player.y // BLOCK_SIZE]
        self.maze.add_path_to_matrix(self.maze.findPath(current_pos, [self.maze.size - 1, self.maze.size - 2]))
        self.hint = True
        matrix = self.maze.matrix
        for row in range(len(matrix)):
            for col in range(len(matrix)):
                if(matrix[row][col] == "w"):
                    Footprint(self, col, row, "w")
                if(matrix[row][col] == "s"):
                    Footprint(self, col, row, "s")
                if(matrix[row][col] == "a"):
                    Footprint(self, col, row, "a")
                if(matrix[row][col] == "d"):
                    Footprint(self, col, row, "d")
    def start_the_game(self):    
        self.screen = pg.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))
        while True:
            self.new()
            self.run()
# create the game object
