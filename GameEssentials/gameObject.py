from __future__ import annotations
from collections import defaultdict

from .component import Component
from Components.transform import Transform
from typing import Optional, Type, TypeVar, Generic
from pygame import Vector2

T = TypeVar("T", bound=Component)

class GameObject:
    def __init__(self, name: str, tag: str, parent: Optional["GameObject"] = None):
        self.Name = name
        self.Tag = tag
        self.Parent: Optional[GameObject] = None
        self.Components: list[Component] = []
        self.Children: list[GameObject] = []
        self._componentLookup: dict[type, list[Component]] = defaultdict(list)
        self.Enabled = True
        self._awoken = False
        self._started = False
        self._destroyed = False
        self.Transform = Transform()
        self.AddComponent(self.Transform)
        
        if parent is not None:
            parent.AddChild(self)

# ---------- Children ------------

    def AddChild(self, child: "GameObject") -> "GameObject":
        if child.Parent is not None:
            child.Parent.RemoveChild(child)
        
        if self._awoken and not child._awoken:
            child.Awake()
        if self._started and not child._started:
            child.Start()
            
        if self.Enabled and not child.Enabled:
            child.Enable()
        if not self.Enabled and child.Enabled:
            child.Disable()
        
        child.Parent = self
        self.Children.append(child)
        return child
        
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
    
    def AddComponent(self, component: Component) -> Component:
        component.GameObject = self
        self.Components.append(component)
        self._componentLookup[type(component)].append(component)
        
        if self._awoken:
            component.Awake()
            
        if self._started:
            component.Start()
            
        if self.Enabled:
            component.OnEnable()
            
        return component
    
    def RemoveComponent(self, component: Component):
        component_type = type(component)
        
        if component in self.Components:
            self.Components.remove(component)
            
            lst = self._componentLookup.get(type(component))
            lst.remove(component)
            if not lst:
                del self._componentLookup[type(component)]
            if self.Enabled:
                component.OnDisable()
            component.GameObject = None

        
    def GetFirstComponentOfType(self, type: Type[T]) -> Optional[T]:
        lst = self._componentLookup.get(type)
        return lst[0] if lst else None
    
    def GetAllComponentsOfType(self, type: Type[T]) -> list[T]:
        return list(self._componentLookup.get(type, []))
    
# --------- Lifecycle ----------

    def Awake(self):
        if self._awoken:
            return
        self._awoken = True
        
        for component in self.Components[:]:
            component.Awake()
        
        for child in self.Children[:]:
            child.Awake()
        
            
    def Start(self):
        if self._started:
            return
        self._started = True
        
        for component in self.Components[:]:
            component.Start()
        
        for child in self.Children[:]:
            child.Start()
        
    
    def Update(self, deltaTime: float):
        if not self.Enabled:
            return
        
        for component in self.Components[:]:
            if component.Enabled:
                component.Update(deltaTime)
            
        for child in self.Children[:]:
            if child.Enabled:
                child.Update(deltaTime)
            
    def Enable(self):
        if self.Enabled:
            return
        
        self.Enabled = True
        
        for component in self.Components:
            if component.Enabled:
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
            
    def Destroy(self):
        self._destroyed = True
        for child in self.Children:
            child.Destroy()
