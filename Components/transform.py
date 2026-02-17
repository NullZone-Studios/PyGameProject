from GameEssentials import Component
from typing import Type, Optional
from pygame import Vector3
import numpy as np

class Transform(Component):
    TWO_PI = 2 * np.pi
    
    def __init__(self, position: Optional[Vector3] = None, rotation: Optional[Vector3] = None, scale: Optional[Vector3] = None):
        super().__init__()
        self.Position: Vector3 = position or Vector3(0,0,0)
        self.Rotation: Vector3 = rotation or Vector3(0,0,0)
        self.Scale: Vector3 = scale or Vector3(1,1,1)
        
        self.localMatrix = np.identity(4)
        self.worldMatrix = np.identity(4)
        self.rotationMatrix = np.identity(4)
        self.worldRotationMatrix = np.identity(4)
        
        self.dirtyFlags = {
            "local": True,
            "world": True,
            "rotation": True,
            "worldRotation": True
        }
    
    def markDirty(self, rotation: bool = False):
        self.dirtyFlags["local"] = True
        self.dirtyFlags["world"] = True
        if rotation:
            self.dirtyFlags["rotation"] = True
            self.dirtyFlags["worldRotation"] = True
            
        if self.GameObject:
            for child in self.GameObject.Children:
                childTransform = child.GetFirstComponentOfType(Transform)
                if childTransform:
                    childTransform.markDirty(rotation)
    
    def Translate(self, x: float = 0, y: float = 0, z: float = 0):
        self.Position.x += x
        self.Position.y += y
        self.Position.z += z
        self.markDirty()
        
    def SetPosition(self, position: Vector3):
        self.Position = position
        self.markDirty()
        
    def SetRotation(self, rotation: Vector3):
        self.Rotation = Vector3(
            rotation.x % self.TWO_PI,
            rotation.y % self.TWO_PI,
            rotation.z % self.TWO_PI
        )
        self.markDirty(rotation=True)
        
    def LookAt(self, target: Vector3):
        direction = target - self.WorldPosition
        if direction.length() == 0:
            return
        direction.normalize_ip()
        
        # Calculate yaw and pitch
        yaw = np.arctan2(direction.x, direction.z)
        pitch = np.arcsin(-direction.y)
        
        self.SetRotation(Vector3(pitch, yaw, self.Rotation.z))
        
    def Rotate(self, pitch: float = 0, yaw: float =0, roll: float =0):
        self.Rotation.x = (self.Rotation.x+pitch) % self.TWO_PI
        self.Rotation.y = (self.Rotation.y+yaw) % self.TWO_PI
        self.Rotation.z = (self.Rotation.z+roll) % self.TWO_PI
        self.markDirty(rotation=True)
    
    
    def SetScale(self, scale: Vector3):
        self.Scale = scale
        self.markDirty()
        
    def ComputeLocalMatrix(self):
        if not self.dirtyFlags["local"]:
            return self.localMatrix
        else:
            self.dirtyFlags["local"] = False
        
        # Translation
        translate = np.identity(4)
        translate[:3,3] = [self.Position.x, self.Position.y, self.Position.z]
        
        # Rotation
        rotation = self.ComputeRotationMatrix()
        
        # Scale
        scale = np.identity(4)
        scale[0,0] = self.Scale.x
        scale[1,1] = self.Scale.y
        scale[2,2] = self.Scale.z
        
        # Local Matrix
        self.localMatrix = translate @ rotation @ scale
        return self.localMatrix
    
    def ComputeWorldMatrix(self):
        if not self.dirtyFlags["world"]:
            return self.worldMatrix
        else:
            self.dirtyFlags["world"] = False
        
        localMatrix = self.ComputeLocalMatrix()
        
        if self.GameObject and self.GameObject.Parent:
            parentTransform = self.GameObject.Parent.GetFirstComponentOfType(Transform)
            if parentTransform:
                self.worldMatrix = parentTransform.ComputeWorldMatrix() @ localMatrix
                return self.worldMatrix
        self.worldMatrix = localMatrix
        return self.worldMatrix
    
    def ComputeRotationMatrix(self):
        if not self.dirtyFlags["rotation"]:
            return self.rotationMatrix
        else:
            self.dirtyFlags["rotation"] = False
        
        rx,ry,rz = self.Rotation
        cx,sx = np.cos(rx), np.sin(rx)
        cy,sy = np.cos(ry), np.sin(ry)
        cz,sz = np.cos(rz), np.sin(rz)
        
        Rx = np.array([[1,0,0,0],[0,cx,-sx,0],[0,sx,cx,0],[0,0,0,1]])
        Ry = np.array([[cy,0,sy,0],[0,1,0,0],[-sy,0,cy,0],[0,0,0,1]])
        Rz = np.array([[cz,-sz,0,0],[sz,cz,0,0],[0,0,1,0],[0,0,0,1]])
        
        self.rotationMatrix = Rz @ Ry @ Rx
        
        return self.rotationMatrix
    
    def ComputeWorldRotationMatrix(self):
        if not self.dirtyFlags["worldRotation"]:
            return self.worldRotationMatrix
        
        localRotation = self.ComputeRotationMatrix()

        # If has parent, multiply by parent's world rotation
        if self.GameObject and self.GameObject.Parent:
            parentTransform = self.GameObject.Parent.GetFirstComponentOfType(Transform)
            if parentTransform:
                self.worldRotationMatrix = parentTransform.ComputeWorldRotationMatrix() @ localRotation
                return self.worldRotationMatrix
        self.worldRotationMatrix = localRotation
        return self.worldRotationMatrix
    
    @property
    def WorldPosition(self) -> Vector3:
        self.ComputeWorldMatrix()
        return Vector3(*self.worldMatrix[:3,3])
    
    @property
    def Forward(self) -> Vector3:
        rotation = self.ComputeWorldRotationMatrix()
        f = Vector3(rotation[0,2], rotation[1,2], rotation[2,2])
        if f.length() != 0:
            f.normalize_ip()
        return f
    
    @property
    def Right(self) -> Vector3:
        rotation = self.ComputeWorldRotationMatrix()
        r = Vector3(rotation[0,0], rotation[1,0], rotation[2,0])
        if r.length() != 0:
            r.normalize_ip()
        return r
    
    @property
    def Up(self) -> Vector3:
        r = self.Right
        f = self.Forward
        u = f.cross(r)
        if u.length() != 0:
            u.normalize_ip()
        return u
