from Components import Script, BoxCollider
from pygame import Vector3

class CollisionLogger(Script):
    def __init__(self, size: Vector3, label: str = ""):
        super().__init__()
        self.size = size
        self.label = label

    def Start(self):
        if not self.GameObject.GetFirstComponentOfType(BoxCollider):
            self.GameObject.AddComponent(BoxCollider(self.size))

    def OnCollisionEnter(self, other: BoxCollider):
        name = self.label or self.GameObject.Name
        print(f"[CollisionEnter] {name} hit {other.GameObject.Name}")

    def OnCollisionExit(self, other: BoxCollider):
        name = self.label or self.GameObject.Name
        print(f"[CollisionExit] {name} left {other.GameObject.Name}")
