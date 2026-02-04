import pygame
import numpy as np
import os
from GameEssentials import Component
from Components import Transform, Camera
from typing import Optional
from pygame import Color

class SpriteRenderer(Component):
    def __init__(self, spritePath: str, color: Optional[Color] = Color(255,255,255,255)):
        super().__init__()
        self.surface: pygame.Surface = pygame.image.load(spritePath).convert_alpha()
        self.color: pygame.Color = color
    
    def GetRenderData(self, camera: Camera):
        transform = self.GameObject.GetFirstComponentOfType(Transform)
        if not transform:
            return None
        
        worldPosition = np.array([transform.WorldPosition.x, transform.WorldPosition.y, transform.WorldPosition.z, 1.0])
        cameraPosition = camera.ViewMatrix @ worldPosition
        if cameraPosition[2] <= camera.Near:
            return None
        
        projection = camera.ProjectionMatrix @ cameraPosition
        
        if projection[3] == 0:
            return None
        
        projection /= projection[3]
        
        return {
            "depth": cameraPosition[2],
            "ndc": projection,
            "surface": self.surface
        }