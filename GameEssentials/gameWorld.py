from .gameObject import GameObject
from .component import Component
from Components import Camera
from typing import Optional

class GameWorld:
    instance: "GameWorld" = None
    
    @staticmethod
    def GetInstance() -> "GameWorld":
        if GameWorld.instance is None:
            GameWorld()
        return GameWorld.instance
    
    def __init__(self):
        if GameWorld.instance is not None:
            raise Exception("GameWorld is a singleton! use GetInstance()")
        GameWorld.instance = self
        self.GameObjects: list[GameObject] = []
        GameWorld.GameObjects = self.GameObjects
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
    
    def Instantiate(self, gameObject: GameObject):
        gameObject.Awake()
        gameObject.Start()
        self.GameObjects.append(gameObject)
        
    def FindMainCamera(self) -> Optional[Component]:
        if self.MainCamera:
            return self.MainCamera
        
        for obj in self.GameObjects:
            camera = obj.GetComponent(Camera)
            if camera:
                self.MainCamera = camera
                GameWorld.MainCamera = camera
                return camera
        return None
    
    def Update(self, deltaTime: float):
        for obj in self.GameObjects[:]:
            obj.Update(deltaTime)
            if obj._destroyed:
                self.GameObjects.remove(obj)