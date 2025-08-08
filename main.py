from gpiozero import Button, LED
from time import sleep
from picamera2 import Picamera2,  Preview
from datetime import datetime
#from PIL import Image
from photostrip import merge
from escpos.printer import File
#from adafruit_thermal_printer import get_printer_class
#import serial

button = Button(21) #aracade button
led = LED(12) #arcade LED
camera = Picamera2()
camera.configure(camera.create_still_configuration(main={"size": (640, 480)})) #must call before capturing
camera.start()
#ThermalPrinter = get_printer_class(1.00)
#uart = serial.Serial("/dev/usb/lp0", baudrate=9600, timeout=3)
#printer = ThermalPrinter(uart, auto_warm_up=False) #save battery

#initial states
has_printed = False
led.on()


while True:
    if button.is_pressed and not has_printed: #to trigger only once per press
        has_printed = True
        led.off()
        #printer.wake() 
        print("Button was pressed")
        photo_id = datetime.now()
        timestamp =  photo_id.strftime("%Y-%m-%d-%H-%M-%S")
        picture_1 = f"images/{timestamp}_01.jpg"
        picture_2 = f"images/{timestamp}_02.jpg"
        picture_3 = f"images/{timestamp}_03.jpg"
        picture_4 = f"images/{timestamp}_04.jpg"
        sleep(3) #countdown will go here
        camera.capture_file(picture_1)
        print("Picture 1 captured")
        sleep(3) #countdown will go here
        camera.capture_file(picture_2)
        print("Picture 2 captured")
        sleep(3) #countdown will go here
        camera.capture_file(picture_3)
        print("Picture 3 captured")
        camera.capture_file(picture_4)
        print("Picture 4 captured")
        photostrip = merge(picture_1, picture_2, picture_3, picture_4)
        photostrip.save(f"images/{timestamp}_photostrip.png")
        print("Photostrip created")
        p = File(devfile="/dev/usb/lp0")
        p.image(f"images/{timestamp}_photostrip.png")
        
    elif not button.is_pressed and has_printed:
        has_printed = False
        led.on()
        #printer.sleep() #off to save battery
