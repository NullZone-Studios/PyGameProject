from Components import Transform, AudioSource, Script
from GameWorld import GameWorld
import pygame
import random

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
        
        # get the AudioSource on this object
        source: AudioSource = self.GameObject.GetFirstComponentOfType(AudioSource)
        if not source:
            return

        # get the main camera object
        camera = GameWorld.MainCamera
        if not camera:
            return

        # calculate distance between camera and cat
        cat_pos: pygame.Vector3 = self.GameObject.Transform.WorldPosition
        cam_pos: pygame.Vector3 = camera.GameObject.Transform.WorldPosition

        distance_vector = cam_pos - cat_pos
        distance = distance_vector.magnitude()

        # if close enough, play meow
        if distance <= self.MEOW_DISTANCE:
            if not source.channel or not source.channel.get_busy():
                source.Play()
                self.meowCooldown = random.uniform(self.MIN_COOLDOWN, self.MAX_COOLDOWN)
