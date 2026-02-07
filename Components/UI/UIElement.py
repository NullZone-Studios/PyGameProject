from pygame import Vector2
from GameEssentials.component import Component

class Element(Component):
    def __init__(self):
        super().__init__()
        self.position: Vector2 = Vector2(0,0)
        self.anchor: Vector2 = Vector2(.5,.5)