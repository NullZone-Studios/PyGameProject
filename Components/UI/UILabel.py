from .UIElement import Element
import pygame

class Label(Element):
    def __init__(self, tag = "div", text: str = ""):
        super().__init__(tag)
        self.Text = text
        
    def Draw(self, surface):
        super().Draw(surface)

        if not self.computedStyle:
            return

        style = self.computedStyle
        rect = self.AbsoluteRectangle

        font = style.font or pygame.font.SysFont("sans-serif", 12)

        labelSprite = font.render(
            text=self.Text,
            antialias= True,
            color=style.color or pygame.Color("black"),
            wraplength=self.rectangle.width
        )

        textRectangle = labelSprite.get_rect()
        
        if style.textAlign == "center":
            textRectangle.x = rect.x + (rect.width - textRectangle.width) // 2
        elif style.textAlign == "right":
            textRectangle.x = rect.x + rect.width - textRectangle.width
        else:
            textRectangle.x = rect.x
            
        if style.verticalAlign == "middle":
            textRectangle.y = rect.y + (rect.height - textRectangle.height) // 2
        elif style.verticalAlign == "bottom":
            textRectangle.y = rect.y + rect.height - textRectangle.height
        else:
            textRectangle.y = rect.y
        
        surface.blit(labelSprite, textRectangle)
