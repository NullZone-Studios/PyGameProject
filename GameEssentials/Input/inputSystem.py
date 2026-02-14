from .inputLayer import InputLayer, InputEvent
import pygame
from typing import Optional
from .buttonState import ButtonState
from .deviceType import DeviceType
from .mouseCodes import MouseCodes

class InputSystem:
    def __init__(self):
        self.layers: list[InputLayer] = []
        self.lastKeys = set()
        self.lastMouse = set()
        self.lastMousePosition: Optional[pygame.Vector2] = None
        self.mouseWheel: pygame.Vector2 = pygame.Vector2(0,0)
        
    def AddLayer(self, layer: InputLayer):
        self.layers.append(layer)
        self.layers.sort(key=lambda l:l.priority)
        
    def RemoveLayer(self, layer: InputLayer):
        self.layers.remove(layer)
        
    def Update(self):
        pygame.event.pump()
        self.processKeyboard()
        self.processMouse()
        
    def processKeyboard(self):
        keys = pygame.key.get_pressed()
        current = {k for k in range(len(keys)) if keys[k]}
        self.emitTransitions(DeviceType.KEYBOARD, current, self.lastKeys)
        self.lastKeys = current
    
    def processMouse(self):
        mouseButtons = pygame.mouse.get_pressed()
        current = {i+1 for i in range(len(mouseButtons)) if mouseButtons[i]}
        position = pygame.mouse.get_pos()
        delta = pygame.Vector2(position) - self.lastMousePosition if self.lastMousePosition else pygame.Vector2(0,0)
        self.lastMousePosition = position
        wheelDelta = pygame.Vector2(0,0)
        
        for event in pygame.event.get([pygame.MOUSEWHEEL]):
            wheelDelta += pygame.Vector2(event.x, event.y)
        
        self.mouseWheel = wheelDelta
        
        self.emitTransitions(DeviceType.MOUSE, current, self.lastMouse, position, delta, wheelDelta)
        self.lastMouse = current
        
    def emitTransitions(self, device, current, last, position: Optional[pygame.Vector2] = None, delta: Optional[pygame.Vector2] = None, wheelDelta: Optional[pygame.Vector2] = None):
        allKeys = current | last
        
        for key in allKeys:
            if key in current and key not in last:
                state = ButtonState.PRESSED
            elif key in current and key in last:
                state = ButtonState.HELD
            elif key not in current and key in last:
                state = ButtonState.RELEASED
            else:
                continue
            
            event = InputEvent(
                device=device,
                code=key,
                state=state,
                position=position,
                delta=delta
            )
            self.dispatch(event)
        
        if delta and delta.length_squared() > 0:
            moveEvent = InputEvent(
                device=device,
                code=MouseCodes.MOVE,
                state=None,
                position=position,
                delta=delta
            )
            self.dispatch(moveEvent)
            
        if wheelDelta and wheelDelta.length_squared() > 0:
            wheelEvent = InputEvent(
                device=device,
                code=MouseCodes.SCROLL,
                state=None,
                delta=wheelDelta
            )
            self.dispatch(wheelEvent)
        
            
    def dispatch(self, event: InputEvent):
        for layer in self.layers:
            layer.DispatchEvent(event)
            
            if event.consumed:
                break