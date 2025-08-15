#!/usr/bin/env python3
# test_pygame_preview.py
#
# Minimal Pygame + Picamera2 preview test:
# - Fullscreen Pygame window
# - Smooth lores YUV preview (faster)
# - Overlay text demo
# Keys:
#   O : toggle "READY" overlay
#   C : show a quick 3-2-1 countdown (no capture)
# Esc/Ctrl+Q : quit

import os
os.environ.setdefault("DISPLAY", ":0")
os.environ.pop("SDL_VIDEODRIVER", None)  # let SDL pick x11 if available

import sys
import time
import pygame
from pygame import Surface
from picamera2 import Picamera2
import numpy as np

def make_screen():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.mouse.set_visible(False)
    return screen

def make_font(h_frac=0.18):
    # font size ≈ 18% of screen height
    w, h = pygame.display.get_surface().get_size()
    size = max(24, int(h * h_frac))
    return pygame.font.SysFont("DejaVu Sans", size, bold=True)

def draw_overlay_text(screen, text, font):
    if not text:
        return
    w, h = screen.get_size()

    # semi-transparent black bar
    bar_h = int(h * 0.28)
    bar = Surface((w, bar_h), pygame.SRCALPHA)
    bar.fill((0, 0, 0, 150))
    screen.blit(bar, (0, (h - bar_h) // 2))

    # centered white text
    surf = font.render(text, True, (255, 255, 255))
    rect = surf.get_rect(center=(w // 2, h // 2))
    screen.blit(surf, rect)

def countdown(screen, font, seconds=3):
    # Simple overlay-only countdown (no capture); blocks but pumps events
    for n in range(seconds, 0, -1):
        # keep preview visible underneath; we only draw overlays
        pygame.event.pump()
        draw_overlay_text(screen, str(n), font)
        pygame.display.flip()
        time.sleep(1)

def main():
    # Pygame fullscreen window
    screen = make_screen()
    font = make_font()
    screen_w, screen_h = screen.get_size()

    picam2 = Picamera2()
    picam2.configure(
        picam2.create_preview_configuration(
            main={"size": (screen_w, screen_h), "format": "RGB888"}
        )
    )
    picam2.start()

    overlay_on = True
    running = True
    clock = pygame.time.Clock()

    while running:
        # Handle a few keys; keep it minimal
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE or (e.key == pygame.K_q and (e.mod & pygame.KMOD_CTRL)):
                    running = False
                elif e.key == pygame.K_o:
                    overlay_on = not overlay_on
                elif e.key == pygame.K_c:
                    countdown(screen, font, seconds=3)

        # Grab the latest main frame and blit it to the fullscreen window
        try:
            frame = picam2.capture_array()  # HxWx3 (often BGR on some builds)
            h, w = frame.shape[:2]
            # Convert BGR -> RGB (common on Pi pipelines due to byte order)
            frame = frame[:, :, ::-1].copy()
            frame_surf = pygame.image.frombuffer(frame.tobytes(), (w, h), "RGB")
            if (w, h) != (screen_w, screen_h):
                frame_surf = pygame.transform.smoothscale(frame_surf, (screen_w, screen_h))
            screen.blit(frame_surf, (0, 0))
        except Exception:
            pass
        if overlay_on:
            draw_overlay_text(screen, "READY", font)

        pygame.display.flip()
        clock.tick(60)  # cap loop to ~60fps for stability

    # Cleanup
    try:
        picam2.stop()
    except Exception:
        pass
    pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    main()