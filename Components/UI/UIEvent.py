from pygame import Vector2
from typing import Optional

class Event:
    def __init__(self, type: str, position: Optional[Vector2] = None, delta: Optional[Vector2] = None):
        self.type = type
        self.position = position
        self.delta = delta
        
        self.target: Optional["Element"] = None
        self.currentTarget: Optional["Element"] = None
        
        self.stopped = False
        
    def StopPropagation(self):
        self.stopped = True
        
    @property
    def propagationStopped(self):
        return self.stopped
    
class EventType:
    MOUSE_ENTER = "mouseenter"
    MOUSE_LEAVE = "mouseleave"
    MOUSE_DOWN = "mousedown"
    MOUSE_UP = "mouseup"
    MOUSE_DRAG = "mousedrag"
    MOUSE_CLICK = "mouseclick"
    