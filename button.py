from gpiozero import Button
from time import sleep

button = Button(16)
has_printed = False

while True:
    if button.is_pressed and not has_printed:
        print("Button was pressed")
        has_printed = True
        sleep(0.2) #delay to avoid multiple button presses
    elif not button.is_pressed and has_printed:
        has_printed = False
    sleep(0.01) #avoid CPU dying