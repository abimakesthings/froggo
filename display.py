#display.py
from time import sleep
import pygame

pygame.mixer.init()
ready_sound = pygame.mixer.Sound("sounds/ready.MP3")

def display_text(text, screen, font_size):
    screen.fill((0, 0, 0)) #black background
    font = pygame.font.SysFont("quicksand medium", font_size)
    surface = font.render(str(text), True, (255,255,255)) #creates an "image" of the text
    
    #center text
    surface_width, surface_height = surface.get_size()
    x = 400 - surface_width/2 #screen width is 800
    y = 240 - surface_height/2 #screen height is 480
    screen.blit(surface, (x, y)) #put the "image" onto the center of canvas                 
    pygame.display.flip() #show canvas
    pygame.time.wait(800)
    if text == "Ready":
        ready_sound.play()
    pygame.time.wait(2200)

def countdown_text(text, screen):
    font = pygame.font.SysFont("quicksand medium", 140)
    surface = font.render(str(text), True, (255, 255, 255))#creates an "image" of the text
    surface.set_alpha(128) #0 = fully transparent, 255 = fully opaque)

    #place surface in screen "canvas"
    surface_width, surface_height = surface.get_size()
    x = 400 - surface_width/2 #screen width is 800
    screen.blit(surface, (x, 300))
