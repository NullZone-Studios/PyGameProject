from GameObject.Component import Component
from typing import Type, Optional
from pygame import Vector2

class Transform2D(Component):
    def __init__(self, x: Optional[int] = 0, y: Optional[int] = 0):
        super.__init__()
        self.Position = Vector2(x,y)
        self.Rotation: float = 0
        
    def Translate(self, x, y):
        self.Position.X += x
        self.Position.Y += y