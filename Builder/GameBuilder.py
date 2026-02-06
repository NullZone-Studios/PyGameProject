from typing import Optional
from GameEssentials import GameObject
from Engine import Engine
import pygame

class GameBuilder:
    RESOLUTION: pygame.Vector2 = pygame.Vector2(1280,720)
    BACKGROUND_COLOR: pygame.Color = pygame.Color(0,0,0)
    ICON: pygame.Surface = pygame.image.load("src/images/weird_cat.png")
    TITLE: str = "Game"
    
    def Build(self, gameObjects: list[GameObject]):
        pass
    
    def Start(self):
        Engine.Run(self)