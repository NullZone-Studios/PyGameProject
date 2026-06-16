from GameEssentials import GameObject
from .panel import Panel
import pygame
from typing import Optional
from pygame import Vector2

class Ground(GameObject):
    def __init__(self, name = "Ground", tag= "Ground", parent= None, panelsWide: int = 10, panelsDeep: int = 10, panelSize: int = 100, color: pygame.Color = pygame.Color("white")):
        super().__init__(name, tag, parent)
    
        startLocation: Vector2 = Vector2(0.5 - panelsWide/2, 0.5 - panelsDeep/2)    
        for i in range(panelsWide):
            for j in range(panelsDeep):
                panel = Panel(name= name + "-"+str(i)+","+str(j), tag= tag, parent= self, width=panelSize, depth=panelSize, color=color)
                
                locationX = (startLocation.x+j)*(panelSize*2)
                locationZ = (startLocation.y+i)*(panelSize*2)
                panel.Transform.Translate(x=locationX, z=locationZ)
                
                