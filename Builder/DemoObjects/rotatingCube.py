import pygame
from GameEssentials import GameObject
from Components import ShapeRenderer
from Builder.DemoScripts import Rotator

class RotatingCube(GameObject):
    def __init__(self, name = "RotatingCube", tag = "RotatingCube", parent = None, size: float = 1, color: pygame.Color = pygame.Color("white")):
        super().__init__(name, tag, parent)
        self.AddComponent(ShapeRenderer(shape= "cube", color= color, scale= (size, size, size)))
        self.AddComponent(Rotator())
