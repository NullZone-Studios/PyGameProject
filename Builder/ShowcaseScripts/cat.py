from Components import Transform, AudioSource, Script
import pygame
import random
from GameEssentials.soundEngine import SoundEngine

class Cat(Script):
    MEOW_DISTANCE = 100.0  # max distance to trigger sound
    MIN_COOLDOWN = 1.4
    MAX_COOLDOWN = 4.0
    
    def __init__(self, player):
        super().__init__()
        self.player = player

    def Start(self):
        self.meowCooldown = random.uniform(self.MIN_COOLDOWN, self.MAX_COOLDOWN)

    def Update(self, deltaTime: float):
        if self.meowCooldown > 0:
            self.meowCooldown -= deltaTime
            return
    
        source: AudioSource = self.GameObject.GetFirstComponentOfType(AudioSource)
        if not source:
            return
    
        cat_pos = self.player.Transform.WorldPosition
        cam_pos = self.player.Transform.WorldPosition
    
        distance = (cam_pos - cat_pos).magnitude()
    
        if distance <= self.MEOW_DISTANCE:
            # Only check playing state if source exists
            if not source.source or source.source.get_state() != "playing":
                source.Play()
                self.meowCooldown = random.uniform(self.MIN_COOLDOWN, self.MAX_COOLDOWN)

