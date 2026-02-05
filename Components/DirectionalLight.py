import pygame
import numpy as np
from Components import Light, Transform

class DirectionalLight(Light):
    def GetDirection(self):
        transform: Transform = self.GameObject.GetFirstComponentOfType(Transform)
        if not transform:
            return np.array([0,1,0], dtype=float)
        
        direction = transform.WorldRotationMatrix @ np.array([0,0,-1])
        length = np.linalg.norm(direction)
        if length > 0:
            direction /= length
        return direction
    
    def GetDiffuseFactor(self, worldPosition, normal) -> float:
        if not self.Enabled:
            return 0
        direction = self.GetDirection()
        return max(np.dot(normal, -direction), 0) * self.intensity