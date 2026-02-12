from Components import Camera, Light
from .gameObject import GameObject
import pygame

class Renderer:
    def __init__(self):
        pass
    
    def BuildRenderQueue(self, camera: Camera, gameObjects: list[GameObject]):
            queue = []

            lights = []
            def CollectLights(obj: GameObject):
                for compenent in obj.Components:
                    if isinstance(compenent, Light):
                        lights.append(compenent)
                for child in obj.Children:
                    CollectLights(child)
            for obj in gameObjects:
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
            for obj in gameObjects:
                AddObjectToQueue(obj)

            return queue
        
    def RenderQueue(self, screen: pygame.Surface, camera: Camera, queue):
            sw, sh = camera.ScreenWidth, camera.ScreenHeight
            
            worldItems = [item for item in queue if item["type"] in ["sprite", "triangle"]]
            overlayItems = [item for item in queue if item["type"] == "overlay"]
            
            # World
            worldItems.sort(key=lambda r: r["depth"], reverse=True)
            for item in worldItems:
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
            
            # UI Overlay
            overlayItems.sort(key= lambda r: r["layer"], reverse=True)
            for item in overlayItems:
                if item["surface"]:
                    screen.blit(item["surface"], (0,0))