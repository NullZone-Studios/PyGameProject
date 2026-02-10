import pygame
from typing import Optional

class Style:
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
        color: Optional[pygame.Color] = None
        ):
        self.position = position
        self.display = display
        self.flexDirection = flexDirection
        self.gap = gap
        self.overflow = overflow
        self.background = background
        self.borderColor = borderColor
        self.borderWidth = borderWidth
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