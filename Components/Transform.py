from GameEssentials import Component
from typing import Type, Optional
from pygame import Vector3
import numpy as np

class Transform(Component):
    def __init__(self, position: Optional[Vector3] = None, rotation: Optional[Vector3] = None, scale: Optional[Vector3] = None):
        super().__init__()
        self.Position: Vector3 = position or Vector3(0,0,0)
        self.Rotation: Vector3 = rotation or Vector3(0,0,0)
        self.Scale: Vector3 = scale or Vector3(1,1,1)
        
        self._localMatrix = np.identity(4)
        self._worldMatrix = np.identity(4)
        
    def Translate(self, x: float = 0, y: float = 0, z: float = 0):
        self.Position.x += x
        self.Position.y += y
        self.Position.z += z
        
    def SetRotation(self, rotation: Vector3):
        self.Rotation = rotation
        
    def Rotate(self, pitch: float = 0, yaw: float =0, roll: float =0):
        self.Rotation.x += pitch
        self.Rotation.y += yaw
        self.Rotation.z += roll
    
    def SetScale(self, scale: Vector3):
        self.Scale = scale
        
    def ComputeLocalMatrix(self):
        # Translation
        translate = np.identity(4)
        translate[:3,3] = [self.Position.x, self.Position.y, self.Position.z]
        
        # Rotation
        rx,ry,rz = self.Rotation.x, self.Rotation.y, self.Rotation.z
        
        Rx = np.array([[1,0,0,0],
                      [0,np.cos(rx), -np.sin(rx),0],
                      [0,np.sin(rx), np.cos(rx), 0],
                      [0,0,0,1]])
        
        Ry = np.array([[np.cos(ry), 0, np.sin(ry), 0],
                       [0,1,0,0],
                       [-np.sin(ry), 0, np.cos(ry), 0],
                       [0,0,0,1]])
        
        Rz = np.array([[np.cos(rz), -np.sin(rz),0,0],
                       [np.sin(rz), np.cos(rz), 0,0],
                       [0,0,1,0],
                       [0,0,0,1]])
        
        rotation = Rz @ Ry @ Rx
        
        # Scale
        scale = np.identity(4)
        scale[0,0] = self.Scale.x
        scale[1,1] = self.Scale.y
        scale[2,2] = self.Scale.z
        
        # Local Matrix
        self._localMatrix = translate @ rotation @ scale
        return self._localMatrix
    
    def ComputeWorldMatrix(self):
        localMatrix = self.ComputeLocalMatrix()
        
        if self.GameObject and self.GameObject.Parent:
            parentTransform = self.GameObject.Parent.GetFirstComponentOfType(Transform)
            if parentTransform:
                self._worldMatrix = parentTransform.ComputeWorldMatrix() @ localMatrix
                return self._worldMatrix
        self._worldMatrix = localMatrix
        return self._worldMatrix
    
    def ComputeRotationMatrix(self):
        rx,ry,rz = self.Rotation
        cx,sx = np.cos(rx), np.sin(rx)
        cy,sy = np.cos(ry), np.sin(ry)
        cz,sz = np.cos(rz), np.sin(rz)
        
        Rx = np.array([[1,0,0],[0,cx,-sx],[0,sx,cx]])
        Ry = np.array([[cy,0,sy],[0,1,0,[-sy,0,cy]]])
        Rz = np.array([[cz,-sz,0],[sz,cz,0],[0,0,1]])
        
        return Rz @ Ry @ Rx
    
    @property
    def WorldPosition(self) -> Vector3:
        self.ComputeWorldMatrix()
        return Vector3(*self._worldMatrix[:3,3])