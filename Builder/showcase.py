from GameEssentials import GameObject, Input, SoundEngine
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
    
    def ToggleMouse(self):
        pygame.mouse.set_pos((self.RESOLUTION.x/2, self.RESOLUTION.y/2))
        pygame.mouse.set_relative_mode(not pygame.mouse.get_relative_mode())
    
    def Build(self, engine):
        gameObjects = engine.world.GameObjects
        
        # ---------- CAMERA ----------
        cameraObject = GameObject("MainCamera", "Camera")
        #cameraObject.AddComponent(Move())
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
        spriteObject.AddComponent(Cat(cameraObject))
        spriteObject.AddComponent(SpriteRenderer("src/images/weird_cat.png"))
        gameObjects.append(spriteObject)
        
        overlayObject = GameObject("overlay", "overlay")
        gameObjects.append(overlayObject)
        
        canvas: UI.Canvas = overlayObject.AddComponent(UI.Canvas(self.RESOLUTION.x, self.RESOLUTION.y, inputSystem=engine.input))
        panel = canvas.root.AddChild(UI.Element("panel"))
        panel.style = UI.Style(
            display="flex",
            flexDirection="row",
            gap=8,
            background=pygame.Color(0,0,0,0),
            font=pygame.font.SysFont("sans-serif", 32)
        )
        
        content = panel.AddChild(UI.Element("content"))
        content1 = panel.AddChild(UI.Element("content"))
        content2 = panel.AddChild(UI.Button("BIG BUTTON"))
        content2.AddEventListener("OnClick", lambda event: print(f"BIG BUTTON HAS BEEN CLICKED!"))
        content.style = UI.Style(
            width=200,
            height=50,
            overflow="hidden",
            background=pygame.Color("white"),
            borderColor=pygame.Color("black"),
            borderWidth=5,
            borderRadius=100,
            hover=UI.Style(background=pygame.Color("black"), color=pygame.Color("white"))
        )
        content1.style = content.style
        content2.style = content.style
        
        badge = panel.AddChild(UI.Element("badge"))
        badge.style = UI.Style(
            position="absolute",
            left=4,
            bottom=4,
            width=30,
            height=30,
            background=pygame.Color("red")
        )
        

