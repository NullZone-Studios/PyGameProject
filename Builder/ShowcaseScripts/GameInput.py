from GameEssentials.Input import InputLayer, InputEvent, DeviceType, ButtonState, MouseCodes
from typing import Callable
from pygame import Vector2

class GameInputLayer(InputLayer):
    def __init__(self):
        super().__init__()
        self.keyboardMapping: dict[int, dict[int, list[Callable]]] = {}
        self.mouseMapping: dict[int, dict[int, list[Callable]]] = {}
        self.mouseMoveListeners: list[Callable[[Vector2], None]] = []
        self.mouseScrollListeners: list[Callable[[Vector2], None]] = []
    
    def AddKeyEvent(self, key: int, state: int, callback: Callable):
        if not key in self.keyboardMapping:
            self.keyboardMapping[key]= {}
        if not state in self.keyboardMapping[key]:
            self.keyboardMapping[key][state] = []
        self.keyboardMapping[key][state].append(callback)
            
    def RemoveKeyEvent(self, key: int, state: int, callback: Callable):
        if key in self.keyboardMapping and state in self.keyboardMapping[key] and callback in self.keyboardMapping[key][state]:
            self.keyboardMapping[key][state].remove(callback)
    
    def AddMouseMoveEvent(self, callback: Callable[[Vector2], None]):
        self.mouseMoveListeners.append(callback)
    def RemoveMouseMoveEvent(self, callback: Callable[[Vector2], None]):
        if callback in self.mouseMoveListeners:
            self.mouseMoveListeners.remove(callback)
            
    def AddMouseScrollEvent(self, callback: Callable[[Vector2], None]):
        self.mouseScrollListeners.append(callback)
    def RemoveMouseScrollEvent(self, callback: Callable[[Vector2], None]):
        if callback in self.mouseScrollListeners:
            self.mouseScrollListeners.remove(callback)
            
    def AddMouseButtonEvent(self, button: int, state: int, callback: Callable[[Vector2], None]):
        if not button in self.mouseMapping:
            self.mouseMapping[button] = {}
        if not state in self.mouseMapping[button]:
            self.mouseMapping[button][state] = []
        self.mouseMapping[button][state].append(callback)
    def RemoveMouseButtonEvent(self, button: int, state: int, callback: Callable[[Vector2], None]):
        if button in self.mouseMapping and state in self.mouseMapping[button] and callback in self.mouseMapping[button][state]:
            self.mouseMapping[button][state].remove(callback)
    
    def DispatchEvent(self, event: InputEvent):
        if event.device not in (DeviceType.KEYBOARD, DeviceType.MOUSE):
            return
        
        if event.device == DeviceType.KEYBOARD:
            if event.code in self.keyboardMapping and event.state in self.keyboardMapping[event.code]:
                for callback in self.keyboardMapping[event.code][event.state]:
                    callback()
                event.consumed = len(self.keyboardMapping[event.code][event.state]) > 0
                
        if event.device == DeviceType.MOUSE:
            if event.code in self.mouseMapping and event.state in self.mouseMapping[event.code]:
                for callback in self.keyboardMapping[event.code][event.state]:
                    callback(Vector2(event.position))
                event.consumed = len(self.keyboardMapping[event.code][event.state]) > 0
                
            if event.code == MouseCodes.MOVE:
                for callback in self.mouseMoveListeners:
                    callback(Vector2(event.position))
                event.consumed = len(self.mouseMoveListeners) > 0
            
            if event.code == MouseCodes.SCROLL:
                for callback in self.mouseScrollListeners:
                    callback(Vector2(event.delta))
                event.consumed = len(self.mouseScrollListeners) > 0
                
class MouseKeys:
    LEFT = 1,
    RIGHT = 2,
    MIDDLE = 3