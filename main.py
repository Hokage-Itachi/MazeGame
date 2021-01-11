from game.game import Game
import pygame

g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()