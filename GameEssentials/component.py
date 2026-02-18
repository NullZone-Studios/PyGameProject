from typing import Optional, Type

class Component:
    def __init__(self):
        self.GameObject = None # type: ignore
        self.Enabled = True
        
    def Enable(self):
        self.Enabled = True
        self.OnEnable()
    
    def Disable(self):
        self.Enabled = False
        self.OnDisable()
    
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

    def OnCollisionEnter(self, other):
        return

    def OnCollisionStay(self, other):
        return

    def OnCollisionExit(self, other):
        return
    
    def OnDestroy(self):
        return
