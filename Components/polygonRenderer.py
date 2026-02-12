import pygame
import numpy as np
from GameEssentials import Component
from Components.transform import Transform
from Components.light import Light
from Components.camera import Camera

class PolygonRenderer(Component):
    def __init__(self, vertices: list[np.ndarray], color: pygame.Color = pygame.Color(255,255,255), filled: bool = True, backfaceCulling: bool = True):
        super().__init__()
        self.vertices: list[np.ndarray] = vertices
        self.color: pygame.Color = color
        self.filled: bool = filled
        self.backfaceCulling: bool = backfaceCulling
        
    def GetRenderData(self, camera: Camera, lights: list[Light] = None):
        transform: Transform = self.GameObject.Transform
        if not transform:
            return None
        
        cameraTransform: Transform = camera.GameObject.Transform
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

        viewVerticies = self.toViewSpace(worldVertices, camera)
        triangles = []
        near = camera.Near
        
        for i in range(1,len(viewVerticies) -1):
            baseTriangle = [viewVerticies[0], viewVerticies[i], viewVerticies[i+1]]
            clipped = self.clipTriangleNear(baseTriangle, camera.Near)
            
            for triangle in clipped:
                points, depths = self.projectTriangle(triangle, camera)
                triangles.append({
                    "type": "triangle",
                    "points": points,
                    "depth": sum(depths) / len(depths),
                    "color": shadeColor,
                    "normal": normal,
                    "filled": self.filled
                })

        return triangles
    
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
    
    def toViewSpace(self, worldVerticies: list[np.ndarray] ,camera: Camera):
        view = camera.ViewMatrix
        viewVerticies = []
        for p in worldVerticies:
            p4 = np.array([p[0], p[1],p[2],1.0])
            v = view @ p4
            viewVerticies.append(v)
        return viewVerticies
    
    def clipTriangleNear(self, triangle: list, near: float) -> list:
        inside = []
        outside = []

        for v in triangle:
            if -v[2] >= near:  # note: -v[2] because view Z is negative in front
                inside.append(v)
            else:
                outside.append(v)

        if len(inside) == 0:
            return []

        def intersect(v1, v2):
            t = (near + v1[2]) / (v1[2] - v2[2])
            return v1 + t * (v2 - v1)

        # all vertices inside, return original
        if len(inside) == 3:
            return [triangle]

        # one vertex inside
        if len(inside) == 1:
            v0 = inside[0]
            v1 = intersect(v0, outside[0])
            v2 = intersect(v0, outside[1])
            return [[v0, v1, v2]]

        # two vertices inside
        if len(inside) == 2:
            v0, v1 = inside
            v2 = intersect(v0, outside[0])
            v3 = intersect(v1, outside[0])
            return [[v0, v1, v3], [v0, v3, v2]]

        return []

            
    def projectTriangle(self, triangle: list, camera: Camera):
        points = []
        depths = []
        
        for v in triangle:
            clip = camera.ProjectionMatrix @ v
            clip /= clip[3]
            
            x = (clip[0] * .5 + .5) * camera.ScreenWidth
            y = (1 - (clip[1] * .5 + .5)) * camera.ScreenHeight
            
            points.append(pygame.Vector2(x,y))
            depths.append(-v[2])
        return points, depths
