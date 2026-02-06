import pygame
import numpy as np
from GameEssentials import Component
from Components.transform import Transform

class Light(Component):
    def __init__(self, color: pygame.Color = pygame.Color(255,255,255), intensity: float = 1.0):
        super().__init__()
        self.color = color
        self.intensity = intensity
    
    def GetDiffuseFactor(self, worldPosition: np.ndarray, normal: np.ndarray) -> float:
        raise Exception("Not implemented")