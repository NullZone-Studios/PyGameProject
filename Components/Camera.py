import numpy as np
import pygame as pg
from GameEssentials import Component
from Components.transform import Transform

class CameraRenderType:
    ORTHOGRAPHIC = 0
    PERSPECTIVE = 1

class Camera(Component):
    def __init__(self, screenWidth: int = 1280, screenHeight: int = 720):
        super().__init__()
        self.FOV: int = 60
        self.Near: float = 0.1
        self.Far: float = 1000.0
        self.RenderType = CameraRenderType.PERSPECTIVE
        self.ScreenWidth = screenWidth
        self.ScreenHeight = screenHeight
    
    @property
    def ViewMatrix(self):
        transform: Transform = self.GameObject.Transform
        if not transform:
            return np.identity(4)
        worldMatrix = transform.ComputeWorldMatrix()
        return np.linalg.inv(worldMatrix)
    
    @property
    def ProjectionMatrix(self):
        aspect_ratio = self.ScreenWidth / self.ScreenHeight
        if self.RenderType == CameraRenderType.PERSPECTIVE:
            fov_rad = np.deg2rad(self.FOV)
            f = 1 / np.tan(fov_rad / 2)
            near, far = self.Near, self.Far
            projection = np.zeros((4,4))
            projection[0,0] = f / aspect_ratio
            projection[1,1] = f
            projection[2,2] = (far+near) / (near-far)
            projection[2,3] = (2 * far * near) / (near-far)
            projection[3,2] = -1
            return projection
        else:
            left, right = -10,10
            bottom, top = -10,10
            near,far = self.Near, self.Far
            projection = np.identity(4)
            projection[0,0] = 2 / (right-left)
            projection[1,1] = 2 / (top-bottom)
            projection[2,2] = -2 / (far-near)
            projection[0,3] = -(right+left) / (right-left)
            projection[1,3] = -(top+bottom) / (top-bottom)
            projection[2,3] = -(far+near) / (far-near)
            return projection
    
    @property
    def FocalLength(self):
        fovRadian = np.deg2rad(self.FOV)
        return 1 / np.tan(fovRadian * .5)