from Components import Script
from Components.UI.UILabel import Label

class PositionToLabel(Script):
    def __init__(self, label: Label):
        super().__init__()
        self.label: Label = label
        
    def Update(self, deltaTime):
        position = self.GameObject.Transform.Position
        self.label.Text = f"X: {round(position.x, 2)} \nY: {round(position.y,2)} \nZ: {round(position.z, 2)}"
        return super().Update(deltaTime)