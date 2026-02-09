from pygame import Vector2

class Transform:
    def __init__(self):
        self.offset = Vector2(0,0)
        self.scale = Vector2(1,1)
        self.rotation = 0