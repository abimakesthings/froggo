from gpiozero import Button
from time import sleep
from picamera import PiCamera
from datetime import datetime


button = Button(16)
camera = PiCamera()

has_printed = False

while True:
    if button.is_pressed and not has_printed: #to trigger only once per press
        print("Button was pressed")
        camera.capture(f'im/{datetime.now():%Y-%m-%d-%H-%M-%S}.jpg')
        has_printed = True
        sleep(0.2) #delay to avoid multiple button presses
    elif not button.is_pressed and has_printed:
        has_printed = False
    sleep(0.01) #avoid CPU dying