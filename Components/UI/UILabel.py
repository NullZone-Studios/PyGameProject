from .UIElement import Element
from .Style.boxSpacing import BoxSpacing
import pygame

class Label(Element):
    def __init__(self, tag = "div", text: str = ""):
        super().__init__(tag)
        self.Text = text
        self.cachedSurface = None
        self.cachedSize = None
        
    def Layout(self, available, measureOnly=False):
        style = self.computedStyle
        padding = style.padding if style and style.padding else BoxSpacing()
        
        width = style.width if style else None
        height = style.height if style else None
        
        contentMaxWidth = available.width - padding.left - padding.right
        
        if width is None or height is None:
            textWidth, textHeight = self.measureText(max(0, contentMaxWidth))
            if width is None:
                width = textWidth + padding.left + padding.right
            if height is None:
                height = textHeight + padding.top + padding.bottom
                
                oldWidth, oldHeight = style.width, style.height
                style.width, style.height = width, height
                
                super().Layout(available, measureOnly=True)
                
                style.width = oldWidth
                style.height = oldHeight
        else:
            super().Layout(available, measureOnly=measureOnly)
    
    def measureText(self, maxWidth):
        style = self.computedStyle
        if not style or not style.font:
            return (0, 0)

        font = style.font
        color = style.color or pygame.Color("black")

        textSurface = font.render(
            text=self.Text,
            antialias=True,
            color=color,
            wraplength=maxWidth
        )

        self.cachedSurface = textSurface
        self.cachedSize = textSurface.get_size()
        return self.cachedSize

        
    def Draw(self, surface, rectangle: pygame.Rect):
        super().Draw(surface, rectangle)
        if not self.cachedSurface:
            return
        style = self.computedStyle
        padding = style.padding or BoxSpacing()
        
        textRectangle = self.cachedSurface.get_rect()
        content = pygame.Rect(
            rectangle.x + padding.left,
            rectangle.y + padding.top,
            rectangle.width - padding.left - padding.right,
            rectangle.height - padding.top - padding.bottom
        )
        
        textX, textY = content.topleft
        
        if style.textAlign == "center":
            textX = content.x + (content.width - textRectangle.width) // 2
        elif style.textAlign == "right":
            textX = content.right - textRectangle.width
        else:
            textX = content.x
            
        if style.verticalAlign == "middle":
            textY = content.y + (content.height - textRectangle.height) // 2
        elif style.verticalAlign == "bottom":
            textY = content.bottom - textRectangle.height
        else:
            textY = content.y
        
        surface.blit(self.cachedSurface, (textX, textY))
