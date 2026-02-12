from .UIElement import Element
from .UIEvent import Event, EventType
from .UILabel import Label
from .UIStyle import Style
from pygame import mouse, Cursor, cursors

class Button(Element):
    def __init__(self, text: str = "Button"):
        super().__init__("button")
        label = self.AddChild(Label("buttonLabel", text))
        label.style = Style(
            textAlign="center",
            verticalAlign="middle"
        )
        
    def HandleEvent(self, event: Event):
        if event.type == EventType.MOUSE_ENTER:
            mouse.set_cursor(cursors.broken_x)
            print(f"Mouse Entered Button")
        elif event.type == EventType.MOUSE_LEAVE:
            print(f"Mouse Left Button")
            mouse.set_cursor(cursors.arrow)