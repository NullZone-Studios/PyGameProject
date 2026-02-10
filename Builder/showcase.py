from GameEssentials import GameObject, InputSystem, ButtonStateBind, SoundEngine
from Components import (
    Transform,
    Camera,
    DirectionalLight,
    PointLight,
    AudioSource,
    AudioListener,
    PolygonRenderer,
    SpriteRenderer
)
import Components.UI as UI
from Builder import GameBuilder
import pygame
import numpy as np
from Builder.ShowcaseScripts import Rotator, Move, Cat

class Showcase(GameBuilder):
    BACKGROUND_COLOR = pygame.Color(100,100,100)
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
        cameraObject.AddComponent(Camera(Showcase.RESOLUTION.x, Showcase.RESOLUTION.y))
        cameraObject.AddComponent(AudioListener())
        gameObjects.append(cameraObject)

        # ---------- LIGHT ----------
        lightObject = GameObject("Sun", "Light")
        lightObject.AddComponent(
            DirectionalLight(color= pygame.Color(255,100,100), intensity=1.0)
        )
        gameObjects.append(lightObject)

        # ---------- CUBE ROOT ----------
        cube = GameObject("Cube", "Geometry")
        cube.Transform.Position = pygame.Vector3(5,0,-5)
        cube.AddComponent(Rotator())
        gameObjects.append(cube)

        # shorthand
        c = pygame.Color(1, 255, 255)
        s = 1.0  # half-size

        # ---------- FRONT ----------
        front = GameObject("Front", "Face", cube)
        front.AddComponent(PolygonRenderer(
            vertices=[
                np.array([-s, -s,  s]),
                np.array([ s, -s,  s]),
                np.array([ s,  s,  s]),
                np.array([-s,  s,  s]),
            ],
            color=c
        ))

        # ---------- BACK ----------
        back = GameObject("Back", "Face", cube)
        back.AddComponent(PolygonRenderer(
            vertices=[
                np.array([ s, -s, -s]),
                np.array([-s, -s, -s]),
                np.array([-s,  s, -s]),
                np.array([ s,  s, -s]),
            ],
            color=c
        ))

        # ---------- LEFT ----------
        left = GameObject("Left", "Face", cube)
        left.AddComponent(PolygonRenderer(
            vertices=[
                np.array([-s, -s, -s]),
                np.array([-s, -s,  s]),
                np.array([-s,  s,  s]),
                np.array([-s,  s, -s]),
            ],
            color=c
        ))

        # ---------- RIGHT ----------
        right = GameObject("Right", "Face", cube)
        right.AddComponent(PolygonRenderer(
            vertices=[
                np.array([ s, -s,  s]),
                np.array([ s, -s, -s]),
                np.array([ s,  s, -s]),
                np.array([ s,  s,  s]),
            ],
            color=c
        ))

        # ---------- TOP ----------
        top = GameObject("Top", "Face", cube)
        top.AddComponent(PolygonRenderer(
            vertices=[
                np.array([-s,  s,  s]),
                np.array([ s,  s,  s]),
                np.array([ s,  s, -s]),
                np.array([-s,  s, -s]),
            ],
            color=c
        ))

        # ---------- BOTTOM ----------
        bottom = GameObject("Bottom", "Face", cube)
        bottom.AddComponent(PolygonRenderer(
            vertices=[
                np.array([-s, -s, -s]),
                np.array([ s, -s, -s]),
                np.array([ s, -s,  s]),
                np.array([-s, -s,  s]),
            ],
            color=c
        ))
        
        spriteObject = GameObject("Sprite1", "Sprite")
        spriteObject.Transform.Translate(-5,0,-5)
        spriteObject.Transform.SetScale(pygame.Vector3(50,50,50))
        spriteObject.AddComponent(AudioSource("meow", "src/sound/purr.wav"))
        spriteObject.AddComponent(Cat())
        spriteObject.AddComponent(SpriteRenderer("src/images/weird_cat.png"))
        gameObjects.append(spriteObject)
        
        overlayObject = GameObject("overlay", "overlay")
        gameObjects.append(overlayObject)
        
        canvas: UI.Canvas = overlayObject.AddComponent(UI.Canvas(self.RESOLUTION.x, self.RESOLUTION.y, color=pygame.Color(0,255,0,100)))
        panel = UI.Element("panel")
        panel.style = UI.Style(
            display="flex",
            flexDirection="row",
            gap=8,
            background=pygame.Color("gray")
        )
        
        content = UI.Element("content")
        content1 = UI.Element("content")
        content.style = UI.Style(
            width=200,
            height=50,
            background=pygame.Color("white"),
            borderColor=pygame.Color("black"),
            borderWidth=5,
            borderRadius=10
        )
        content1.style = UI.Style(
            left=200,
            width=200,
            height=50,
            background=pygame.Color("white"),
            borderColor=pygame.Color("black"),
            borderWidth=5,
            borderRadius=10
        )

        
        badge = UI.Element("badge")
        badge.style = UI.Style(
            position="absolute",
            right=4,
            top=4,
            width=16,
            height=16,
            background=pygame.Color("red")
        )
        
        canvas.root.AddChild(panel)
        panel.AddChild(badge)
        panel.AddChild(content)
        panel.AddChild(content1)
        

