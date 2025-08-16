# hold top-left corner for 3 seconds to exit photobooth and go back to Pi GUI
import pygame

class CornerHold:
    def __init__(self, corner="TL", margin=100, hold_ms=3000,
                 allow_mouse=True, cancel_on_leave=False):
        self.corner = corner
        self.margin = margin
        self.hold_ms = hold_ms
        self.allow_mouse = allow_mouse
        self.cancel_on_leave = cancel_on_leave
        self._down = False
        self._start = 0

    def _in_corner(self, pos, size):
        x, y = pos; w, h = size; m = self.margin
        return ((self.corner == "TL" and x <= m and y <= m) or
                (self.corner == "TR" and x >= w - m and y <= m) or
                (self.corner == "BR" and x >= w - m and y >= h - m) or
                (self.corner == "BL" and x <= m and y >= h - m))

    def update(self, events, size) -> bool:
        now = pygame.time.get_ticks()

        for e in events:
            # ---- TOUCH support ----
            if e.type == pygame.FINGERDOWN:
                pos = (int(e.x * size[0]), int(e.y * size[1]))
                if self._in_corner(pos, size):
                    self._down, self._start = True, now
            elif e.type == pygame.FINGERUP:
                self._down = False
            elif e.type == pygame.FINGERMOTION and self.cancel_on_leave and self._down:
                pos = (int(e.x * size[0]), int(e.y * size[1]))
                if not self._in_corner(pos, size):
                    self._down = False

            # ---- MOUSE fallback (many touch panels appear as a mouse) ----
            elif self.allow_mouse and e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if self._in_corner(e.pos, size):
                    self._down, self._start = True, now
            elif self.allow_mouse and e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                self._down = False
            elif self.allow_mouse and e.type == pygame.MOUSEMOTION and self.cancel_on_leave and self._down:
                if not self._in_corner(e.pos, size):
                    self._down = False

        if self._down and (now - self._start >= self.hold_ms):
            self._down = False
            return True
        return False
# hold top-left corner for 3 seconds to exit photobooth and go back to Pi GUI
import pygame

class CornerHold:
    def __init__(self, corner="TL", margin=60, hold_ms=3000,
                 allow_mouse=True, cancel_on_leave=False):
        self.corner = corner
        self.margin = margin
        self.hold_ms = hold_ms
        self.allow_mouse = allow_mouse
        self.cancel_on_leave = cancel_on_leave
        self._down = False
        self._start = 0

    def _in_corner(self, pos, size):
        x, y = pos; w, h = size; m = self.margin
        return ((self.corner == "TL" and x <= m and y <= m) or
                (self.corner == "TR" and x >= w - m and y <= m) or
                (self.corner == "BR" and x >= w - m and y >= h - m) or
                (self.corner == "BL" and x <= m and y >= h - m))

    def update(self, events, size) -> bool:
        now = pygame.time.get_ticks()

        for e in events:
            # ---- TOUCH support ----
            if e.type == pygame.FINGERDOWN:
                pos = (int(e.x * size[0]), int(e.y * size[1]))
                if self._in_corner(pos, size):
                    self._down, self._start = True, now
            elif e.type == pygame.FINGERUP:
                self._down = False
            elif e.type == pygame.FINGERMOTION and self.cancel_on_leave and self._down:
                pos = (int(e.x * size[0]), int(e.y * size[1]))
                if not self._in_corner(pos, size):
                    self._down = False

            # ---- MOUSE fallback (many touch panels appear as a mouse) ----
            elif self.allow_mouse and e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if self._in_corner(e.pos, size):
                    self._down, self._start = True, now
            elif self.allow_mouse and e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                self._down = False
            elif self.allow_mouse and e.type == pygame.MOUSEMOTION:
                # Start hold if the left button is currently held and we move into the corner
                b = getattr(e, 'buttons', (0,0,0))
                if not self._down and len(b) > 0 and b[0] and self._in_corner(e.pos, size):
                    self._down, self._start = True, now
                # Optionally cancel if we slide out while holding
                if self.cancel_on_leave and self._down and not self._in_corner(e.pos, size):
                    self._down = False

        # Extra safety: some panels don’t emit BUTTONDOWN, but keep button state; poll it
        if self.allow_mouse:
            pressed = pygame.mouse.get_pressed(3)
            if not self._down and pressed[0]:
                pos = pygame.mouse.get_pos()
                if self._in_corner(pos, size):
                    self._down, self._start = True, now
            elif self.cancel_on_leave and self._down and not pressed[0]:
                self._down = False

        if self._down and (now - self._start >= self.hold_ms):
            self._down = False
            return True
        return False