from GameEssentials import GameObject
from Components import Camera
from typing import Optional

class GameWorld:
    GameObjects: list[GameObject] = []
    MainCamera: Optional[Camera] = None
    
    @staticmethod 
    def FindByTag(tag: str) -> Optional[GameObject]:
        for obj in GameWorld.GameObjects:
            if obj.Tag == tag:
                return obj
        return None
    
    @staticmethod
    def FindByName(name: str) -> Optional[GameObject]:
        for obj in GameWorld.GameObjects:
            if obj.Name == name:
                return obj
        return None
    
    @staticmethod
    def Instantiate(gameObject: GameObject):
        GameWorld.GameObjects.append(gameObject)
        
    @staticmethod
    def FindMainCamera():
        for obj in GameWorld.GameObjects:
            camera = obj.GetFirstComponentOfType(Camera)
            if camera:
                GameWorld.MainCamera = camera
        return None