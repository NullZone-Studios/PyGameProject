from .inputEvent import InputEvent
from typing import Optional

class InputLayer:
    def __init__(self, priority: int = 0):
        self.priority = priority
    
    def DispatchEvent(self, event: InputEvent):
        pass