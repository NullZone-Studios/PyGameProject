from Components import Transform, Script
from GameEssentials import InputSystem, ButtonStateBind
import pygame
import numpy as np

class Move(Script):
    MOUSE_SENSITIVITY = .33
    
    def __init__(self):
        super().__init__()
        pygame.mouse.set_relative_mode(True)
        self.screen: pygame.Surface = pygame.display.get_surface()
        self.movementDirection: pygame.Vector3 = pygame.Vector3(0,0,0)
        self.speed = 20
        
    def Update(self, deltaTime: float):
        transform: Transform = self.GameObject.Transform
        localDirection = np.array([self.movementDirection.x, self.movementDirection.y, self.movementDirection.z])
        worldDirection = transform.ComputeRotationMatrix() @ localDirection
        
        transform.Translate(
            worldDirection[0] * deltaTime,
            worldDirection[1] * deltaTime,
            worldDirection[2] * deltaTime
        )
        
        if pygame.mouse.get_relative_mode():
            position = pygame.mouse.get_pos()
            screenWidht, screenHeight = self.screen.get_size()
            offset = pygame.Vector2(screenWidht/2, screenHeight/2) - position
            if offset.magnitude() > 0:
                offset.normalize()
            
            pitch = offset.y * deltaTime * Move.MOUSE_SENSITIVITY
            yaw = offset.x * deltaTime * Move.MOUSE_SENSITIVITY
                
            transform.Rotate(
                pitch=pitch,
                yaw= -yaw if transform.Rotation.x > np.pi/2 and transform.Rotation.x < np.pi * 1.5 else yaw 
            )
            pygame.mouse.set_pos(screenWidht/2, screenHeight/2)
        
        
    
    def Start(self):
        pygame.mouse.set_relative_mode(True)
        
        InputSystem.GetInstance().KeyBindings[pygame.K_w] = ButtonStateBind(
            pressed= lambda _: self.addZ(-self.speed),
            held= None,
            released= lambda _: self.addZ(self.speed)
        )
        InputSystem.GetInstance().KeyBindings[pygame.K_a] = ButtonStateBind(
            pressed= lambda _: self.addX(-self.speed),
            held= None,
            released= lambda _: self.addX(self.speed)
        )
        InputSystem.GetInstance().KeyBindings[pygame.K_s] = ButtonStateBind(
            pressed= lambda _: self.addZ(self.speed),
            held= None,
            released= lambda _: self.addZ(-self.speed)
        )
        InputSystem.GetInstance().KeyBindings[pygame.K_d] = ButtonStateBind(
            pressed= lambda _: self.addX(self.speed),
            held= None,
            released= lambda _: self.addX(-self.speed)
        )
        InputSystem.GetInstance().KeyBindings[pygame.K_SPACE] = ButtonStateBind(
            pressed= lambda _: self.addY(self.speed),
            held= None,
            released= lambda _: self.addY(-self.speed)
        )
        InputSystem.GetInstance().KeyBindings[pygame.K_c] = ButtonStateBind(
            pressed= lambda _: self.addY(-self.speed),
            held= None,
            released= lambda _: self.addY(self.speed)
        )
        
    def addZ(self, value: float):
        self.movementDirection.z += value
    def addX(self, value:float):
        self.movementDirection.x += value
    def addY(self, value:float):
        self.movementDirection.y += value
