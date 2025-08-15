#main.py
from gpiozero import Button, LED
from time import sleep
from picamera2 import Picamera2, Preview
from datetime import datetime
from photostrip import merge
from display import display_text
from take_picture import take_picture
from show_picture import show_picture
from escpos.printer import File
from camera_config import camera_config, camera_preview, preview_and_countdown
import pygame

import os
os.environ.setdefault("DISPLAY", ":0")
os.environ.pop("SDL_VIDEODRIVER", None)   # let SDL pick x11 if available
os.system("unclutter -idle 0.01 -root &")
#initial states
button = Button(21) #aracade button
led = LED(12) #arcade LED
printer = File(devfile="/dev/usb/lp0")
printer.profile.media["width"]["pixels"] = 384
has_printed = False
led.on()
camera = camera_config()
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen.fill((0, 0, 0)) #black background
display_text("Push the button!", screen, 90)
pygame.mixer.init()
pygame.mouse.set_visible(False)
printing_sound = pygame.mixer.Sound("sounds/printing.MP3")
button_press_sound = pygame.mixer.Sound("sounds/button_press.MP3")

while True:
    if button.is_pressed and not has_printed: #to trigger only once per press
        has_printed = True
        button_press_sound.play()
        led.off()
        photo_id = datetime.now()
        timestamp = photo_id.strftime("%Y-%m-%d-%H-%M-%S")
        display_text("Ready",screen,150)
        camera.start()
        
        #takes 4 photos. For each, output path with name to array
        pictures=[]
        for i in range(1, 5):
            preview_and_countdown(camera, screen)
            picture=take_picture(camera, timestamp, i)
            show_picture(screen, picture)
            pictures.append(picture) #add to array

        camera.stop()
        photostrip = merge(*pictures) #spread operator
        photostrip.save(f"images/{timestamp}_photostrip.png")
        display_text("Printing...",screen,150)
        printing_sound.play()
        printer.image(f"images/{timestamp}_photostrip.png")
        camera.stop()
        sleep(1)
        
    elif not button.is_pressed and has_printed: #button's not pressed
        has_printed = False
        led.on()
        display_text("Push the button!", screen, 90)