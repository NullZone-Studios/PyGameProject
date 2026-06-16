from Components import (
    Camera,
)
from GameEssentials import (
    GameObject,
)
import pygame
from pygame import (Vector2)
from typing import Optional

class CameraObject(GameObject):
    def __init__(self, name = "Camera", tag = "Camera", parent = None, resolution: Optional[Vector2] = Vector2(x=1280,y=720)):
        super().__init__(name, tag, parent)
        self.AddComponent(Camera(resolution.x, resolution.y))