import pygame
from GameEssentials import Input, Renderer, GameWorld, SoundEngine
from GameEssentials.collisionSystem import CollisionSystem

# pygame setup
class Engine:    
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.input = Input.InputSystem()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(game.RESOLUTION, flags=pygame.SCALED, vsync=1)
        pygame.display.set_icon(game.ICON)
        pygame.display.set_caption(game.TITLE)
        self.renderQueue = []
        self.world = GameWorld.GetInstance()
        self.renderer = Renderer()
        
    def Stop(self):
        if not self.running:
            return
        self.running = False
    
    def Run(self):
        if self.game.RUNNING:
            return
        self.game.RUNNING = True

        self.world.Awaken()
        self.world.Start()

        while self.game.RUNNING:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.RUNNING = False

            self.input.Update()

            # UPDATE GAME
            self.world.Update(self.clock.get_time() / 1000.0)
            CollisionSystem.Update()

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

            self.clock.tick(120)  # limits FPS to 60

        pygame.quit()