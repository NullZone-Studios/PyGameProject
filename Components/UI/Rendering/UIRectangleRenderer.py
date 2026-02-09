import pygame
from Components.UI.Rendering.UIRenderer import Renderer

class RectangleRenderer(Renderer):
    def draw(self, screen, rectangle, style):
        
        if style.background:
            pygame.draw.rect(screen, style.background, rectangle)
        
        if style.borderWidth:
            pygame.draw.rect(
                screen,
                style.borderColor,
                rectangle,
                style.borderWidth
            )