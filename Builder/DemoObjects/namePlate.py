import pygame
from GameEssentials import GameObject
from Components import UI

class NamePlate(GameObject):
    def __init__(self, name="NamePlate", tag="NamePlate", parent = None, text: str = "Nameplate"):
        super().__init__(name, tag, parent)
        
        canvas: UI.Canvas = self.AddComponent(UI.Canvas(width=500, height=200, worldSpace=True, color=pygame.Color("white")))
        centeringDiv = canvas.root.AddChild(UI.Element())
        centeringDiv.style = UI.Style(
            display="flex",
            verticalAlign="center",
            flexDirection="row",
        )
        label = centeringDiv.AddChild(UI.Label(text=text))
        label.style = UI.Style(
            font= pygame.font.SysFont("arial", 90, bold=True),
            margin=(0,10)
        )