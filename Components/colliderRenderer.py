import pygame
import numpy as np
from GameEssentials import Component
from Components.camera import Camera
from Components.collider import BoxCollider

class DebugColliderRenderer(Component):
    def __init__(self, color: pygame.Color = pygame.Color(0, 255, 0), thickness: int = 1):
        super().__init__()
        self.color = color
        self.thickness = thickness

    def GetRenderData(self, camera: Camera, lights = None):
        collider = self.GameObject.GetFirstComponentOfType(BoxCollider)
        if not collider:
            return None

        min_v, max_v = collider.GetWorldBounds()
        corners = [
            pygame.Vector3(min_v.x, min_v.y, min_v.z),
            pygame.Vector3(max_v.x, min_v.y, min_v.z),
            pygame.Vector3(max_v.x, max_v.y, min_v.z),
            pygame.Vector3(min_v.x, max_v.y, min_v.z),
            pygame.Vector3(min_v.x, min_v.y, max_v.z),
            pygame.Vector3(max_v.x, min_v.y, max_v.z),
            pygame.Vector3(max_v.x, max_v.y, max_v.z),
            pygame.Vector3(min_v.x, max_v.y, max_v.z)
        ]

        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]

        def project_point(world_point: pygame.Vector3):
            world = np.array([world_point.x, world_point.y, world_point.z, 1.0])
            view = camera.ViewMatrix @ world
            depth = -view[2]
            if depth <= camera.Near:
                return None
            clip = camera.ProjectionMatrix @ view
            if clip[3] == 0:
                return None
            clip /= clip[3]
            x = (clip[0] * 0.5 + 0.5) * camera.ScreenWidth
            y = (1 - (clip[1] * 0.5 + 0.5)) * camera.ScreenHeight
            return pygame.Vector2(x, y), depth

        projected = [project_point(corner) for corner in corners]

        lines = []
        for a, b in edges:
            if projected[a] is None or projected[b] is None:
                continue
            start, depth_a = projected[a]
            end, depth_b = projected[b]
            lines.append({
                "type": "line",
                "start": start,
                "end": end,
                "color": self.color,
                "thickness": self.thickness,
                "depth": (depth_a + depth_b) * 0.5
            })

        return lines
