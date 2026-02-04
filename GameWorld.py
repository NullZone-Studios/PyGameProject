import pygame
import numpy
from Components import Camera, SpriteRenderer
from GameEssentials import GameObject, InputSystem, ButtonStateBind
from typing import Optional

# pygame setup
pygame.init()
pygame
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Test Project")
clock = pygame.time.Clock()
running = True

gameObjects = list[GameObject]()
MainCamera: Optional[Camera] = None
renderQueue = []

def Update(deltaTime: float):
    for obj in gameObjects[:]:
        obj.Update(deltaTime)
        if obj._destroyed:
            gameObjects.remove(obj)
            
def FindMainCamera():
    for obj in gameObjects:
        camera = obj.GetFirstComponentOfType(Camera)
        if camera:
            return camera
    return None

def BuildRenderQueue(camera: Camera):
    queue = []
    
    for obj in gameObjects:
        renderer = obj.GetFirstComponentOfType(SpriteRenderer)
        if not renderer:
            continue
        data = renderer.GetRenderData(camera)
        if data:
            queue.append(data)
    return queue

def RenderQueue(screen: pygame.Surface, camera: Camera, queue):
    sw, sh = camera.ScreenWidth, camera.ScreenHeight
    for item in queue:
        ndc = item["ndc"]
        surface: pygame.Surface = item["surface"]
        depth = max(item["depth"], camera.Near)
        
        if depth <= 0:
            continue
        if not (-1 <= ndc[0] <= 1 and -1 <= ndc[1] <= 1):
            continue

        
        x = (ndc[0]*.5+.5) * sw
        y = (1 - (ndc[1] * .5+.5)) * sh
        
        scale = camera.FocalLength / depth
        w = max(1, int(surface.get_width() * scale))
        h = max(1, int(surface.get_height() * scale))
        
        shade = min(1.0, 5 / depth)
        
        scaled = pygame.transform.scale(surface, (w,h))
        scaled.set_alpha(int(255 * shade))
        screen.blit(scaled, (x-w // 2, y-h // 2))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    InputSystem.GetInstance().Update()

    # UPDATE GAME
    Update(clock.get_time() / 1000.0)
    
    if not MainCamera:
        MainCamera = FindMainCamera()
    
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    if MainCamera:
        renderQueue = BuildRenderQueue(MainCamera)
        renderQueue.sort(key=lambda r: r["depth"], reverse=True)
        RenderQueue(screen, MainCamera, renderQueue)
        

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()