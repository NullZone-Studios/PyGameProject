from GameEssentials import GameObject
from Components import Face
import pygame
from typing import Optional

class Panel(GameObject):
    def __init__(self, name, tag, parent = None, width: float = 100, depth: float = 100, color: pygame.Color = pygame.Color("white")):
        super().__init__(name, tag, parent)
        self.AddComponent(Face(width= width, depth= depth, color= color))