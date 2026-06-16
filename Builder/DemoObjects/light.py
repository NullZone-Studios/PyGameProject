from GameEssentials import GameObject
from Components import (
    PointLight
)
import pygame

class LightObject(GameObject):
    def __init__(self, name: str = "Light", tag: str = "Light", parent = None, intensity: float = 1.0, range: float = 10.0, color: pygame.Color = pygame.Color("white")):
        super().__init__(name, tag, parent)
        self.AddComponent(PointLight(color= color, intensity= intensity, range= range))
        