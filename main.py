from gpiozero import Button, LED
from time import sleep
from picamera2 import Picamera2,  Preview
from datetime import datetime
#from PIL import Image
from photostrip import merge

button = Button(21) #aracade button
led = LED(12) #arcade LED
camera = Picamera2()
camera.configure(camera.create_still_configuration(main={"size": (640, 480)})) #must call before capturing
camera.start()

#initial states
has_printed = False
led.on()

while True:
    if button.is_pressed and not has_printed: #to trigger only once per press
        led.off()
        has_printed = True
        print("Button was pressed")
        photo_id = datetime.now()
        timestamp =  photo_id.strftime("%Y-%m-%d-%H-%M-%S")
        picture_1 = f"images/{timestamp}_01.jpg"
        picture_2 = f"images/{timestamp}_02.jpg"
        picture_3 = f"images/{timestamp}_03.jpg"
        sleep(3) #countdown will go here
        camera.capture_file(picture_1)
        print("Picture 1 captured")
        sleep(3) #countdown will go here
        camera.capture_file(picture_2)
        print("Picture 2 captured")
        sleep(3) #countdown will go here
        camera.capture_file(picture_3)
        print("Picture 3 captured")
        photostrip = merge(picture_1, picture_2, picture_3)
        photostrip.save(f"images/{timestamp}_photostrip.bmp")
        print("Photostrip created")
        
    elif not button.is_pressed and has_printed:
        has_printed = False
        led.on()
