from Components import Transform, Script
from GameEssentials.Input.gameInput import GameInput, ButtonState
import pygame
import numpy as np

class Move(Script):
    MOUSE_SENSITIVITY = .20
    
    def __init__(self, inputLayer: GameInput):
        super().__init__()
        pygame.mouse.set_relative_mode(True)
        self.screen: pygame.Surface = pygame.display.get_surface()
        self.movementDirection: pygame.Vector3 = pygame.Vector3(0,0,0)
        self.speed = 20
        self.inputLayer = inputLayer
        
        inputLayer.AddKeyEvent(pygame.K_w, ButtonState.PRESSED, lambda : self.addZ(-self.speed))
        inputLayer.AddKeyEvent(pygame.K_w, ButtonState.RELEASED, lambda : self.addZ(self.speed))
        
        inputLayer.AddKeyEvent(pygame.K_a, ButtonState.PRESSED, lambda : self.addX(-self.speed))
        inputLayer.AddKeyEvent(pygame.K_a, ButtonState.RELEASED, lambda : self.addX(self.speed))
        
        inputLayer.AddKeyEvent(pygame.K_s, ButtonState.PRESSED, lambda : self.addZ(self.speed))
        inputLayer.AddKeyEvent(pygame.K_s, ButtonState.RELEASED, lambda : self.addZ(-self.speed))
        
        inputLayer.AddKeyEvent(pygame.K_d, ButtonState.PRESSED, lambda : self.addX(self.speed))
        inputLayer.AddKeyEvent(pygame.K_d, ButtonState.RELEASED, lambda : self.addX(-self.speed))
        
        inputLayer.AddKeyEvent(pygame.K_SPACE, ButtonState.PRESSED, lambda : self.addY(self.speed))
        inputLayer.AddKeyEvent(pygame.K_SPACE, ButtonState.RELEASED, lambda : self.addY(-self.speed))
        
        inputLayer.AddKeyEvent(pygame.K_c, ButtonState.PRESSED, lambda : self.addY(-self.speed))
        inputLayer.AddKeyEvent(pygame.K_c, ButtonState.RELEASED, lambda : self.addY(self.speed))
        
        inputLayer.AddMouseMoveEvent(self.HandleMouseMove)
        
    def Update(self, deltaTime: float):
        transform: Transform = self.GameObject.Transform
        localDirection = np.array([self.movementDirection.x, self.movementDirection.y, self.movementDirection.z, 0])
        worldDirection = transform.ComputeRotationMatrix() @ localDirection
        
        transform.Translate(
            worldDirection[0] * deltaTime,
            worldDirection[1] * deltaTime,
            worldDirection[2] * deltaTime
        )
    
    def Start(self):
        pygame.mouse.set_relative_mode(True)
        
    def HandleMouseMove(self, position: pygame.Vector2):
        if pygame.mouse.get_relative_mode():
            screenWidht, screenHeight = self.screen.get_size()
            centerOfScreen = pygame.Vector2(screenWidht/2, screenHeight/2)
            offset = centerOfScreen - position
            transform = self.GameObject.Transform
            
            pitch = offset.y * Move.MOUSE_SENSITIVITY * .005
            yaw = offset.x * Move.MOUSE_SENSITIVITY * .005
                
            transform.Rotate(
                pitch=pitch,
                yaw= -yaw if transform.Rotation.x > np.pi/2 and transform.Rotation.x < np.pi * 1.5 else yaw 
            )
            pygame.mouse.set_pos(centerOfScreen.x, centerOfScreen.y)
        
    def addZ(self, value: float):
        self.movementDirection.z += value
    def addX(self, value:float):
        self.movementDirection.x += value
    def addY(self, value:float):
        self.movementDirection.y += value
