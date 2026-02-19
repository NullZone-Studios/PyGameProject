from .UIElement import Element
from .UIEvent import Event, EventType
from .UILabel import Label
from .UIStyle import Style
from pygame import mouse, Cursor, cursors
import pygame

class Button(Element):
    def __init__(self, text: str = "Button"):
        super().__init__("button")
        label = self.AddChild(Label("buttonLabel", text))
        label.style = Style(
            textAlign="center",
            verticalAlign="middle",
            margin=(0, 10, 0, 0)
        )
        self.cursor = cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)