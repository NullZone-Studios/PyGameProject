import numpy
import pygame
from Builder import GameBuilder
from Components import (
    ShapeRenderer,
    AudioSource,
    AudioListener,
    MusicSource,
    Face,
    UI
)
from GameEssentials import (
    GameObject,
    Input,
    GameWorld,
    SoundEngine
)
from .DemoScripts import (
    Move, 
    Rotator
)
from .DemoObjects import (
    Player,
    Camera,
    Light,
    Ground,
    RotatingCube,
    NamePlate
)

class Demo(GameBuilder):
    TITLE = "Demo"
    
    def ToggleMouse(self):
        pygame.mouse.set_pos((self.RESOLUTION.x/2, self.RESOLUTION.y/2))
        pygame.mouse.set_relative_mode(not pygame.mouse.get_relative_mode())
    
    def Build(self, engine):
        World: GameWorld = engine.world
        InputHandler = Input.GameInput()
        engine.input.AddLayer(InputHandler)
        
        # --- Add mouse toggle handling ---
        InputHandler.AddKeyEvent(pygame.K_ESCAPE, Input.ButtonState.PRESSED, self.ToggleMouse)
        
        # --- Create Objects ---
        playerObject = Player(inputHandler= InputHandler)
        cameraObject = Camera(resolution= Demo.RESOLUTION, parent= playerObject)
        
        rotatingCube = RotatingCube(color= pygame.Color("orange"))
        rotatingCubeName = NamePlate(parent= rotatingCube, text= "Rotating\nCube")
        orbitingCube = RotatingCube(color= pygame.Color("yellow"), parent= rotatingCube)
        
        
        lightObject = Light(color= pygame.Color("white"), intensity=.7, range=1000)
        orbLightObject = Light(color= pygame.Color(200,200,200), intensity=.7, range=1000, parent=orbitingCube)
        
        rotatingCube.Transform.Translate(y=-5)
        orbitingCube.Transform.Translate(x=50)
        rotatingCubeName.Transform.Translate(y=2)
        
        # --- Ground Face ---
        groundObject = Ground(panelsDeep=7, panelsWide=7, panelSize=10)
        groundObject.Transform.Translate(y=-10)
        
        
        # --- Instantiate Objects
        World.Instantiate(groundObject)
        World.Instantiate(rotatingCube)
        World.Instantiate(lightObject)
        # World.Instantiate(cameraObject)
        World.Instantiate(playerObject)
        
        