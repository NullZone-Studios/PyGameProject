from Builder.ShowcaseScripts.cameraController import CameraController
from GameEssentials import GameObject, Input, SoundEngine, GameWorld
from Components import (
    Transform,
    Camera,
    DirectionalLight,
    PointLight,
    AudioSource,
    AudioListener,
    MusicSource,
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
from Builder.ShowcaseScripts import Rotator, Move, Cat, CrystalTurret, CollisionLogger, GameInputLayer, PositionToLabel, GameMaster, Player

class Showcase(GameBuilder):
    BACKGROUND_COLOR = pygame.Color(0,0,0)
    TITLE = "Space Zap 3D"
    RESOLUTION = pygame.Vector2(1280, 720)
    MOUSE_SENSITIVITY = .5
    
    def ToggleMouse(self):
        pygame.mouse.set_pos((self.RESOLUTION.x/2, self.RESOLUTION.y/2))
        pygame.mouse.set_relative_mode(not pygame.mouse.get_relative_mode())
        crosshairObject = GameWorld.GetInstance().FindByName("crosshair")
        if crosshairObject.Enabled:
            crosshairObject.Disable()
        else:
            crosshairObject.Enable()
    
    def Build(self, engine):
        gameObjects = engine.world.GameObjects
        InputHandler = GameInputLayer()
        engine.input.AddLayer(InputHandler)
        
        # --- Basic Controlls ---
        InputHandler.AddKeyEvent(pygame.K_ESCAPE, Input.ButtonState.PRESSED, self.ToggleMouse)
        
        # ---------- PLAYER ----------
        playerObject = GameObject("Player", "Player")
        playerObject.AddComponent(CollisionLogger(pygame.Vector3(1.5, 1.5, 1.5), "Player"))
        playerObject.AddComponent(DebugColliderRenderer())
        playerObject.AddComponent(ShapeRenderer(shape="cube", color=pygame.Color("cornflowerblue"), scale=(1,1,1)))
        playerObject.AddComponent(Move(InputHandler))
        playerObject.AddComponent(AudioSource(soundName=f"player_shoot", soundPath="src/sound/shoot_sound2.wav", autoPlay=False))
        playerObject.AddComponent(Player(InputHandler))
        gameObjects.append(playerObject)
        
        # ---------- CAMERA ----------
        cameraObject = GameObject("MainCamera", "Camera")
        cameraObject.AddComponent(Camera(Showcase.RESOLUTION.x, Showcase.RESOLUTION.y))
        cameraObject.AddComponent(AudioListener())
        cameraObject.AddComponent(CameraController())
        gameObjects.append(cameraObject)
        
        
        # ---------- Game Ambience ----------
        backgroundAmbienceObject = cameraObject.AddChild(GameObject("backgroundAmbience", "Music"))
        backgroundAmbienceObject.Transform.Translate(z=-10)
        backgroundAmbienceObject.AddComponent(MusicSource("ambience", "src/sound/space_ambience_fixed.wav", autoPlay=True, loop=True))

        # ---------- LIGHT ----------
        lightObject = GameObject("Sun", "Light")
        #lightObject.AddComponent(DirectionalLight(color= pygame.Color(255,255,255), intensity=.8))
        lightObject.AddComponent(PointLight(color= pygame.Color(200,200,200), intensity=.7, range=1000))
        gameObjects.append(lightObject)

        # ---------- CRYSTAL TURRET1 ----------
        # crystalTurret1 = GameObject("Crystal", "Geometry")
        # crystalTurret1.Transform.Position = pygame.Vector3(-20, 0, 20)
        # crystalTurret1.AddComponent(CrystalTurret(fire_interval=2.5))
        # crystalTurret1.AddComponent(CollisionLogger(pygame.Vector3(1, 1, 1), "Crystal"))
        # crystalTurret1.AddComponent(DebugColliderRenderer())
        # crystalTurret1.AddComponent(Rotator())
        # crystalTurret1.AddComponent(ShapeRenderer(shape="crystal", color=pygame.Color(200, 255, 255)))
        # gameObjects.append(crystalTurret1)

        # ---------- CRYSTAL TURRET1 BASE ----------
        crystalTurret1Base = GameObject("CrystalBase", "Geometry")
        crystalTurret1Base.Transform.Position = pygame.Vector3(-20, -5, 20)
        crystalTurret1Base.AddComponent(ShapeRenderer(shape="cube", color=pygame.Color(210, 60, 60), scale=(1,3.5,1), offset=(0,-0.5,0)))
        gameObjects.append(crystalTurret1Base)
    
        # ---------- CRYSTAL TURRET2 ----------
        # crystalTurret2 = GameObject("Crystal", "Geometry")
        # crystalTurret2.Transform.Position = pygame.Vector3(-20, 0, -20)
        # crystalTurret2.AddComponent(CrystalTurret(fire_interval=2.5))
        # crystalTurret2.AddComponent(CollisionLogger(pygame.Vector3(1, 1, 1), "Crystal"))
        # crystalTurret2.AddComponent(DebugColliderRenderer())
        # crystalTurret2.AddComponent(Rotator())
        # crystalTurret2.AddComponent(ShapeRenderer(shape="crystal", color=pygame.Color(200, 255, 255)))
        # gameObjects.append(crystalTurret2)

        # ---------- CRYSTAL TURRET2 BASE ----------
        crystalTurret2Base = GameObject("CrystalBase", "Geometry")
        crystalTurret2Base.Transform.Position = pygame.Vector3(-20, -5, -20)
        crystalTurret2Base.AddComponent(ShapeRenderer(shape="cube", color=pygame.Color(210, 60, 60), scale=(1,3.5,1), offset=(0,-0.5,0)))
        gameObjects.append(crystalTurret2Base)

        # ---------- CRYSTAL TURRET3 ----------
        # crystalTurret3 = GameObject("Crystal", "Geometry")
        # crystalTurret3.Transform.Position = pygame.Vector3(20, 0, -20)
        # crystalTurret3.AddComponent(CrystalTurret(fire_interval=2.5))
        # crystalTurret3.AddComponent(CollisionLogger(pygame.Vector3(1, 1, 1), "Crystal"))
        # crystalTurret3.AddComponent(DebugColliderRenderer())
        # crystalTurret3.AddComponent(Rotator())
        # crystalTurret3.AddComponent(ShapeRenderer(shape="crystal", color=pygame.Color(200, 255, 255)))
        # gameObjects.append(crystalTurret3)

        # ---------- CRYSTAL TURRET3 BASE ----------
        crystalTurret3Base = GameObject("CrystalBase", "Geometry")
        crystalTurret3Base.Transform.Position = pygame.Vector3(20, -5, -20)
        crystalTurret3Base.AddComponent(ShapeRenderer(shape="cube", color=pygame.Color(210, 60, 60), scale=(1,3.5,1), offset=(0,-0.5,0)))
        gameObjects.append(crystalTurret3Base)

        # ---------- CRYSTAL TURRET4 ----------
        # crystalTurret4 = GameObject("Crystal", "Geometry")
        # crystalTurret4.Transform.Position = pygame.Vector3(20, 0, 20)
        # crystalTurret4.AddComponent(CrystalTurret(fire_interval=2.5))
        # crystalTurret4.AddComponent(CollisionLogger(pygame.Vector3(1, 1, 1), "Crystal"))
        # crystalTurret4.AddComponent(DebugColliderRenderer())
        # crystalTurret4.AddComponent(Rotator())
        # crystalTurret4.AddComponent(ShapeRenderer(shape="crystal", color=pygame.Color(200, 255, 255)))
        # gameObjects.append(crystalTurret4)

        # ---------- CRYSTAL TURRET4 BASE ----------
        crystalTurret4Base = GameObject("CrystalBase", "Geometry")
        crystalTurret4Base.Transform.Position = pygame.Vector3(20, -5, 20)
        crystalTurret4Base.AddComponent(ShapeRenderer(shape="cube", color=pygame.Color(210, 60, 60), scale=(1,3.5,1), offset=(0,-0.5,0)))
        gameObjects.append(crystalTurret4Base)
        
        
        #--------------GAME MASTER----------------
        gogm = GameObject("GameMaster", "Logic")
        gm = GameMaster()
        gogm.AddComponent(gm)
        gameObjects.append(gogm)
        #gm.EasyMode()
        #gm.StartGame()
        
        # ---------- UI ----------
        crossHairUI = GameObject("crosshair", "Overlay")
        canvas: UI.Canvas = crossHairUI.AddComponent(UI.Canvas(self.RESOLUTION.x, self.RESOLUTION.y, inputSystem=engine.input))
        crosshairElement = canvas.root.AddChild(UI.Element("crosshair"))
        crosshairElement.style = UI.Style(
            margin=(
                (self.RESOLUTION.y//4)-5,
                (self.RESOLUTION.x//4)-5,
                0,
                0
            ),
            width=20,
            height=20,
            borderRadius=20,
            borderWidth=2,
            borderColor=pygame.Color("white")
        )
        crosshairBeamLeft = crosshairElement.AddChild(UI.Element("beam-left"))
        crosshairBeamLeft.style = UI.Style(
            margin=(
              5,
              -50,
              0,
              0  
            ),
            width=80,
            height=2,
            background=pygame.Color("white"),
            borderRadius=20
        )
        crosshairBeamRight = crosshairElement.AddChild(UI.Element("beam-right"))
        crosshairBeamRight.style = UI.Style(
            margin=(
              1,
              19,
              0,
              0  
            ),
            width=80,
            height=2,
            background=pygame.Color("white"),
            borderRadius=20
        )
        
        gameObjects.append(crossHairUI)
        
        # ---------- START MENU UI ----------
        startMenuUI = GameObject("StartMenuUI", "Overlay")
        gameObjects.append(startMenuUI)
        startMenuCanvas = startMenuUI.AddComponent(UI.Canvas(self.RESOLUTION.x, self.RESOLUTION.y, inputSystem= engine.input))
        panel = startMenuCanvas.root.AddChild(UI.Element("panel"))
        gameTitle = panel.AddChild(UI.Label("GameTitle", self.TITLE))
        buttonContainer = panel.AddChild(UI.Element("ButtonContainer"))
        startButton: UI.Button = buttonContainer.AddChild(UI.Button("Start"))
        optionsButton: UI.Button = buttonContainer.AddChild(UI.Button("Options"))
        quitButton: UI.Button = buttonContainer.AddChild(UI.Button("Quit"))
        
        # ------ START UI STYLE ----------
        panelStyle = UI.Style(
            font=pygame.font.SysFont("arial", 28),
            height=self.RESOLUTION.y,
            color=pygame.Color("white"),
            margin=(self.RESOLUTION.y/4, 20)
        )
        
        gameTitleStyle = UI.Style(
            font=pygame.font.SysFont("arial", 48, bold=True),
            textAlign="center",
            verticalAlign="bottom",
            margin=(0,0,20,0)
        )
        
        buttonContinerStyle = UI.Style(
            display="flex",
            flexDirection="column",
            gap=10,
            padding=20,
            background=pygame.Color(200,200,200,50),
            borderRadius=10,
        )
        buttonStyle = UI.Style(
            font= pygame.font.SysFont("arial", 36, bold=True),
            width=200,
            height=50,
            borderWidth=2,
            borderColor=pygame.Color("gray"),
            background=pygame.Color("white"),
            color=pygame.Color("black"),
            borderRadius=5,
            hover=UI.Style(
                background=pygame.Color("black"),
                borderColor=pygame.Color("white"),
                color=pygame.Color("white")
            )
        )
        
        panel.style = panelStyle
        gameTitle.style = gameTitleStyle
        buttonContainer.style = buttonContinerStyle
        startButton.style = buttonStyle
        optionsButton.style = buttonStyle
        quitButton.style = buttonStyle
        
        quitButton.AddEventListener(UI.EventType.MOUSE_CLICK, lambda event: self.Quit())
        startButton.AddEventListener(UI.EventType.MOUSE_CLICK, lambda event: gm.StartGame())
        
        optionsMenuUI = GameObject("optionsUI", "Overlay")
        optionsCanvas: UI.Canvas = optionsMenuUI.AddComponent(UI.Canvas(self.RESOLUTION.x, self.RESOLUTION.y, inputSystem=engine.input))
        optionsBackButton = optionsCanvas.root.AddChild(UI.Label("backButton", "BACK"))
        optionsBackButton.style = UI.Style(
            font = pygame.font.SysFont("arial", 36, bold=True),
            margin=(20,20),
            color=pygame.Color("white"),
            hover=UI.Style(
                color=pygame.Color("yellow"),
            )
        )
        optionsBackButton.cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
        optionsMenuUI.Disable()
        gameObjects.append(optionsMenuUI)
        
        def ToggleOptionsMenu():
            if optionsMenuUI.Enabled:
                startMenuUI.Enable()
                optionsMenuUI.Disable()
            else:
                startMenuUI.Disable()
                optionsMenuUI.Enable()
        
        optionsButton.AddEventListener(UI.EventType.MOUSE_CLICK, lambda event: ToggleOptionsMenu())
        optionsBackButton.AddEventListener(UI.EventType.MOUSE_CLICK, lambda event: ToggleOptionsMenu())
        
        # ------ STAR FIELD ----------
        starBoxObject = GameObject("StarBox", "World")
        starBoxObject.Transform.SetScale(pygame.Vector3(10,10,10))
        starObject = starBoxObject.AddChild(GameObject("Star", "World"))
        starObject.AddComponent(Face(1,1, pygame.Color("white")))
        for i in range(20):
            starBoxObject.AddChild(starObject.Clone())
        for child in starBoxObject.Children:
            
            if np.random.random() > .5:
                child.Transform.Translate(x=np.random.randint(80,200))
            else:
                child.Transform.Translate(x=np.random.randint(-200,-80))
            
            if np.random.random() > .5:
                child.Transform.Translate(y=np.random.randint(80,200))
            else:
                child.Transform.Translate(y=np.random.randint(-200, 80))
            
            if np.random.random() > .5:
                child.Transform.Translate(z=np.random.randint(80,200))
            else:
                child.Transform.Translate(z=np.random.randint(-200,-80))
                
            
            child.Transform.LookAt(pygame.Vector3(0,0,0))
            child.Transform.Rotate(pitch=np.pi/2)
        gameObjects.append(starBoxObject)
        
        cameraObject.AddComponent(PositionToLabel(crosshairElement))