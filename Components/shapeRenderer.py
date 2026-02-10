import pygame
import numpy as np
from GameEssentials import Component
from Components import PolygonRenderer

class ShapeRenderer(Component):
    def __init__(self, shape: str = "cube"):
        super().__init__()
        self.shape = shape
        
    def Start(self):
        if self.shape.lower() == "cube":
            self.CreateCube()
        elif self.shape.lower() == "pentagon":
            raise NotImplementedError("Pentagon shape not implemented yet.")
        elif self.shape.lower() == "cone":
            raise NotImplementedError("Cone shape not implemented yet.")

        return super().Start()


    def CreateCube(self):
        from GameEssentials.gameObject import GameObject
        # shorthand
        c = pygame.Color(1, 255, 255)
        s = 1.0  # half-size

        # ---------- FRONT ----------
        front = GameObject("Front", "Face", self.GameObject)
        front.AddComponent(PolygonRenderer(
            vertices=[
                np.array([-s, -s,  s]),
                np.array([ s, -s,  s]),
                np.array([ s,  s,  s]),
                np.array([-s,  s,  s]),
            ],
            color=c
        ))

        # ---------- BACK ----------
        back = GameObject("Back", "Face", self.GameObject)
        back.AddComponent(PolygonRenderer(
            vertices=[
                np.array([ s, -s, -s]),
                np.array([-s, -s, -s]),
                np.array([-s,  s, -s]),
                np.array([ s,  s, -s]),
            ],
            color=c
        ))

        # ---------- LEFT ----------
        left = GameObject("Left", "Face", self.GameObject)
        left.AddComponent(PolygonRenderer(
            vertices=[
                np.array([-s, -s, -s]),
                np.array([-s, -s,  s]),
                np.array([-s,  s,  s]),
                np.array([-s,  s, -s]),
            ],
            color=c
        ))

        # ---------- RIGHT ----------
        right = GameObject("Right", "Face", self.GameObject)
        right.AddComponent(PolygonRenderer(
            vertices=[
                np.array([ s, -s,  s]),
                np.array([ s, -s, -s]),
                np.array([ s,  s, -s]),
                np.array([ s,  s,  s]),
            ],
            color=c
        ))

        # ---------- TOP ----------
        top = GameObject("Top", "Face", self.GameObject)
        top.AddComponent(PolygonRenderer(
            vertices=[
                np.array([-s,  s,  s]),
                np.array([ s,  s,  s]),
                np.array([ s,  s, -s]),
                np.array([-s,  s, -s]),
            ],
            color=c
        ))

        # ---------- BOTTOM ----------
        bottom = GameObject("Bottom", "Face", self.GameObject)
        bottom.AddComponent(PolygonRenderer(
            vertices=[
                np.array([-s, -s, -s]),
                np.array([ s, -s, -s]),
                np.array([ s, -s,  s]),
                np.array([-s, -s,  s]),
            ],
            color=c
        ))