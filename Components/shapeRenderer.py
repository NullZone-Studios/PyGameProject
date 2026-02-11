import pygame
import numpy as np
from GameEssentials import Component
from Components import PolygonRenderer

class ShapeRenderer(Component):
    def __init__(self, shape: str = "cube", color = pygame.Color(1, 255, 255), scale = (1, 1, 1), offset = (0, 0, 0), rotation_offset = (0, 0, 0)):
        super().__init__()
        self.shape = shape
        self.color = color
        self.scale = np.array(scale)
        self.offset = np.array(offset)
        self.rotation_offset = rotation_offset
        
    def Start(self):
        if self.shape.lower() == "cube":
            self.CreateCube()
        elif self.shape.lower() == "pentagon":
            raise NotImplementedError("Pentagon shape not implemented yet.")
        elif self.shape.lower() == "cone":
            self.CreateCone()
        else:
            raise ValueError(f"Shape '{self.shape}' is not supported.")

        return super().Start()


    def CreateCube(self):
        from GameEssentials.gameObject import GameObject
        # shorthand
        c = self.color
        s = 1.0  # half-size

        # ---------- FRONT ----------
        front = GameObject("Front", "Face", self.GameObject)
        if self.rotation_offset != (0, 0, 0):
            front.Transform.Rotate(pitch=self.rotation_offset[0], yaw=self.rotation_offset[1], roll=self.rotation_offset[2])
        front.AddComponent(PolygonRenderer(
            vertices=[
                np.array([-s, -s,  s]) * self.scale + self.offset,
                np.array([ s, -s,  s]) * self.scale + self.offset,
                np.array([ s,  s,  s]) * self.scale + self.offset,
                np.array([-s,  s,  s]) * self.scale + self.offset,
            ],
            color=c
        ))

        # ---------- BACK ----------
        back = GameObject("Back", "Face", self.GameObject)
        if self.rotation_offset != (0, 0, 0):
            back.Transform.Rotate(pitch=self.rotation_offset[0], yaw=self.rotation_offset[1], roll=self.rotation_offset[2])
        back.AddComponent(PolygonRenderer(
            vertices=[
                np.array([ s, -s, -s]) * self.scale + self.offset,
                np.array([-s, -s, -s]) * self.scale + self.offset,
                np.array([-s,  s, -s]) * self.scale + self.offset,
                np.array([ s,  s, -s]) * self.scale + self.offset,
            ],
            color=c
        ))

        # ---------- LEFT ----------
        left = GameObject("Left", "Face", self.GameObject)
        if self.rotation_offset != (0, 0, 0):
            left.Transform.Rotate(pitch=self.rotation_offset[0], yaw=self.rotation_offset[1], roll=self.rotation_offset[2])
        left.AddComponent(PolygonRenderer(
            vertices=[
                np.array([-s, -s, -s]) * self.scale + self.offset,
                np.array([-s, -s,  s]) * self.scale + self.offset,
                np.array([-s,  s,  s]) * self.scale + self.offset,
                np.array([-s,  s, -s]) * self.scale + self.offset,
            ],
            color=c
        ))

        # ---------- RIGHT ----------
        right = GameObject("Right", "Face", self.GameObject)
        if self.rotation_offset != (0, 0, 0):
            right.Transform.Rotate(pitch=self.rotation_offset[0], yaw=self.rotation_offset[1], roll=self.rotation_offset[2])
        right.AddComponent(PolygonRenderer(
            vertices=[
                np.array([ s, -s,  s]) * self.scale + self.offset,
                np.array([ s, -s, -s]) * self.scale + self.offset,
                np.array([ s,  s, -s]) * self.scale + self.offset,
                np.array([ s,  s,  s]) * self.scale + self.offset,
            ],
            color=c
        ))

        # ---------- TOP ----------
        top = GameObject("Top", "Face", self.GameObject)
        if self.rotation_offset != (0, 0, 0):
            top.Transform.Rotate(pitch=self.rotation_offset[0], yaw=self.rotation_offset[1], roll=self.rotation_offset[2])
        top.AddComponent(PolygonRenderer(
            vertices=[
                np.array([-s,  s,  s]) * self.scale + self.offset,
                np.array([ s,  s,  s]) * self.scale + self.offset,
                np.array([ s,  s, -s]) * self.scale + self.offset,
                np.array([-s,  s, -s]) * self.scale + self.offset,
            ],
            color=c
        ))

        # ---------- BOTTOM ----------
        bottom = GameObject("Bottom", "Face", self.GameObject)
        if self.rotation_offset != (0, 0, 0):
            bottom.Transform.Rotate(pitch=self.rotation_offset[0], yaw=self.rotation_offset[1], roll=self.rotation_offset[2])
        bottom.AddComponent(PolygonRenderer(
            vertices=[
                np.array([-s, -s, -s]) * self.scale + self.offset,
                np.array([ s, -s, -s]) * self.scale + self.offset,
                np.array([ s, -s,  s]) * self.scale + self.offset,
                np.array([-s, -s,  s]) * self.scale + self.offset,
            ],
            color=c
        ))
    
    def CreateCone(self):
        from GameEssentials.gameObject import GameObject
        # Triangular pyramid with equilateral base
        c = self.color
        s = 1.0  # half-size
        
        # Define pyramid vertices with equilateral triangle base
        # Base vertices positioned at 120-degree intervals around origin
        # This creates an equilateral triangle centered at (0, -s, 0)
        sqrt3_half = np.sqrt(3) / 2
        v0 = np.array([0, -s, s]) * self.scale + self.offset  # top of triangle
        v1 = np.array([-s * sqrt3_half, -s, -s/2]) * self.scale + self.offset  # bottom-left
        v2 = np.array([s * sqrt3_half, -s, -s/2]) * self.scale + self.offset  # bottom-right
        
        # Apex vertex (tip, centered above the base triangle)
        v3 = np.array([0, s, 0]) * self.scale + self.offset
        
        # ---------- BASE ----------
        base = GameObject("Base", "Face", self.GameObject)
        if self.rotation_offset != (0, 0, 0):
            base.Transform.Rotate(pitch=self.rotation_offset[0], yaw=self.rotation_offset[1], roll=self.rotation_offset[2])
        base.AddComponent(PolygonRenderer(
            vertices=[v0, v1, v2],
            color=c
        ))
        
        # ---------- FRONT FACE ----------
        front = GameObject("Front", "Face", self.GameObject)
        if self.rotation_offset != (0, 0, 0):
            front.Transform.Rotate(pitch=self.rotation_offset[0], yaw=self.rotation_offset[1], roll=self.rotation_offset[2])
        front.AddComponent(PolygonRenderer(
            vertices=[v0, v3, v1],
            color=c
        ))
        
        # ---------- LEFT FACE ----------
        left = GameObject("Left", "Face", self.GameObject)
        if self.rotation_offset != (0, 0, 0):
            left.Transform.Rotate(pitch=self.rotation_offset[0], yaw=self.rotation_offset[1], roll=self.rotation_offset[2])
        left.AddComponent(PolygonRenderer(
            vertices=[v1, v3, v2],
            color=c
        ))
        
        # ---------- RIGHT FACE ----------
        right = GameObject("Right", "Face", self.GameObject)
        if self.rotation_offset != (0, 0, 0):
            right.Transform.Rotate(pitch=self.rotation_offset[0], yaw=self.rotation_offset[1], roll=self.rotation_offset[2])
        right.AddComponent(PolygonRenderer(
            vertices=[v2, v3, v0],
            color=c
        ))