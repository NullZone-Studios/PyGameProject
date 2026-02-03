import pygame
import numpy
from GameEssentials.GameObject import GameObject
from typing import Optional

# pygame setup
pygame.init()
pygame
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Test Project")
clock = pygame.time.Clock()
running = True

gameObjects = list[GameObject]()
MainCamera: Optional[GameObject] = None

def Update(deltaTime: float):
    for obj in gameObjects[:]:
        obj.Update(deltaTime)
        if obj._destroyed:
            gameObjects.remove(obj)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # UPDATE GAME
    Update(clock.get_time())

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("blue")

    # RENDER YOUR GAME HERE
    

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()