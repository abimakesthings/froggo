from gpiozero import Button
from time import sleep
from picamera2 import Picamera2
from datetime import datetime

button = Button(16)
camera = Picamera2()
camera.start()
has_printed = False

while True:
    if button.is_pressed and not has_printed: #to trigger only once per press
        has_printed = True
        print("Button was pressed")
        photo_id = datetime.now()
        sleep(3) #countdown will go here
        camera.capture_file(f"images/{photo_id:%Y-%m-%d-%H-%M-%S}_01.jpg")
        sleep(3) #countdown will go here
        camera.capture_file(f"images/{photo_id:%Y-%m-%d-%H-%M-%S}_02.jpg")
        sleep(3) #countdown will go here
        camera.capture_file(f"images/{photo_id:%Y-%m-%d-%H-%M-%S}_03.jpg")
        print("3 pictures captured")
    elif not button.is_pressed and has_printed:
        has_printed = False
