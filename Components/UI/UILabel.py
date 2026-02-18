from .UIElement import Element
import pygame

class Label(Element):
    def __init__(self, tag = "div", text: str = ""):
        super().__init__(tag)
        self.Text = text
        
    def Layout(self, available):
        super().Layout(available)
        style = self.computedStyle
        if style and style.font:
            textSurface = style.font.render(
                text=self.Text,
                antialias= True,
                color=style.color or pygame.Color("black"),
                wraplength=style.width if style.width else available.width
            )
            textRect = textSurface.get_rect()
            self.rectangle.width = textRect.width
            self.rectangle.height = style.height if style.height else textRect.height
        
        
    def Draw(self, surface, rectangle: pygame.Rect):
        super().Draw(surface, rectangle)

        if not self.computedStyle:
            return

        style = self.computedStyle

        font = style.font or pygame.font.SysFont("sans-serif", 12)

        labelSprite = font.render(
            text=self.Text,
            antialias= True,
            color=style.color or pygame.Color("black"),
            wraplength=rectangle.width
        )

        textRectangle = labelSprite.get_rect()
        
        if style.textAlign == "center":
            textRectangle.x = rectangle.x + (rectangle.width - textRectangle.width) // 2
        elif style.textAlign == "right":
            textRectangle.x = rectangle.x + rectangle.width - textRectangle.width
        else:
            textRectangle.x = rectangle.x
            
        if style.verticalAlign == "middle":
            textRectangle.y = rectangle.y + (rectangle.height - textRectangle.height) // 2
        elif style.verticalAlign == "bottom":
            textRectangle.y = rectangle.y + rectangle.height - textRectangle.height
        else:
            textRectangle.y = rectangle.y
        
        surface.blit(labelSprite, textRectangle)
