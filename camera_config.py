# camera_config.py
from picamera2 import Picamera2
from libcamera import Transform
from display import countdown_text
import pygame
import numpy as np

pygame.mixer.init()

#camera config
def camera_config() -> Picamera2:
    camera = Picamera2()
    camera.configure(camera.create_preview_configuration(
        main={"size": (800, 480), "format": "RGB888"},
        transform=Transform(rotation=0),
    ))
    return camera

def camera_preview(camera, screen):
    frame = camera.capture_array()
    
    # Convert BGR to grayscale using luminosity method
    gray = (0.299 * frame[:, :, 2] + 0.587 * frame[:, :, 1] + 0.114 * frame[:, :, 0]).astype(np.uint8)
    frame = np.stack([gray] * 3, axis=-1)  # Convert to 3-channel grayscale

    h, w = frame.shape[:2]
    frame_surface = pygame.image.frombuffer(frame.tobytes(), (w, h), "RGB")
    if (w, h) != screen.get_size():
        frame_surface = pygame.transform.smoothscale(frame_surface, screen.get_size())
    screen.blit(frame_surface, (0, 0))

def preview_and_countdown(camera, screen):
    sounds = {
        3: pygame.mixer.Sound("sounds/1.MP3"),
        2: pygame.mixer.Sound("sounds/2.MP3"),
        1: pygame.mixer.Sound("sounds/3.MP3"),
    }

    for i in range(3, 0, -1): #for (let i = 3; i > 0; i--)
        sounds[i].play()
        end = pygame.time.get_ticks() + 1000
        while pygame.time.get_ticks() < end:
            camera_preview(camera, screen)
            countdown_text(i, screen)
            pygame.display.flip()
