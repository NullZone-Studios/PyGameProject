from GameEssentials import GameObject, InputSystem, ButtonStateBind, SoundEngine
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
from Builder import GameBuilder
import pygame
import numpy as np
from Builder.ShowcaseScripts import Rotator, Move, Cat
from Builder.ShowcaseScripts import CollisionLogger

class Showcase(GameBuilder):
    BACKGROUND_COLOR = pygame.Color("blue")
    TITLE = "Showcase "
    RESOLUTION = pygame.Vector2(1280, 720)
    MOUSE_SENSITIVITY = .5
    
    def Build(self, gameObjects: list[GameObject]):
        InputSystem.GetInstance().KeyBindings[pygame.K_ESCAPE] = ButtonStateBind(
            pressed= lambda _: pygame.mouse.set_relative_mode(not pygame.mouse.get_relative_mode())
        )
        
        # ---------- CAMERA ----------
        cameraObject = GameObject("MainCamera", "Camera")
        cameraObject.AddComponent(Move())
        cameraObject.AddComponent(CollisionLogger(pygame.Vector3(1.5, 1.5, 1.5), "Camera"))
        cameraObject.AddComponent(DebugColliderRenderer())
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
        cube = GameObject("Cube", "Geometry")
        cube.Transform.Position = pygame.Vector3(5,0,-5)
        cube.AddComponent(Rotator())
        cube.AddComponent(CollisionLogger(pygame.Vector3(2, 2, 2), "Cube"))
        cube.AddComponent(DebugColliderRenderer())
        cube.AddComponent(ShapeRenderer("cube"))
        gameObjects.append(cube)
        
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
        spriteObject = GameObject("Sprite1", "Sprite")
        spriteObject.Transform.Translate(-5,0,-5)
        spriteObject.Transform.SetScale(pygame.Vector3(50,50,50))
        spriteObject.AddComponent(AudioSource("meow", "src/sound/purr.wav"))
        spriteObject.AddComponent(Cat())
        spriteObject.AddComponent(CollisionLogger(pygame.Vector3(0.05, 0.05, 0.05), "CatSprite"))
        spriteObject.AddComponent(DebugColliderRenderer())
        spriteObject.AddComponent(SpriteRenderer("src/images/weird_cat.png"))
        gameObjects.append(spriteObject)
