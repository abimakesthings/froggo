import pygame
pygame.mixer.init()

shutter_sound = pygame.mixer.Sound("sounds/shutter.MP3")

def take_picture(camera,timestamp,number):
    shutter_sound.play()
    picture_path = f"images/{timestamp}_0{number}.jpg"
    camera.capture_file(picture_path)
    return picture_path
     
