from pygame import Vector2
from typing import Optional

class InputEvent:
    def __init__(self, device, code, state, position: Optional[Vector2] = None, delta: Optional[Vector2] = None):
        self.device = device
        self.code = code
        self.state = state
        self.position = position
        self.delta = delta
        
        self.consumed = False