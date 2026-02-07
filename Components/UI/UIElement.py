import pygame
from pygame import Vector2
from GameEssentials.component import Component
from Components.camera import Camera

class Element(Component):
    def __init__(self):
        super().__init__()
        self.position: Vector2 = Vector2(0, 0)
        self.anchor: Vector2 = Vector2(0.5, 0.5)
        self.size: Vector2 = Vector2(100, 50)
        self.layer: int = 0

    def resolve_rect(self, canvas, camera: Camera) -> pygame.Rect:
        if canvas.renderMode != 0:
            return None
        
        sw, sh = camera.ScreenWidth, camera.ScreenHeight

        x = sw * self.anchor.x + self.position.x
        y = sh * self.anchor.y + self.position.y

        x -= self.size.x * self.anchor.x
        y -= self.size.y * self.anchor.y

        return pygame.Rect(x, y, self.size.x, self.size.y)
