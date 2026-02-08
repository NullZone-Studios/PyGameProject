from GameEssentials.component import Component
from GameEssentials.gameObject import GameObject
from Components.light import Light
from Components.camera import Camera
from Components.UI.UIElement import Element
from Components.UI.UIContainer import Container

class Canvas(Component):
    class CanvasRenderMode:
        SCREEN_SPACE = 0
        WORLD_SPACE = 1
    
    def __init__(self, renderMode=CanvasRenderMode.SCREEN_SPACE):
        super().__init__()
        self.renderMode = renderMode

    @property
    def isScreenSpace(self) -> bool:
        return self.renderMode == Canvas.CanvasRenderMode.SCREEN_SPACE

    def GetRenderData(self, camera: Camera, lights: list[Light]):
        renderItems = []
        
        def Layout(obj: GameObject):
            for component in obj.Components:
                if isinstance(component, Container):
                    component.ApplyLayout()
                    
            for child in obj.Children:
                Layout(child)

        def Collect(obj: GameObject):
            for component in obj.Components:
                if isinstance(component, Element):
                    if hasattr(component, "BuildRenderData"):
                        data = component.BuildRenderData(self, camera)
                        if data:
                            if isinstance(data, list):
                                renderItems.extend(data)
                            else:
                                renderItems.append(data)

            for child in obj.Children:
                Collect(child)

        Layout(self.GameObject)
        Collect(self.GameObject)
        return renderItems
