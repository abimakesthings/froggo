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

button = Button(21) #aracade button
led = LED(12) #arcade LED
printer = File(devfile="/dev/usb/lp0")
printer.profile.media["width"]["pixels"] = 384

#initial states
has_printed = False
led.on()
camera = camera_config()
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen.fill((0, 0, 0)) #black background
display_text("Push the button!", screen)

while True:
    if button.is_pressed and not has_printed: #to trigger only once per press
        has_printed = True
        led.off()
        print("Button was pressed")
        photo_id = datetime.now()
        timestamp = photo_id.strftime("%Y-%m-%d-%H-%M-%S")
        display_text("Ready",screen)
        camera.start()
        print("camera started")
        preview_and_countdown(camera, screen)
        print("preview started")
        picture_1=take_picture(camera, timestamp, 1)
        print("Picture 1 captured")
        #show_picture
        preview_and_countdown(camera, screen)
        picture_2=take_picture(camera, timestamp, 2)
        print("Picture 2 captured")
        #show_picture
        preview_and_countdown(camera, screen)
        picture_3=take_picture(camera, timestamp, 3)
        print("Picture 3 captured")
        #show_picture
        preview_and_countdown(camera, screen)
        picture_4=take_picture(camera, timestamp, 4)
        print("Picture 4 captured")
        #show_picture
        camera.stop()
        photostrip = merge(picture_1, picture_2, picture_3, picture_4)
        photostrip.save(f"images/{timestamp}_photostrip.png")
        print("Photostrip created")
        display_text("Printing...",screen)
        #printer.image(f"images/{timestamp}_photostrip.png") #print
        camera.stop()
        sleep(1)
        
    elif not button.is_pressed and has_printed: #button's not pressed
        has_printed = False
        led.on()
        display_text("Push the button!", screen)