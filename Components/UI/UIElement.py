from pygame import Vector2, Surface
from typing import Optional
import pygame
from .UIStyle import Style
from .UIResolvedStyle import ResolvedStyle
from .UIEvent import Event


class Element:
    def __init__(self, tag: str = "div"):
        self.tag = tag
        self.style: Optional[Style] = None
        self.computedStyle: Optional[ResolvedStyle] = None
        self.children = []
        self.parent: Optional["Element"] = None

        self.rectangle: pygame.Rect = pygame.Rect(0, 0, 0, 0)
        self.scrollOffset: Vector2 = Vector2(0, 0)
        self.cursor: pygame.Cursor = None

        self.depth = 0

    def AddChild(self, child: "Element") -> "Element":
        child.parent = self
        self.children.append(child)
        return child

    def RemoveChild(self, child: "Element"):
        if child in self.children:
            child.parent = None
            self.children.remove(child)
            
    def Query(self, elementType: Optional[type] = None, tag: Optional[str] = None) -> Optional["Element"]:
        if elementType and tag:
            if isinstance(self, elementType) and self.tag == tag:
                return self
            for child in self.children:
                return child.Query(elementType = elementType, tag = tag)
        elif elementType:
            if isinstance(self, elementType):
                return self
            for child in self.children:
                return child.Query(elementType = elementType)
        elif tag:
            if self.tag == tag:
                return self
            for child in self.children:
                return child.Query(tag = tag)
        else:
            return None
        
    def Q(self, elementType: Optional[type] = None, tag: Optional[str] = None):
        return self.Query(elementType = elementType, tag = tag)

    @property
    def AbsoluteRectangle(self) -> pygame.Rect:
        if not self.parent:
            return self.rectangle

        parent_rect = self.parent.AbsoluteRectangle
        return pygame.Rect(
            parent_rect.x + self.rectangle.x,
            parent_rect.y + self.rectangle.y,
            self.rectangle.width,
            self.rectangle.height,
        )

    def ResolveStyle(self, base: Optional[Style] = None):
        self.computedStyle = ResolvedStyle(base=base, override=self.style)

        for child in self.children:
            child.ResolveStyle(self.computedStyle)

    def Layout(self, available: pygame.Rect):
        style = self.computedStyle

        def LayoutBlock():
            cursorY = 0
            for child in self.children:
                if child.computedStyle.position == "absolute":
                    child.Layout(
                        pygame.Rect(0, 0, self.rectangle.width, self.rectangle.height)
                    )
                    continue

                child.Layout(
                    pygame.Rect(
                        0,
                        cursorY,
                        self.rectangle.width,
                        self.rectangle.height - cursorY,
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

                for child in self.children:
                    if child.computedStyle.position == "absolute":
                        child.Layout(
                            pygame.Rect(
                                0, 0, self.rectangle.width, self.rectangle.height
                            )
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
                    child.Layout(pygame.Rect(cursor, 0, childWidth, childHeight))

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
                            pygame.Rect(
                                0, 0, self.rectangle.width, self.rectangle.height
                            )
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

                    child.Layout(pygame.Rect(0, cursor, childWidth, childHeight))

                    cursor += childHeight + gap
                    maxWidth = max(maxWidth, childWidth)

                if self.computedStyle.width is None:
                    self.rectangle.width = maxWidth

        width = style.width if style.width is not None else available.width
        height = style.height if style.height is not None else available.height

        x = available.x
        y = available.y

        if style.position == "absolute":
            x = style.left if style.left is not None else 0
            y = style.top if style.top is not None else 0
            if style.right is not None:
                x = available.width - width - style.right
            if style.bottom is not None:
                y = available.height - height - style.bottom

        self.rectangle = pygame.Rect(x, y, width, height)

        if style.position == "absolute":
            for child in self.children:
                child.Layout(pygame.Rect(0, 0, width, height))
            return

        if style.display == "flex":
            LayoutFlex()
        else:
            LayoutBlock()

    def Draw(self, surface: Surface, rectangle: pygame.Rect):
        if not self.computedStyle:
            return
        
        style = self.computedStyle

        if style.background:
            pygame.draw.rect(
                surface,
                style.background,
                rectangle,
                border_top_left_radius=style.borderRadiusTopLeft or 0,
                border_top_right_radius=style.borderRadiusTopRight or 0,
                border_bottom_left_radius=style.borderRadiusBottomLeft or 0,
                border_bottom_right_radius=style.borderRadiusBottomRight or 0,
            )

        if style.borderWidth and style.borderWidth > 0:
            pygame.draw.rect(
                surface,
                style.borderColor or pygame.Color("white"),
                rectangle,
                width=style.borderWidth,
                border_top_left_radius=style.borderRadiusTopLeft or 0,
                border_top_right_radius=style.borderRadiusTopRight or 0,
                border_bottom_left_radius=style.borderRadiusBottomLeft or 0,
                border_bottom_right_radius=style.borderRadiusBottomRight or 0,
            )

    def Render(self, surface: pygame.Surface, parentClip: Optional[pygame.Rect] = None, offset: Optional[Vector2] = None):
        if not self.computedStyle:
            return
        
        offset = offset if offset is not None else Vector2(0,0)
        
        style = self.computedStyle
        rectangle: pygame.Rect = pygame.Rect(
            offset.x + self.rectangle.x,
            offset.y + self.rectangle.y,
            self.rectangle.width,
            self.rectangle.height
        )
        
        effectiveClip = parentClip
        
        hidden = style.overflow in ("hidden", "scroll", "scroll-x", "scroll-y")
        rounded = (style.borderRadiusTopLeft or style.borderRadiusTopRight or style.borderRadiusBottomLeft or style.borderRadiusBottomRight)
        hasRoundedMask = hidden and rounded
        
        if hidden:
            if effectiveClip:
                effectiveClip = rectangle.clip(effectiveClip)
            else:
                effectiveClip = rectangle.copy()
        
        oldClip = surface.get_clip()
        if effectiveClip:
            surface.set_clip(effectiveClip)
            
        self.Draw(surface, rectangle)
        
        childOffset: Vector2 = Vector2(
            rectangle.x - self.scrollOffset.x,
            rectangle.y - self.scrollOffset.y
        )
        
        if hasRoundedMask:
            temp = pygame.Surface(rectangle.size, pygame.SRCALPHA)
            
            localOffset = Vector2(
                -self.scrollOffset.x,
                -self.scrollOffset.y
            )
            for child in self.children:
                    child.Render(temp, None, localOffset)

            mask = pygame.Surface(rectangle.size, pygame.SRCALPHA)
            pygame.draw.rect(
                mask,
                (255,255,255,255),
                mask.get_rect(),
                border_top_left_radius=style.borderRadiusTopLeft or 0,
                border_top_right_radius=style.borderRadiusTopRight or 0,
                border_bottom_left_radius=style.borderRadiusBottomLeft or 0,
                border_bottom_right_radius=style.borderRadiusBottomRight or 0
            )
            
            temp.blit(mask, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
            
            if parentClip:
                surface.set_clip(parentClip)
            
            surface.blit(temp, rectangle.topleft)
        else:
            
            for child in self.children:
                    child.Render(surface, effectiveClip, childOffset)

        surface.set_clip(oldClip)

    def HitTest(self, point: Vector2, offset: Optional[Vector2] = None) -> Optional["Element"]:
        if not self.computedStyle:
            return None
        
        offset = offset if offset is not None else Vector2(0,0)
        
        rectangle = pygame.Rect(
            offset.x + self.rectangle.x,
            offset.y + self.rectangle.y,
            self.rectangle.width,
            self.rectangle.height
        )
        
        style = self.computedStyle
        
        if style.overflow in ("hidden", "scroll", "scroll-x", "scroll-y"):
            if not rectangle.collidepoint(point):
                return None
        else:
            if not rectangle.collidepoint(point):
                return None
        
        childOffset = Vector2(
            rectangle.x - self.scrollOffset.x,
            rectangle.y - self.scrollOffset.y
        )
        
        for child in reversed(self.children):
            hit = child.HitTest(point, childOffset)
            if hit:
                return hit
            
        return self
    
    def HandleEvent(self, event: Event) -> bool:
        if not event.stopped and self.parent:
            return self.parent.HandleEvent(event)
        return False