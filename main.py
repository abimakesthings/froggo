#main.py
from gpiozero import Button, LED
from time import sleep
from picamera2 import Picamera2, Preview
from datetime import datetime
from photostrip import merge
from display import display_text
from countdown import countdown_and_capture
from escpos.printer import File

import os
os.environ.setdefault("DISPLAY", ":0")
os.environ.pop("SDL_VIDEODRIVER", None)   # let SDL pick x11 if available

import pygame

button = Button(21) #aracade button
led = LED(12) #arcade LED
camera = Picamera2()

camera.configure(
    camera.create_still_configuration(
        main={"size": (640, 480)},                          # for your saved photos
        lores={"size": (480, 320), "format": "YUV420"},     # lores MUST be YUV
        display="lores"                                     # <- preview this
    )
)
printer = File(devfile="/dev/usb/lp0")
printer.profile.media["width"]["pixels"] = 384

#initial states
has_printed = False
led.on()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #fullscreen window
screen.fill((0, 0, 0)) #black background


while True:
    if button.is_pressed and not has_printed: #to trigger only once per press
        has_printed = True
        led.off()
        print("Button was pressed")
        photo_id = datetime.now()
        timestamp =  photo_id.strftime("%Y-%m-%d-%H-%M-%S")
        picture_1 = f"images/{timestamp}_01.jpg"
        picture_2 = f"images/{timestamp}_02.jpg"
        picture_3 = f"images/{timestamp}_03.jpg"
        picture_4 = f"images/{timestamp}_04.jpg"
        pygame.init()
        camera.start()
        print("camera started")
        camera.stop_preview() #prevent event loop error
        print("fake preview stopped")
        display_text("Ready")
        pygame.display.quit()
        camera.start_preview(Preview.QT)
        print("preview started")
        countdown_and_capture(camera, picture_1) #countdown will go here
        print("Picture 1 captured")
        camera.capture_file(picture_2)
        print("Picture 2 captured")
        sleep(3)
        camera.capture_file(picture_3)
        print("Picture 3 captured")
        sleep(3) #countdown will go here
        camera.capture_file(picture_4)
        print("Picture 4 captured")
        photostrip = merge(picture_1, picture_2, picture_3, picture_4)
        photostrip.save(f"images/{timestamp}_photostrip.png")
        print("Photostrip created")
        pygame.display.init()
        display_text("Printing...")
        #printer.image(f"images/{timestamp}_photostrip.png") #print
        camera.stop()
        sleep(1)
        
    elif not button.is_pressed and has_printed: #button's not pressed
        has_printed = False
        led.on()
        camera.stop() #do i need this as a failsafe? 