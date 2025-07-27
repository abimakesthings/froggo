from gpiozero import Button
from picamera import PiCamera
from datetime import datetime
from signal import pause

button = Button(16)
camera = PiCamera()

while True:
    if button.is_pressed:
        print("Button is pressed")
    else:
        print("Button is not pressed")

def capture():
    camera.capture(f'/home/pi/{datetime.now():%Y-%m-%d-%H-%M-%S}.jpg')

button.when_pressed = capture

pause()