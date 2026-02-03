from typing import Optional, Type
from GameObject import GameObject

class Component:
    def __init__(self):
        self.GameObject: GameObject | None = None
        self.Enabled = True
        
    def Enable(self):
        self.Enabled = True
    
    def Disable(self):
        self.Enabled = False
    
    def OnEnable(self):
        return
    
    def OnDisable(self):
        return
    
    def Awake(self):
        return
    
    def Start(self):
        return
    
    def Update(self, deltaTime: float):
        return