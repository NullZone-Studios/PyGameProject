from Components import Light, Transform
import pygame
import numpy as np

class PointLight(Light):
    def __init__(self, color: pygame.Color = pygame.Color(255,255,255), intensity: float = 1.0, range: float =10.0):
        super().__init__(color, intensity)
        self.range = range
        
    def GetDiffuseFactor(self, worldPosition, normal) -> float:
        if not self.Enabled:
            return 0
        
        transform: Transform = self.GameObject.GetFirstComponentOfType(Transform)
        if not transform:
            return 0
        
        lightPosition = np.array([
            transform.WorldPosition.x,
            transform.WorldPosition.y,
            transform.WorldPosition.z
        ])
        
        direction = worldPosition - lightPosition
        distance = np.linalg.norm(direction)
        if distance == 0 or distance > self.range:
            return 0
        
        direction /= distance
        attenuation = 1.0 - (distance / self.range)
        return max(np.dot(normal, -dir), 0) * self.intensity * attenuation