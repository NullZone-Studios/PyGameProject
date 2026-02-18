from GameEssentials import Component
from pygame import Vector3
from typing import Tuple

class BoxCollider(Component):
    def __init__(self, size: Vector3, offset: Vector3 | None = None, isTrigger: bool = False):
        super().__init__()
        self.Size = size
        self.Offset = offset or Vector3(0, 0, 0)
        self.IsTrigger = isTrigger
    
    def GetWorldBounds(self) -> Tuple[Vector3, Vector3]:
        transform = self.GameObject.Transform
        scale = transform.Scale
        half = Vector3(
            self.Size.x * scale.x,
            self.Size.y * scale.y,
            self.Size.z * scale.z
        ) * 0.5
        center = transform.WorldPosition + self.Offset
        min_v = center - half
        max_v = center + half
        return min_v, max_v

    def Intersects(self, other: "BoxCollider") -> bool:
        a_min, a_max = self.GetWorldBounds()
        b_min, b_max = other.GetWorldBounds()
        return (
            a_min.x <= b_max.x and a_max.x >= b_min.x and
            a_min.y <= b_max.y and a_max.y >= b_min.y and
            a_min.z <= b_max.z and a_max.z >= b_min.z
        )
