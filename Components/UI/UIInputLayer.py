from __future__ import annotations
from GameEssentials.Input import InputLayer, InputEvent, DeviceType, ButtonState, MouseCodes
from .UIEvent import Event, EventType
from .UIElement import Element
from pygame import Vector2, mouse, cursors
import pygame
from typing import Optional

class UILayer(InputLayer):
    def __init__(self, canvas: "Canvas"):
        self.canvas = canvas
        self.lastMousePosition: Optional[Vector2] = None
        self.hovered: Optional[Element] = None
        self.active: Optional[Element] = None
        self.focused: Optional[Element] = None
        self.pressed: bool = False
        
    def DispatchEvent(self, event: InputEvent):
        if event.device != DeviceType.MOUSE:
            return
        
        position = Vector2(event.position) if event.position else None
        root = self.canvas.root
        
        if event.code == MouseCodes.MOVE and position:
            self.handleMouseMove(event, position, root)
            return
        
        if event.code == MouseCodes.SCROLL:
            self.handleScroll(event, position)
            return
        
        if position and event.state is not None:
            self.handleButton(event, position)
            
    def handleMouseMove(self, event: InputEvent, position: Vector2, root: Element):
        newHover = root.HitTest(position)
        
        self.updateHover(event, position, newHover)
        self.handleDrag(event, position)
        self.lastMousePosition = position
        
    def updateHover(self, event: InputEvent, position: Vector2, newHover: Optional[Element]):
        if newHover == self.hovered:
            return
        
        if self.hovered:
            self.dispatch(self.hovered, EventType.MOUSE_LEAVE, event, position=position)
            
        if newHover:
            self.dispatch(newHover, EventType.MOUSE_ENTER, event, position=position)
            
        self.hovered = newHover
        self.updateCursor()
    
    def updateCursor(self):
        element: Optional[Element] = self.hovered
        while element:
            if element.cursor:
                mouse.set_cursor(element.cursor)
                return
            element = element.parent
        
        mouse.set_cursor(cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
        
    def handleDrag(self, event: InputEvent, position: Vector2):
        if not self.pressed or not self.active or not self.lastMousePosition:
            return
        
        delta: Vector2 = position - self.lastMousePosition
        if delta.length_squared() == 0:
            return
        
        self.dispatch(self.active, EventType.MOUSE_DRAG, event, position=position, delta=delta)
        
    def handleScroll(self, event: InputEvent, position: Optional[Vector2]):
        position = position or Vector2(0,0)
        if not self.hovered:
            return
        
        self.dispatch(self.hovered, EventType.MOUSE_SCROLL, event, position=position, delta=event.delta)
        
    def handleButton(self, event: InputEvent, position: Vector2):
        if event.state == ButtonState.PRESSED:
            self.handleMouseDown(event, position)
        elif event.state == ButtonState.RELEASED:
            self.handleMouseUp(event, position)
            
    def handleMouseDown(self, event: InputEvent, position: Vector2):
        if not self.hovered:
            return
        self.active = self.hovered
        self.pressed = True
        
        self.dispatch(self.active, EventType.MOUSE_DOWN, event, position=position)
        
    def handleMouseUp(self, event: InputEvent, position: Vector2):
        if not self.active:
            self.pressed = False
            return
        
        if self.focused and self.focused != self.active:
            self.dispatch(self.focused, EventType.BLUR, event)
            
        self.focused = self.active
        self.dispatch(self.active, EventType.FOCUS, event)
        
        self.dispatch(self.active, EventType.MOUSE_UP, event, position=position)
        
        if self.active == self.hovered:
            self.dispatch(self.active, EventType.MOUSE_CLICK, event, position=position)
            
        self.active = None
        self.pressed = False
        
    def dispatch(self, target: Element, eventType: str, inputEvent: InputEvent, **kwargs):
        e = Event(eventType, **kwargs)
        target.DispatchEvent(e)
        inputEvent.consumed |= e.stopped
                
            