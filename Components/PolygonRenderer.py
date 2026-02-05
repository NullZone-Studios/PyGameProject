import pygame
import numpy as np
from GameEssentials import Component
from Components import Transform, Camera, Light

class PolygonRenderer(Component):
    def __init__(self, vertices: list[np.ndarray], color: pygame.Color = pygame.Color(255,255,255), filled: bool = True, backfaceCulling: bool = True):
        super().__init__()
        self.vertices: list[np.ndarray] = vertices
        self.color: pygame.Color = color
        self.filled: bool = filled
        self.backfaceCulling: bool = backfaceCulling
        
    def GetRenderData(self, camera: Camera, lights: list[Light] = None):
        transform: Transform = self.GameObject.GetFirstComponentOfType(Transform)
        if not transform:
            return None
        
        cameraTransform: Transform = camera.GameObject.GetFirstComponentOfType(Transform)
        if not cameraTransform:
            return None
        
        worldVertices = self.getWorldVertices(transform)
        cull, normal = self.computeCullAndNormal(worldVertices, cameraTransform)
        if cull:
            return None
        
        centroid = np.mean(worldVertices, axis=0)
        ambient = .15
        shadeR, shadeG, shadeB, = self.color.r * ambient, self.color.g * ambient, self.color.b * ambient
        if lights:
            for light in lights:
                factor = light.GetDiffuseFactor(centroid, normal)
                shadeR += self.color.r * light.color.r / 255 * factor
                shadeG += self.color.g * light.color.g / 255 * factor
                shadeB += self.color.b * light.color.b / 255 * factor
        
        shadeR = max(0, min(int(shadeR), 255))
        shadeG = max(0, min(int(shadeG), 255))
        shadeB = max(0, min(int(shadeB), 255))
        shadeColor = pygame.Color(shadeR, shadeG, shadeB)

        screenPoints, depths = self.projectVertices(worldVertices, camera)
        if screenPoints is None:
            return None
        
        return {
            "type": "polygon",
            "points": screenPoints,
            "depth": sum(depths) / len(depths),
            "normal": normal,
            "color": shadeColor,
            "filled": self.filled
        }
    
    def getWorldVertices(self, transform: Transform) -> list[np.ndarray]:
        vertices = []
        world = transform.ComputeWorldMatrix()
        for v in self.vertices:
            p = np.array([v[0], v[1], v[2], 1.0])
            p = world @ p
            vertices.append(p[:3])
        return vertices
            
    def computeCullAndNormal(self, worldVertices: list[np.ndarray], cameraTransform: Transform):
        if not self.backfaceCulling or len(worldVertices) < 3:
            return False, np.array([0,0,0], dtype=float)
        
        v0,v1,v2 = worldVertices[:3]
        edge1 = v1-v0
        edge2 = v2-v0
        
        normal = np.cross(edge1, edge2)
        length = np.linalg.norm(normal)
        if length == 0:
            return True, normal
        
        normal /= length

        cameraWorldPosition = cameraTransform.WorldPosition
        cameraPosition = np.array([cameraWorldPosition.x, cameraWorldPosition.y, cameraWorldPosition.z])
        
        faceToCamera = cameraPosition - v0
        cameraLength = np.linalg.norm(faceToCamera)
        if cameraLength == 0:
            return True, normal
        faceToCamera /= cameraLength
        
        dot = np.dot(normal, faceToCamera)
        cull = dot <= 0
        
        if dot < 0:
            normal = -normal
        
        return cull, normal
    
    def projectVertices(self, worldVertices: list[np.ndarray], camera: Camera):
        screenPoints: list[pygame.Vector2] = []
        depths: list[float] = []
        view = camera.ViewMatrix
        
        for p in worldVertices:
            p4 = np.array([p[0],p[1],p[2],1])
            viewPosition = view @ p4
            depth: int = viewPosition[2]
            
            clip = camera.ProjectionMatrix @ viewPosition
            if clip[3] <= 0:
                return None, None
            
            clip /= clip[3]
            
            x = (clip[0] * .5 + .5) * camera.ScreenWidth
            y = (1 - (clip[1] * .5 + .5)) * camera.ScreenHeight
            
            screenPoints.append(pygame.Vector2(x,y))
            depths.append(depth)
            
        return screenPoints, depths