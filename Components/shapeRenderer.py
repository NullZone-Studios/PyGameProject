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
            raise NotImplementedError("Cone shape not implemented yet.")
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