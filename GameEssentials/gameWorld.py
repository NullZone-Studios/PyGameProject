from .gameObject import GameObject
from .component import Component
from Components import Camera
from typing import Optional

class GameWorld:
    def __init__(self):
        self.GameObjects: list[GameObject] = []
        self.MainCamera: Optional[Camera] = None
    
    def Awaken(self):
        for obj in self.GameObjects:
            obj.Awake()
            
    def Start(self):
        for obj in self.GameObjects:
            obj.Start()
    
    def FindByTag(self, tag: str) -> Optional[GameObject]:
        for obj in self.GameObjects:
            if obj.Tag == tag:
                return obj
        return None
    
    def FindByName(self, name: str) -> Optional[GameObject]:
        for obj in self.GameObjects:
            if obj.Name == name:
                return obj
        return None
        
    def FindMainCamera(self) -> Optional[Component]:
        if self.MainCamera:
            return self.MainCamera
        
        for obj in self.GameObjects:
            camera = obj.GetComponent(Camera)
            if camera:
                self.MainCamera = camera
                return camera
        return None
    
    def Update(self, deltaTime: float):
        for obj in self.GameObjects[:]:
            obj.Update(deltaTime)
            if obj._destroyed:
                self.GameObjects.remove(obj)