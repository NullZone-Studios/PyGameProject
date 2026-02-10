from pygame import Vector2, Surface
from typing import Optional
import pygame
from .UIStyle import Style
from .UIResolvedStyle import ResolvedStyle

class Element:
    def __init__(self, tag:str = "div"):
        self.tag = tag
        self.style: Optional[Style] = None
        self.computedStyle: Optional[ResolvedStyle] = None
        self.children = []
        self.parent: Optional["Element"] = None
        
        self.rectangle: pygame.Rect = pygame.Rect(0,0,0,0)
        self.surface: Optional[pygame.Surface] = None
        
        self.depth = 0
        
    def AddChild(self, child: "Element") -> "Element":
        child.parent = self
        self.children.append(child)
        return child
        
    def RemoveChild(self, child: "Element"):
        if child in self.children:
            child.parent = None
            self.children.remove(child)
        
    @property
    def AbsoluteRectangle(self) -> pygame.Rect:
        if not self.parent:
            return self.rectangle

        parent_rect = self.parent.AbsoluteRectangle
        return pygame.Rect(
            parent_rect.x + self.rectangle.x,
            parent_rect.y + self.rectangle.y,
            self.rectangle.width,
            self.rectangle.height
        )
        
    def ResolveStyle(self, base: Optional[Style] = None):
        self.computedStyle = ResolvedStyle(
            base=base,
            override=self.style
        )
        
        for child in self.children:
            child.ResolveStyle(self.computedStyle)
        
    def Layout(self, available: pygame.Rect):
        style = self.computedStyle
        
        def LayoutBlock():
            cursorY = 0
            for child in self.children:
                if child.computedStyle.position == "absolute":
                    child.Layout(
                        pygame.Rect(0,0,self.rectangle.width, self.rectangle.height)
                    )
                    continue
                
                child.Layout(
                    pygame.Rect(
                        0,
                        cursorY,
                        self.rectangle.width,
                        self.rectangle.height - cursorY
                    )
                )
                cursorY += child.rectangle.height
            if style.height is None:
                self.rectangle.height = cursorY
        def LayoutFlex():
            gap = style.gap or 0
            if style.flexDirection == "row":
                cursor = 0
                maxHeight = 0
                maxWidth = 0
                
                for child in self.children:
                    if child.computedStyle.position == "absolute":
                        child.Layout(
                            pygame.Rect(0,0,self.rectangle.width, self.rectangle.height)
                        )
                        continue
                    
                    childWidth = (
                        child.computedStyle.width
                        if child.computedStyle.width is not None
                        else 0
                    )
                    childHeight = (
                        child.computedStyle.height
                        if child.computedStyle.height is not None
                        else self.rectangle.height
                    )
                    child.Layout(
                        pygame.Rect(cursor, 0, childWidth, childHeight)
                    )
                    
                    cursor += childWidth + gap
                    maxHeight = max(maxHeight, childHeight)
                if self.computedStyle.height is None:
                    self.rectangle.height = maxHeight
            else:
                cursor = 0
                maxWidth = 0
                
                for child in self.children:
                    if child.computedStyle.position == "absolute":
                        child.Layout(
                            pygame.Rect(0, 0, self.rectangle.width, self.rectangle.height)
                        )
                        continue
                    
                    childWidth = (
                        child.computedStyle.width
                        if child.computedStyle.width is not None
                        else self.rectangle.width
                    )
                    childHeight = (
                        child.computedStyle.height
                        if child.computedStyle.height is not None
                        else 0
                    )
                    
                    child.Layout(
                        pygame.Rect(0, cursor, childWidth, childHeight)
                    )
                    
                    cursor += childHeight + gap
                    maxWidth = max(maxWidth, childWidth)
                
                if self.computedStyle.width is None:
                    self.rectangle.width = maxWidth
        
        width = style.width if style.width is not None else available.width
        height = style.height if style.height is not None else available.height
        x = style.left if style.left is not None else 0
        y = style.top if style.top is not None else 0
        
        if style.right is not None:
            x = available.width - width - style.right
        if style.bottom is not None:
            y = available.height - height - style.bottom
            
        self.rectangle = pygame.Rect(x,y,width,height)
        
        if style.position == "absolute":
            for child in self.children:
                child.Layout(
                    pygame.Rect(0,0,width,height)
                )
            return
        
        if style.display == "flex":
            LayoutFlex()
        else:
            LayoutBlock()
        
    def Draw(self, surface: Surface):
        if not self.computedStyle:
            return
        
        rectangle = self.AbsoluteRectangle
        style = self.computedStyle
        
        if style.background:
            pygame.draw.rect(
                surface,
                style.background,
                rectangle,
                border_top_left_radius=style.borderRadiusTopLeft,
                border_top_right_radius=style.borderRadiusTopRight,
                border_bottom_left_radius=style.borderRadiusBottomLeft,
                border_bottom_right_radius=style.borderRadiusBottomRight
            )
            
        if style.borderWidth and style.borderWidth > 0:
            pygame.draw.rect(
                surface,
                style.borderColor or pygame.Color("white"),
                rectangle,
                width=style.borderWidth,
                border_top_left_radius=style.borderRadiusTopLeft,
                border_top_right_radius=style.borderRadiusTopRight,
                border_bottom_left_radius=style.borderRadiusBottomLeft,
                border_bottom_right_radius=style.borderRadiusBottomRight
            )
        
        
    
    def GetDrawData(self):
        queue = []
        
        queue.append({
            "depth": self.depth,
            "draw": self.Draw
        })
        
        for child in self.children:
            queue.extend(child.GetDrawData())
            
        return queue
        