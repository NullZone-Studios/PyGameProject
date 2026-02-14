from GameEssentials.component import Component
from Components.UI.UIElement import Element
from Components.camera import Camera
from Components.light import Light
from typing import Callable
import pygame
import numpy as np
from .UIEvent import Event
from .UIInput import UIInputLayer

class Canvas(Component):
    def __init__(self, width: int = 100, height: int = 100, layer: int = 0, color: pygame.Color = pygame.Color(0,0,0,0), worldSpace: bool = False, inputSystem = None):
        super().__init__()
        self.root = Element("root")
        self.surface: pygame.Surface = pygame.Surface((width,height), pygame.SRCALPHA)
        self.color = color
        self.worldSpace = worldSpace
        self.layer = layer
        self.inputSystem = inputSystem
        
    def Start(self):
        self.inputSystem.AddLayer(UIInputLayer(self))
        return super().Start()
        
    
    @property
    def Position2D(self) -> pygame.Vector2:
        if not self.GameObject.Transform:
            return pygame.Vector2(0,0)
        
        return pygame.Vector2(
            self.GameObject.Transform.Position.x,
            self.GameObject.Transform.Position.y
        )
            
    def PrepareSurface(self):
        self.surface.fill(self.color)
    
    def GetRenderData(self, camera: Camera, lights: list[Light]):
        self.PrepareSurface()
        self.root.ResolveStyle(None)
        self.root.Layout(pygame.Rect(0,0, *self.surface.get_size()))
        self.root.Render(self.surface)
        
        if self.worldSpace:
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
            ambient = 1 # set to 1 for now to ensure UI is lit up in world space
            r = int(255 * ambient)
            g = int(255 * ambient)
            b = int(255 * ambient)

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
        else:
            return{
                "type": "overlay",
                "layer": self.layer,
                "surface": self.surface,
                "position": self.Position2D
            }       
    
        