# camera_config.py
from picamera2 import Picamera2
from libcamera import Transform
from display import countdown_text
import pygame

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
    frame = frame[:, :, ::-1].copy()  #swap blues and reds to fix skin being blue
    h, w = frame.shape[:2]
    frame_surface = pygame.image.frombuffer(frame.tobytes(), (w, h), "RGB")
    if (w, h) != screen.get_size():
        frame_surface = pygame.transform.smoothscale(frame_surface, screen.get_size())
    screen.blit(frame_surface, (0, 0))

def preview_and_countdown(camera, screen):
    for i in range(3, 0, -1): #for (let i = 3; i > 0; i--)
        end = pygame.time.get_ticks() + 1000
        while pygame.time.get_ticks() < end:
            camera_preview(camera, screen)
            countdown_text(i, screen)
            pygame.display.flip()
