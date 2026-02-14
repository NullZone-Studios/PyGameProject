import pygame
from typing import Optional
from .Style import BoxSpacing

class Style:
    PSEUDO_FIELDS = ("hover", "active", "focus")
    
    def __init__(
        self,
        position: Optional[str] = None,
        display: Optional[str] = None,
        flexDirection: Optional[str] = None,
        gap: Optional[int] = None,
        overflow: Optional[str] = None,
        background: Optional[pygame.Color] = None,
        borderColor: Optional[pygame.Color] = None,
        borderWidth: Optional[int] = None,
        borderRadius: Optional[int] = None,
        borderRadiusTopLeft: Optional[int] = None,
        borderRadiusTopRight: Optional[int] = None,
        borderRadiusBottomLeft: Optional[int] = None,
        borderRadiusBottomRight: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        left: Optional[int] = None,
        right: Optional[int] = None,
        top: Optional[int] = None,
        bottom: Optional[int] = None,
        color: Optional[pygame.Color] = None,
        font: Optional[pygame.Font] = None,
        textAlign: Optional[str] = None,
        verticalAlign: Optional[str] = None,
        padding: int | tuple[int, int] | tuple[int, int ,int ,int] | None = None,
        margin: int | tuple[int, int] | tuple[int, int ,int ,int] | None = None,
        hover: Optional["Style"] = None,
        active: Optional["Style"] = None,
        focus: Optional["Style"] = None
        ):
        self.position = position
        self.display = display
        self.flexDirection = flexDirection
        self.gap = gap
        self.overflow = overflow
        self.background = background
        self.borderColor = borderColor
        self.borderWidth = borderWidth or 0
        self.borderRadius = borderRadius
        self.borderRadiusTopLeft = borderRadiusTopLeft
        self.borderRadiusTopRight = borderRadiusTopRight
        self.borderRadiusBottomLeft = borderRadiusBottomLeft
        self.borderRadiusBottomRight = borderRadiusBottomRight
        self.width = width
        self.height = height
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.color = color
        self.font = font
        self.textAlign = textAlign
        self.verticalAlign = verticalAlign
        self.hover = hover
        self.active = active
        self.focus = focus
        self.padding = BoxSpacing.from_value(padding)
        self.margin = BoxSpacing.from_value(margin)
        
    def ApplyOverride(self, override: "Style"):
        if not override:
            return
        
        for attribute, value in vars(override).items():
            if attribute in Style.PSEUDO_FIELDS:
                continue
            
            if value is not None:
                setattr(self, attribute, value)
                
    def ResolveShorthand(self):
        if self.borderRadius is not None:
            if self.borderRadiusTopLeft is None:
                self.borderRadiusTopLeft = self.borderRadius
            if self.borderRadiusTopRight is None:
                self.borderRadiusTopRight = self.borderRadius
            if self.borderRadiusBottomLeft is None:
                self.borderRadiusBottomLeft = self.borderRadius
            if self.borderRadiusBottomRight is None:
                self.borderRadiusBottomRight = self.borderRadius
                
    def Copy(self) -> "Style":
        copy = Style()
        for attribute, value in vars(self).items():
            setattr(copy, attribute, value)
        return copy