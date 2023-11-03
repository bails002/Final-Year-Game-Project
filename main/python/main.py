import pygame
import sys

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 5)
display_width = 800
display_height = 600
# create screen
screen = pygame.display.set_mode((display_width, display_height))

while True:
    pygame.display.set_caption("adventure game")
    window = screen
    window.fill((255,255,255))