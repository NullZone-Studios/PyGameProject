import pygame
from typing import Callable, Optional

class ButtonStateBind:
    def __init__(self, pressed: Optional[Callable] = None, held: Optional[Callable] = None, released: Optional[Callable] = None):
        self.State: int = ButtonState.RELEASED
        self.Held: Optional[Callable] = held
        self.Pressed: Optional[Callable] = pressed
        self.Released: Optional[Callable] = released
        
class ButtonState:
    PRESSED = 1
    HELD = 2
    RELEASED = 3

class InputSystem:
    instance = None
    
    @staticmethod
    def GetInstance():
        if InputSystem.instance is None:
            InputSystem()
        return InputSystem.instance
    
    def __init__(self):
        if InputSystem.instance is not None:
            raise Exception("InputSystem is a singleton! Use InputSystem.GetInstance()")
        InputSystem.instance = self
        
        self.KeyBindings: dict[int, ButtonStateBind] = {}
        self.lastKeys: set[int] = set()
        
        self.MouseBindings: dict[int, ButtonStateBind] = {}
        self.lastMouse: set[int] = set()
        
        self.JoyBindings: dict[tuple[int,int], ButtonStateBind] = {}
        self.lastJoy: set[tuple[int,int]] = set()
        
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        
    def Update(self):
        pygame.event.pump()
        
        keys = pygame.key.get_pressed()
        keysDown = set(key for key in range(len(keys)) if keys[key])
        self.processBindings(keysDown, self.lastKeys, self.KeyBindings)
        self.lastKeys = keysDown
        
        mouseButtons = pygame.mouse.get_pressed()
        mouseDown = {i+1 for i, pressed in enumerate(mouseButtons) if pressed}
        mousePosition = pygame.mouse.get_pos()
        self.processBindings(mouseDown, self.lastMouse,self.MouseBindings, extra=mousePosition)
        self.lastMouse = mouseDown
        
        joyDown = set()
        joyAxis = {}
        for joyID, joy in enumerate(self.joysticks):
            for button in range(joy.get_numbuttons()):
                if joy.get_button(button):
                    joyDown.add((joyID, button))
            joyAxis[joyID] = [joy.get_axis(a) for a in range(joy.get_numaxes())]
        self.processBindings(joyDown, self.lastJoy, self.JoyBindings, extra=joyAxis)
        self.lastJoy = joyDown
        
        
    def processBindings(self, current: set, last: set, bindings: dict, extra=None):
        for key, binding in bindings.items():
            if key in current:
                if key not in last:
                    binding.State = ButtonState.PRESSED
                    if binding.Pressed:
                        binding.Pressed(extra)
                else:
                    binding.State = ButtonState.HELD
                    if binding.Held:
                        binding.Held(extra)
            else:
                if key in last:
                    binding.State = ButtonState.RELEASED
                    if binding.Released:
                        binding.Released(extra)
                else:
                    binding.State = ButtonState.RELEASED