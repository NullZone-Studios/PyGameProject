import pygame
from Components.UI.UIElement import Element
from Components.UI.UICanvas import Canvas
from Components.camera import Camera

class UIRectangle(Element):
    def __init__(self, color: pygame.Color = pygame.Color("white")):
        super().__init__()
        self.color: pygame.Color = color

    def BuildRenderData(self, canvas: Canvas, camera: Camera):
        rectangle = self.resolve_rect(canvas, camera)
        if not rectangle:
            return None
        
        def draw(screen):
            pygame.draw.rect(screen, self.color, rectangle)
            
        return {
            "type": "overlay",
            "layer": self.layer,
            "draw": draw
        }