from __future__ import annotations

from Component import Component
from GameEssentials.Vector2 import Vector2
from typing import Optional, Type

class GameObject:
    def __init__(self, name: str, parent: Optional["GameObject"] = None):
        self.Name = name
        self.Parent: Optional[GameObject] = None
        self.Components: list[Component] = []
        self.Children: list[GameObject] = []
        self.Position = Vector2()
        self._componentLookup: dict[Type[Component], Component] = {}
        self.Enabled = True
        
        if parent is not None:
            parent.AddChild(self)

# ---------- Children ------------

    def AddChild(self, child: "GameObject"):
        if child.Parent is not None:
            child.Parent.RemoveChild(child)
        
        child.Parent = self
        self.Children.append(child)
        
    def RemoveChild(self, child: "GameObject"):
        if child in self.Children:
            child.Parent = None
            self.Children.remove(child)
        
    def FindChildByName(self, name: str):
        for child in self.Children:
            if child.Name == name:
                return child
        return None
    
# ----------- Components -----------
    
    def AddComponent(self, component: Component):
        if self.FindFirstComponentOfType(type(component)) is not None:
            raise Exception(f"{type(component).__name__} already exists on {self.Name}")
        component.GameObject = self
        self.Components.append(component)
        self._componentLookup[type(component)] = component
    
    def RemoveComponent(self, component: Component):
        component_type = type(component)
        
        if component in self.Components:
            self.Components.remove(component)
            self._componentLookup.pop(component_type, None)
            component.GameObject = None
        
    def FindFirstComponentOfType(self, componentType : type):
        return self._componentLookup.get(componentType)
    
# --------- Lifecycle ----------

    def Awake(self):
        for component in self.Components[:]:
            component.Awake()
        
        for child in self.Children[:]:
            child.Awake()
            
    def Start(self):
        for component in self.Components[:]:
            component.Start()
        
        for child in self.Children[:]:
            child.Start()
    
    def Update(self, deltaTime: float):
        if not self.Enabled:
            return
        
        for component in self.Components[:]:
            component.Update(deltaTime)
            
        for child in self.Children[:]:
            child.Update(deltaTime)
            
    def Enable(self):
        if self.Enabled:
            return
        
        self.Enabled = True
        
        for component in self.Components:
            component.OnEnable()
            
        for child in self.Children[:]:
            child.Enable()

    def Disable(self):
        if not self.Enabled:
            return
        
        self.Enabled = False
        
        for component in self.Components:
            component.OnDisable()
        
        for child in self.Children[:]:
            child.Disable()