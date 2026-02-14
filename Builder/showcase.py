from GameEssentials import GameObject, Input, SoundEngine
from Components import (
    Transform,
    Camera,
    DirectionalLight,
    PointLight,
    AudioSource,
    AudioListener,
    PolygonRenderer,
    SpriteRenderer,
    Face,
    DebugColliderRenderer,
    ShapeRenderer
)
import Components.UI as UI
from Builder import GameBuilder
import pygame
import numpy as np
from Builder.ShowcaseScripts import Rotator, Move, Cat, CrystalTurret, CollisionLogger, GameInputLayer, PositionToLabel

class Showcase(GameBuilder):
    BACKGROUND_COLOR = pygame.Color("blue")
    TITLE = "Showcase "
    RESOLUTION = pygame.Vector2(1280, 720)
    MOUSE_SENSITIVITY = .5
    
    def ToggleMouse(self):
        pygame.mouse.set_pos((self.RESOLUTION.x/2, self.RESOLUTION.y/2))
        pygame.mouse.set_relative_mode(not pygame.mouse.get_relative_mode())
    
    def Build(self, engine):
        gameObjects = engine.world.GameObjects
        InputHandler = GameInputLayer()
        engine.input.AddLayer(InputHandler)
        
        # --- Basic Controlls ---
        InputHandler.AddKeyEvent(pygame.K_ESCAPE, Input.ButtonState.PRESSED, self.ToggleMouse)
        
        # ---------- CAMERA ----------
        cameraObject = GameObject("MainCamera", "Camera")
        cameraObject.AddComponent(CollisionLogger(pygame.Vector3(1.5, 1.5, 1.5), "Camera"))
        cameraObject.AddComponent(DebugColliderRenderer())
        cameraObject.AddComponent(Move(InputHandler))
        cameraObject.AddComponent(Camera(Showcase.RESOLUTION.x, Showcase.RESOLUTION.y))
        cameraObject.AddComponent(AudioListener())
        cameraObject.AddComponent(PointLight(pygame.Color("green"), 1))
        gameObjects.append(cameraObject)

        # ---------- LIGHT ----------
        lightObject = GameObject("Sun", "Light")
        lightObject.AddComponent(
            DirectionalLight(color= pygame.Color(255,255,255), intensity=.8)
        )
        gameObjects.append(lightObject)

        # ---------- CUBE ----------
        # cube = GameObject("Cube", "Geometry")
        # cube.Transform.Position = pygame.Vector3(5,0,-5)
        # cube.AddComponent(Rotator())
        # cube.AddComponent(CollisionLogger(pygame.Vector3(2, 2, 2), "Cube"))
        # cube.AddComponent(DebugColliderRenderer())
        # cube.AddComponent(ShapeRenderer("cube", pygame.Color(255,0,0), (1,1,2), (3,0,0)))
        # cube.AddComponent(ShapeRenderer("cube", pygame.Color(255,0,0), (1,1,2), (-3,0,0)))
        # gameObjects.append(cube)

        # ---------- CRYSTAL TURRET1 ----------
        crystalTurret1 = GameObject("Crystal", "Geometry")
        crystalTurret1.Transform.Position = pygame.Vector3(-20, 0, 20)
        crystalTurret1.AddComponent(CrystalTurret(fire_interval=2.5))
        crystalTurret1.AddComponent(CollisionLogger(pygame.Vector3(1, 1, 1), "Crystal"))
        crystalTurret1.AddComponent(DebugColliderRenderer())
        crystalTurret1.AddComponent(Rotator())
        crystalTurret1.AddComponent(ShapeRenderer(shape="crystal", color=pygame.Color(200, 255, 255)))
        gameObjects.append(crystalTurret1)

        # ---------- CRYSTAL TURRET2 ----------
        crystalTurret2 = GameObject("Crystal", "Geometry")
        crystalTurret2.Transform.Position = pygame.Vector3(-20, 0, -20)
        crystalTurret2.AddComponent(CrystalTurret(fire_interval=2.5))
        crystalTurret2.AddComponent(CollisionLogger(pygame.Vector3(1, 1, 1), "Crystal"))
        crystalTurret2.AddComponent(DebugColliderRenderer())
        crystalTurret2.AddComponent(Rotator())
        crystalTurret2.AddComponent(ShapeRenderer(shape="crystal", color=pygame.Color(200, 255, 255)))
        gameObjects.append(crystalTurret2)

        # ---------- CRYSTAL TURRET3 ----------
        crystalTurret3 = GameObject("Crystal", "Geometry")
        crystalTurret3.Transform.Position = pygame.Vector3(20, 0, -20)
        crystalTurret3.AddComponent(CrystalTurret(fire_interval=2.5))
        crystalTurret3.AddComponent(CollisionLogger(pygame.Vector3(1, 1, 1), "Crystal"))
        crystalTurret3.AddComponent(DebugColliderRenderer())
        crystalTurret3.AddComponent(Rotator())
        crystalTurret3.AddComponent(ShapeRenderer(shape="crystal", color=pygame.Color(200, 255, 255)))
        gameObjects.append(crystalTurret3)

        # ---------- CRYSTAL TURRET4 ----------
        crystalTurret4 = GameObject("Crystal", "Geometry")
        crystalTurret4.Transform.Position = pygame.Vector3(20, 0, 20)
        crystalTurret4.AddComponent(CrystalTurret(fire_interval=2.5))
        crystalTurret4.AddComponent(CollisionLogger(pygame.Vector3(1, 1, 1), "Crystal"))
        crystalTurret4.AddComponent(DebugColliderRenderer())
        crystalTurret4.AddComponent(Rotator())
        crystalTurret4.AddComponent(ShapeRenderer(shape="crystal", color=pygame.Color(200, 255, 255)))
        gameObjects.append(crystalTurret4)
        
        # ---------- GROUND ----------
        groundObject = GameObject("Ground", "Face")
        groundObject.Transform.Translate(y=-10)
        face = groundObject.AddComponent(Face(100,100))
        groundLightObject = GameObject("GroundLight", "Light")
        groundLightObject.Transform.Translate(y=2)
        groundLightObject.AddComponent(PointLight(intensity=.8))
        groundObject.AddChild(groundLightObject)
        gameObjects.append(groundObject)
        
        # ---------- SKYBOX ----------
        skyObject = GameObject("Sky", "Face")
        skyObject.Transform.Translate(y=50)
        skyObject.Transform.Rotate(pitch=np.pi)
        face = skyObject.AddComponent(Face(1000,1000, pygame.Color(200,200,255)))
        gameObjects.append(skyObject)
        
        skyLightObject = GameObject("skyLight", "Light", skyObject)
        skyLightObject.Transform.Translate(y=2)
        skyLightObject.Transform.Rotate(pitch=-np.pi/2)
        skyLightObject.AddComponent(PointLight(intensity=.8))
        
        # ---------- MEOW :D ----------
        # spriteObject = GameObject("Sprite1", "Sprite")
        # spriteObject.Transform.Translate(-5,0,-5)
        # spriteObject.Transform.SetScale(pygame.Vector3(50,50,50))
        # spriteObject.AddComponent(AudioSource("meow", "src/sound/purr.wav"))
        # spriteObject.AddComponent(Cat())
        # spriteObject.AddComponent(CollisionLogger(pygame.Vector3(0.05, 0.05, 0.05), "CatSprite"))
        # spriteObject.AddComponent(DebugColliderRenderer())
        # spriteObject.AddComponent(SpriteRenderer("src/images/weird_cat.png"))
        # gameObjects.append(spriteObject)
        
        uiObject = GameObject("UI", "Overlay")
        canvas: UI.Canvas = uiObject.AddComponent(UI.Canvas(self.RESOLUTION.x, self.RESOLUTION.y, inputSystem=engine.input))
        positionLabel = canvas.root.AddChild(UI.Label("positionLabel", "position"))
        positionLabel.style = UI.Style(
            font=pygame.font.SysFont("arial", 32),
            padding=5
        )
        gameObjects.append(uiObject)
        
        
        cameraObject.AddComponent(PositionToLabel(positionLabel))
