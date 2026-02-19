from typing import Optional
from GameEssentials import GameObject, Input
from Engine import Engine
import pygame

class GameBuilder:
    RESOLUTION: pygame.Vector2 = pygame.Vector2(1280,720)
    BACKGROUND_COLOR: pygame.Color = pygame.Color(0,0,0)
    ICON: pygame.Surface = pygame.image.load("src/images/weird_cat.png")
    TITLE: str = "Game"
    RUNNING = False
        
    @property
    def World(self) -> list[GameObject]:
        return
    
    def Build(self):
        pass

    def Quit(self):
        self.RUNNING = False