import sys
import pygame
from demo_pygame.src.main.Game import *
from demo_pygame.src.ui.MainMenu import *
from demo_pygame.src.ui.Button import *
pygame.init()

main_menu()

g = Game()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()
