from GameEssentials.component import Component
from Components.light import Light
from Components.camera import Camera

class Canvas(Component):
    class CanvasRenderMode:
        SCREEN_SPACE = 0
        WORLD_SPACE = 1
    
    def __init__(self, renderMode: CanvasRenderMode = CanvasRenderMode.SCREEN_SPACE):
        super().__init__()
        self.renderMode = renderMode
        
    def GetRenderData(self, camera: Camera, lights: list[Light]):
        pass