import pygame
from Components.UI.UIElement import Element
from Components.UI.UICanvas import Canvas
from Components.camera import Camera
from Components.UI.UIStyle import Style

class UIRectangle(Element):
    def __init__(self, style: Style):
        super().__init__()
        self.style = style

    def BuildRenderData(self, canvas: Canvas, camera: Camera):
        rectangle = self.resolve_rect(canvas, camera)
        if not rectangle:
            return None
        
        def draw(screen):
            if self.style.borderWidth > 0:
                pygame.draw.rect(
                    screen,
                    self.style.borderColor if self.style.borderColor else pygame.Color("white"),
                    pygame.Rect(
                        rectangle.left - self.style.borderWidth,
                        rectangle.top - self.style.borderWidth,
                        rectangle.width + self.style.borderWidth * 2,
                        rectangle.height + self.style.borderWidth * 2
                    )
                )
            
            pygame.draw.rect(
                screen, 
                self.style.background if self.style.background else pygame.Color("white"), 
                rectangle)
            
        return {
            "type": "overlay",
            "layer": self.layer,
            "draw": draw
        }