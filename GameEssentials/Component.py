from typing import Optional, Type

class Component:
    def __init__(self):
        self.GameObject: GameObject | None = None # type: ignore
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