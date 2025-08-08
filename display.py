from PIL import Image, ImageDraw, ImageFont
from time import sleep
import pygame


def display_text(text):
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #fullscreen window
    screen.fill((0, 0, 0)) #black background

    font = pygame.font.Font(None, 100)
    surface = font.render(str(text), True, (255,255,255)) #creates an "image" of the text
    
    #center text
    surface_width, surface_height = surface.get_size()
    x = 240 - surface_width/2 #screen width is 480. 
    y = 160 - surface_height/2 #screen height is 320. 

    screen.blit(surface, (x, y)) #put the "image" onto the center of canvas                 
    pygame.display.flip() #show canvas
    sleep(3)

