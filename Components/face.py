from Components.polygonRenderer import PolygonRenderer
import pygame
import numpy as np
from typing import Optional

class Face(PolygonRenderer):
    def __init__(self, width:float, depth:float, color: Optional[pygame.Color] = pygame.Color("white")):
        super().__init__(
            [
                np.array([-width, 0,  depth]),
                np.array([ width, 0,  depth]),
                np.array([ width, 0,  -depth]),
                np.array([-width, 0,  -depth]),
            ],
            color,
            filled=True,
            backfaceCulling=True
        )
    
    def GetRenderData(self, camera, lights = None):
        return super().GetRenderData(camera, lights)