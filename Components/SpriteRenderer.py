import pygame
import numpy as np
import os
from GameEssentials import Component
from Components import Transform, Camera, Light
from typing import Optional
from pygame import Color

class SpriteRenderer(Component):
    def __init__(self, spritePath: str, color: Optional[Color] = Color(255,255,255,255)):
        super().__init__()
        self.surface: pygame.Surface = pygame.image.load(spritePath).convert_alpha()
        self.color: pygame.Color = color
    
    def GetRenderData(self, camera: Camera, lights: list[Light]):
        transform = self.GameObject.Transform
        if not transform:
            return None

        # world position of the sprite
        worldPos = np.array([
            transform.WorldPosition.x,
            transform.WorldPosition.y,
            transform.WorldPosition.z,
            1.0
        ])

        viewPos = camera.ViewMatrix @ worldPos
        depth = -viewPos[2]
        if depth <= camera.Near:
            return None

        clip = camera.ProjectionMatrix @ viewPos
        if clip[3] == 0:
            return None
        ndc = clip / clip[3]

        # --- simple lighting ---
        ambient = 0.25
        r = int(self.color.r * ambient)
        g = int(self.color.g * ambient)
        b = int(self.color.b * ambient)

        if lights:
            for light in lights:
                # assume GetDiffuseFactor can work with just the direction to the light
                lightDir = light.GameObject.Transform.WorldPosition - worldPos[:3]  # if point light
                lightDist = np.linalg.norm(lightDir)
                if lightDist > 0:
                    lightDir /= lightDist
                factor = max(0, np.dot(np.array([0,0,1]), lightDir))  # simple forward-facing normal
                r += int(self.color.r * factor * (light.color.r / 255))
                g += int(self.color.g * factor * (light.color.g / 255))
                b += int(self.color.b * factor * (light.color.b / 255))

        shadedColor = pygame.Color(
            max(0, min(r, 255)),
            max(0, min(g, 255)),
            max(0, min(b, 255))
        )
        
        scale = camera.FocalLength / depth
        w = max(1, int(self.surface.get_width() * scale * transform.Scale.x))
        h = max(1, int(self.surface.get_height() * scale * transform.Scale.y))

        return {
            "type": "sprite",
            "depth": depth,
            "ndc": ndc,
            "surface": self.surface,
            "color": shadedColor,
            "width": w,
            "height": h
        }

