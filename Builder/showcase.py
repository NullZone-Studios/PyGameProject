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
        
        overlayObject = GameObject("overlayUI", "overlay")
        canvas = overlayObject.AddComponent(UI.Canvas())
        panel = UI.Element("div")
        panel.style.display = "flex"
        panel.style.flexDirection = "row"
        panel.renderer = UI.Rendering.RectangleRenderer()

        btn1 = panel.Add(UI.Element("button"))
        btn1.style.width = 120
        btn1.renderer = UI.Rendering.RectangleRenderer()

        btn2 = panel.Add(UI.Element("button"))
        btn2.style.width = 120
        btn2.renderer = UI.Rendering.RectangleRenderer()

        canvas.root.Add(panel)
        gameObjects.append(overlayObject)

