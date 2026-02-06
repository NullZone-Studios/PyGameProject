import pygame
import numpy
from Components import Camera, SpriteRenderer, Light
from GameEssentials import GameObject, InputSystem, ButtonStateBind
from typing import Optional
from GameWorld import GameWorld

# pygame setup
class Engine:
    def Run(game):
        pygame.init()
        screen = pygame.display.set_mode(game.RESOLUTION)
        pygame.display.set_icon(game.ICON)
        pygame.display.set_caption(game.TITLE)
        clock = pygame.time.Clock()
        running = True
        
        renderQueue = []

        def Update(deltaTime: float):
            for obj in GameWorld.GameObjects[:]:
                obj.Update(deltaTime)
                if obj._destroyed:
                    GameWorld.GameObjects.remove(obj)

        def BuildRenderQueue(camera: Camera):
            queue = []

            lights = []
            def CollectLights(obj: GameObject):
                for compenent in obj.Components:
                    if isinstance(compenent, Light):
                        lights.append(compenent)
                for child in obj.Children:
                    CollectLights(child)
            for obj in GameWorld.GameObjects:
                CollectLights(obj)

            def AddObjectToQueue(obj: GameObject):
                for component in obj.Components:
                    if hasattr(component, "GetRenderData"):
                        data = component.GetRenderData(camera, lights)
                        if isinstance(data, list):
                            queue.extend(data)
                        elif data:
                            queue.append(data)

                for child in obj.Children:
                    AddObjectToQueue(child)
            for obj in GameWorld.GameObjects:
                AddObjectToQueue(obj)

            return queue

        def RenderQueue(screen: pygame.Surface, camera: Camera, queue):
            sw, sh = camera.ScreenWidth, camera.ScreenHeight
            for item in queue:
                if item["type"] == "sprite":
                    ndc = item["ndc"]
                    surface: pygame.Surface = item["surface"]
                    color: pygame.Color = item["color"]
                    depth = item["depth"]

                    # Skip if behind camera
                    if depth <= camera.Near:
                        continue
                    
                    # Skip if outside NDC
                    if not (-1 <= ndc[0] <= 1 and -1 <= ndc[1] <= 1):
                        continue

                    # --- NDC → screen coordinates ---
                    x = (ndc[0] * 0.5 + 0.5) * sw
                    y = (1 - (ndc[1] * 0.5 + 0.5)) * sh

                    # --- Perspective scale (like polygons) ---
                    scale = camera.FocalLength / depth
                    w = item["width"]
                    h = item["height"]

                    # --- Apply lighting tint ---
                    tinted = surface.copy()
                    tinted.fill(color, special_flags=pygame.BLEND_RGBA_MULT)

                    # --- Scale the sprite with perspective ---
                    scaled = pygame.transform.scale(tinted, (w, h))

                    # --- Center on screen coordinates ---
                    screen.blit(scaled, (x - w // 2, y - h // 2))
                elif item["type"] == "triangle":
                    if item["filled"]:
                        pygame.draw.polygon(screen, item["color"], item["points"])
                    else:
                        pygame.draw.polygon(screen, item["color"], item["points"], 1)

        game.Build(GameWorld.GameObjects)
        for obj in GameWorld.GameObjects:
            obj.Awake()
            obj.Start()

        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            InputSystem.GetInstance().Update()

            # UPDATE GAME
            Update(clock.get_time() / 1000.0)

            if not GameWorld.MainCamera:
                GameWorld.FindMainCamera()

            # fill the screen with a color to wipe away anything from last frame
            screen.fill(game.BACKGROUND_COLOR)

            # RENDER YOUR GAME HERE
            if GameWorld.MainCamera:
                renderQueue = BuildRenderQueue(GameWorld.MainCamera)
                renderQueue.sort(key=lambda r: r["depth"], reverse=True)
                RenderQueue(screen, GameWorld.MainCamera, renderQueue)

            # flip() the display to put your work on screen
            pygame.display.flip()

            clock.tick(60)  # limits FPS to 60

        pygame.quit()