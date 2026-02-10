# Components/UI/Canvas.py

from GameEssentials.component import Component
from Components.UI.UIElement import Element
from Components.UI.Layout.UILayoutEngine import LayoutElement

import pygame

class Canvas(Component):
    def __init__(self):
        super().__init__()
        self.root = Element("root")

    def Render(self, screen):
        self._compute_styles(self.root)
        LayoutElement(self.root)
        self.Draw(screen, self.root, pygame.Vector2(0, 0))

    def ComputeStyles(self, element):
        if element.parent:
            element.computedStyle.color = (
                element.style.color or element.parent.computedStyle.color
            )
        else:
            element.computedStyle.color = element.style.color

        element.computedStyle.display = element.style.display
        element.computedStyle.flexDirection = element.style.flexDirection

        for child in element.children:
            self._compute_styles(child)

    def Draw(self, screen, element, parentPos):
        pos = parentPos + pygame.Vector2(
            element.layout.x, element.layout.y
        ) + element.transform.offset

        rect = pygame.Rect(
            pos.x,
            pos.y,
            element.layout.width,
            element.layout.height
        )

        element._worldRect = rect  # cache for hit testing

        if element.renderer:
            element.renderer.draw(screen, rect, element.computedStyle)

        for child in element.children:
            self.Draw(screen, child, pos)
