from GameEssentials.component import Component
from GameEssentials.soundEngine import SoundEngine
from Components.transform import Transform
import pygame

class AudioSource(Component):
    def __init__(self, soundName: str, soundPath: str, autoPlay: bool = False, loop: bool = False):
        super().__init__()
        self.soundName = soundName
        self.soundPath = soundPath
        self.autoPlay = autoPlay
        self.loop = loop
        self.channel: pygame.mixer.Channel | None = None
        
    def Start(self):
        SoundEngine.GetInstance().LoadSFX(self.soundName, self.soundPath)
        if self.autoPlay:
            self.Play()
            
    def Play(self):
        transform: Transform = self.GameObject.GetFirstComponentOfType(Transform)
        if not transform:
            return

        soundEngine = SoundEngine.GetInstance()
        position = transform.WorldPosition

        # Already has a channel? just keep it
        if self.channel and self.channel.get_busy():
            return

        # Assign a channel for looping or first-time play
        if self.loop:
            self.channel = soundEngine.PlaySFX3DLoop(self.soundName, position)
        else:
            self.channel = soundEngine.PlaySFX3D(self.soundName, position)

    def Update(self, deltaTime):
        if not self.channel:
            return

        transform: Transform = self.GameObject.GetFirstComponentOfType(Transform)
        if not transform:
            return

        position = transform.WorldPosition
        soundEngine = SoundEngine.GetInstance()

        # Update left/right volume using listener's transform
        left, right = soundEngine.compute3D(position)
        self.channel.set_volume(left, right)
