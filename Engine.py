import pygame
import numpy
from Components import Camera, SpriteRenderer, Light
from GameEssentials import GameObject, Input, Renderer, GameWorld
from typing import Optional

# pygame setup
class Engine:
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.input = Input.InputSystem()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(game.RESOLUTION)
        pygame.display.set_icon(game.ICON)
        pygame.display.set_caption(game.TITLE)
        self.running = False
        self.renderQueue = []
        self.world = GameWorld()
        self.renderer = Renderer()
    
    def Run(self):
        if self.running:
            return
        self.running = True

        self.world.Awaken()
        self.world.Start()

        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.input.Update()

            # UPDATE GAME
            self.world.Update(self.clock.get_time() / 1000.0)

            if not self.world.MainCamera:
                self.world.FindMainCamera()

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill(self.game.BACKGROUND_COLOR)

            # RENDER YOUR GAME HERE
            if self.world.MainCamera:
                renderQueue = self.renderer.BuildRenderQueue(self.world.MainCamera, self.world.GameObjects)
                self.renderer.RenderQueue(self.screen, self.world.MainCamera, renderQueue)

            # flip() the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60

        pygame.quit()