from Components import Transform, AudioSource, Script
from GameWorld import GameWorld
import pygame
import random
from GameEssentials.soundEngine import SoundEngine

class Cat(Script):
    MEOW_DISTANCE = 100.0  # max distance to trigger sound
    MIN_COOLDOWN = 1.4
    MAX_COOLDOWN = 4.0

    def Start(self):
        self.meowCooldown = random.uniform(self.MIN_COOLDOWN, self.MAX_COOLDOWN)

    def Update(self, deltaTime: float):
        if self.meowCooldown > 0:
            self.meowCooldown -= deltaTime
            return
    
        source: AudioSource = self.GameObject.GetFirstComponentOfType(AudioSource)
        if not source:
            return
    
        camera = GameWorld.MainCamera
        if not camera:
            return
    
        cat_pos = self.GameObject.Transform.WorldPosition
        cam_pos = camera.GameObject.Transform.WorldPosition
    
        distance = (cam_pos - cat_pos).magnitude()
    
        if distance <= self.MEOW_DISTANCE:
            # Only check playing state if source exists
            if not source.source or source.source.get_state() != "playing":
                source.Play()
                self.meowCooldown = random.uniform(self.MIN_COOLDOWN, self.MAX_COOLDOWN)

