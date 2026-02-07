from GameEssentials.component import Component
from GameEssentials.gameObject import GameObject
from Components.light import Light
from Components.camera import Camera
from Components.UI.UIElement import Element

class Canvas(Component):
    class CanvasRenderMode:
        SCREEN_SPACE = 0
        WORLD_SPACE = 1
    
    def __init__(self, renderMode=CanvasRenderMode.SCREEN_SPACE):
        super().__init__()
        self.renderMode = renderMode

    def GetRenderData(self, camera: Camera, lights: list[Light]):
        renderItems = []

        def Collect(obj: GameObject):
            for component in obj.Components:
                if isinstance(component, Element):
                    data = component.BuildRenderData(self, camera)
                    if data:
                        if isinstance(data, list):
                            renderItems.extend(data)
                        else:
                            renderItems.append(data)

            for child in obj.Children:
                Collect(child)

        Collect(self.GameObject)
        return renderItems
