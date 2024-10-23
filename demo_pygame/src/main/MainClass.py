import sys
import pygame
from BTL_Python_Nhom7.demo_pygame.src.main.Game import Game

g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()
