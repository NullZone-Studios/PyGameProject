from GameEssentials import GameObject, Input
from Builder.DemoScripts import Move
from Components import ShapeRenderer, UI
import pygame
from typing import Optional

class Player(GameObject):
    def __init__(self, name: str = "Player", tag: str = "Player", parent: Optional[GameObject] = None, inputHandler: Optional[Input.GameInput] = None):
        super().__init__(name, tag, parent)
        self.AddComponent(Move(inputHandler))
        self.AddComponent(ShapeRenderer(shape="cube", color=pygame.Color("cornflowerblue"), scale=(1,1,1)))
        canvas: UI.Canvas = self.AddComponent(UI.Canvas(width=500, height=500))
        container: UI.Element = canvas.root.AddChild(UI.Element())
        container.style = UI.Style(
            display="flex",
            flexDirection="row"
        )
        self.label: UI.Label = container.AddChild(UI.Label())
        self.label.style = UI.Style(
            font= pygame.font.SysFont("arial", 25, bold=True),
            color=pygame.Color("white"),
            margin=(10,10)
        )
        
    def Update(self, deltaTime):
        self.label.Text = f"X: {self.Transform.Position.x:.2f}\nY: {self.Transform.Position.y:.2f}\nZ: {self.Transform.Position.z:.2f}"
        return super().Update(deltaTime)