import pygame as pg
import sys
from os import path
from config.settings import *
from game.sprites import *
from game.tilesmap import *
from models.maze import *
import pygame_menu
import time

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.maze_size = 15
        
        # self.time = 30
        pg.time.set_timer(pg.USEREVENT, 1000)
        
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map = Map('map.txt')

    def new(self):
        self.maze = Maze(self.maze_size)
        self.maze.create()
        self.load_data()
        self.time = self.maze_size * 2
        self.is_winner = False
        self.is_loser = False    
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
        if(self.player.x  >= self.camera.width - BLOCK_SIZE):
            self.is_winner = True
        if(self.time <= 0):
            self.is_loser = True

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
        
        self.end = End(self, self.maze.size - 1, self.maze.size - 2)
        self.screen.blit(self.end.image, self.camera.apply(self.end))
        
        self.start = Start(self, 1, 0)
        self.screen.blit(self.start.image, self.camera.apply(self.start))
        
        self.screen.blit(self.player.image, self.camera.apply(self.player))
        # Draw time
        self.screen.blit(pg.font.Font(None, 36).render(str(self.time), True, WHITE), (SURFACE_WIDTH - 36, 10))
        
        
        if(self.is_winner):
            font = pg.font.Font(None, 36)
            text_1 = font.render("Amazing, Good Job....", True, WHITE)
            text_1_rect = text_1.get_rect()
            text_1_x = self.screen.get_width() / 2 - text_1_rect.width / 2
            text_1_y = self.screen.get_height() / 2 - text_1_rect.height / 2
            self.screen.blit(text_1, [text_1_x, text_1_y])
            
            text_2 = font.render("Press \"Esc\"", True, WHITE)
            text_2_rect = text_2.get_rect()
            text_2_x = self.screen.get_width() / 2 - text_2_rect.width / 2 
            text_2_y = self.screen.get_height() / 2 - text_2_rect.height / 2 + 30
            self.screen.blit(text_2, [text_2_x, text_2_y])
        if(self.is_loser):
            font = pg.font.Font(None, 36)
            text_1 = font.render("Oh no, Oh no, Oh no no no no....", True, WHITE)
            text_1_rect = text_1.get_rect()
            text_1_x = self.screen.get_width() / 2 - text_1_rect.width / 2
            text_1_y = self.screen.get_height() / 2 - text_1_rect.height / 2
            self.screen.blit(text_1, [text_1_x, text_1_y])
            
            text_2 = font.render("Press \"Esc\"", True, WHITE)
            text_2_rect = text_2.get_rect()
            text_2_x = self.screen.get_width() / 2 - text_2_rect.width / 2 
            text_2_y = self.screen.get_height() / 2 - text_2_rect.height / 2 + 30
            self.screen.blit(text_2, [text_2_x, text_2_y])
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.USEREVENT:
                if(not self.is_winner and not self.is_loser):
                    self.time -= 1
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.show_start_screen()
                if event.key == pg.K_h:
                    self.show_hint()
    
    def show_start_screen(self):
        # print(pg.font.get_fonts())
        menu = pygame_menu.Menu(300, 550, 'Welcome to Maze Runner',
                       theme=pygame_menu.themes.THEME_GREEN)

        # menu.add_text_input('Name :', default='John Doe')
        menu.add_selector('Difficulty', [('Easy', 1), ('Medium', 2), ('Hard', 3)], onchange=self.set_difficulty)
        menu.add_button('Play', self.start_the_game)
        menu.add_button('Help', self.show_help_screen)
        menu.add_button('Quit', pygame_menu.events.EXIT)
        menu.mainloop(self.screen)

    def show_help_screen(self):
        self.screen = pg.display.set_mode((500, 300))
        self.screen.fill(WHITE)
        font = pg.font.SysFont("None", 20)
        text = font.render('How to play?', True, BLACK, WHITE)
        textRect = text.get_rect()
        textRect.center = (40, 10)
        
        tutor_1 = "1. Use (A, W, S, D) or (left, right, up, down) arrow to move the character."
        tutor_2 = "2. Click \"H\" to show the hint about the path."
        tutor_3 = " 3. Click \"Esc\" to return to start menu."
        tutor_1_text = pg.font.SysFont("None", 15).render(tutor_1, True, BLACK, WHITE)
        tutor_1_text_rect = text.get_rect()
        tutor_1_text_rect.center= (100, 30)
        
        tutor_2_text = pg.font.SysFont("None", 15).render(tutor_2, True, BLACK, WHITE)
        tutor_2_text_rect = text.get_rect()
        tutor_2_text_rect.center= (100, 40)
        
        tutor_3_text = pg.font.SysFont("None", 15).render(tutor_3, True, BLACK, WHITE)
        tutor_3_text_rect = text.get_rect()
        tutor_3_text_rect.center= (97, 50)
        while True:
            self.screen.blit(text, textRect)
            self.screen.blit(tutor_1_text, tutor_1_text_rect)
            self.screen.blit(tutor_2_text, tutor_2_text_rect)
            self.screen.blit(tutor_3_text, tutor_3_text_rect)
            pg.display.update()
            self.events()

    def set_difficulty(self, value, difficulty):
   
        print("Difficulty:", difficulty)
        if(difficulty == 1):
            self.maze_size = 15
        elif(difficulty == 3):
            self.maze_size = 40
        else:
            self.maze_size = 25
        print("Maze Size:", self.maze_size)
    
    def show_hint(self):
        current_pos = [self.player.x // BLOCK_SIZE, self.player.y // BLOCK_SIZE]
        self.maze.add_path_to_matrix(self.maze.findPath(current_pos, [self.maze.size - 1, self.maze.size - 2]))
        # self.maze.print_to_file("output.txt")
        # print(self.maze.matrix)
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
        
        self.new()
        self.run()
# create the game object
