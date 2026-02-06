import pygame
import numpy as np
from Components.transform import Transform
from typing import Optional

class BasicChannels:
    UI = "UI"
    PLAYER = "PLAYER"

class SoundEngine:
    instance = None
    
    @staticmethod
    def GetInstance():
        if SoundEngine.instance is None:
            SoundEngine()
        return SoundEngine.instance
    
    def __init__(self):
        if SoundEngine.instance is not None:
            raise Exception("SoundEngine is a singleton! Use SoundEngine.GetInstance()")
        SoundEngine.instance = self
        pygame.mixer.quit()  # optional safety
        pygame.mixer.init(frequency=48000, size=-16, channels=2)

        pygame.mixer.set_num_channels(16)
        
        self.sfx: dict[str, pygame.mixer.Sound] = {}
        self.channels: dict[str, pygame.mixer.Channel] = {
            BasicChannels.UI: pygame.mixer.Channel(0),
            BasicChannels.PLAYER: pygame.mixer.Channel(1)
        }
        
        self.worldChannels = [
            pygame.mixer.Channel(i) for i in range(2, 16)
        ]
        
        self.masterVolume = 1.0
        self.musicVolume = 1.0
        self.sfxVolume = 1.0
        
        self.maxDistance = 1200.0
        self.maxPanDistance = 600.0
        self.listenerTransform: Optional[Transform] = None
        
    def SetListenerTransform(self, listenerTransform: Transform):
        self.listenerTransform = listenerTransform
        
    def LoadSFX(self, name:str, path:str):
        sound = pygame.mixer.Sound(path)
        
        soundArray = pygame.sndarray.array(sound)
        if len(soundArray.shape) == 1:
            stereoArray = np.stack([soundArray, soundArray], axis=1)
            sound = pygame.sndarray.make_sound(stereoArray.astype(np.int16))
        
        self.sfx[name] = sound
        self.applySFXVolume(name)
        
    def PlaySFX(self, name: str, channel: str = BasicChannels.PLAYER):
        if name not in self.sfx:
            print(f"[SoundEngine] Missing SFX: {name}")
            return
        
        ch = self.channels.get(channel)
        if ch:
            ch.play(self.sfx[name])
        else:
            self.sfx[name].play()
            
    def PlaySFX3D(self, name:str, position: pygame.Vector3):
        if name not in self.sfx:
            print(f"[SoundEngine] Missing SFX: {name}")
            return None
        channel: pygame.mixer.Channel = self.getFreeChannel()
        if channel is None:
            return None
        left,right = self.compute3D(position)
        channel.set_volume(left, right)
        channel.play(self.sfx[name])
        return channel
        
    def PlaySFX3DLoop(self, name: str, position: pygame.Vector3):
        if name not in self.sfx:
            return None
        channel = self.getFreeChannel()
        if not channel:
            return None
        
        left,right = self.compute3D(position)
        channel.set_volume(left,right)
        channel.play(self.sfx[name], loops=-1)
        return channel
        
    def compute3D(self, position: pygame.Vector3):
        if self.listenerTransform is None:
            return self.masterVolume * self.sfxVolume, self.masterVolume * self.sfxVolume
    
        listenerPos = self.listenerTransform.WorldPosition
        listenerRight = self.listenerTransform.Right
        listenerForward = self.listenerTransform.Forward
    
        toSound = position - listenerPos
        distance = toSound.magnitude()
        direction = toSound.normalize() if distance != 0 else pygame.Vector3(0,0,1)
    
        # Volume falloff (inverse square style)
        volume = 0 if distance >= self.maxDistance else (1 - (distance / self.maxDistance)**2)
        volume *= self.masterVolume * self.sfxVolume
    
        # Stereo panning
        pan = max(-1, min(1, listenerRight.dot(direction)))
        left = volume * (1 - pan)/2
        right = volume * (1 + pan)/2
    
        return left, right


    
    def getFreeChannel(self):
        for ch in self.worldChannels:
            if not ch.get_busy():
                return ch
        return None
    
    def StopChannel(self, channel: str):
        if channel in self.channels:
            self.channels[channel].stop()
    
    def PlayMusic(self, path: str, loop: bool = True):
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(self.musicVolume * self.masterVolume)
        pygame.mixer.music.play(-1 if loop else 0)
        
    def StopMusic(self):
        pygame.mixer.music.stop()
        
    def SetMasterVolume(self, volume: float):
        self.masterVolume = max(0.0, min(1.0, volume))
        self.updateVolumes()
    
    def SetSFXVolume(self, volume: float):
        self.sfxVolume = max(0,min(1, volume))
        self.updateVolumes()
        
    def SetMusicVolume(self, volume: float):
        self.musicVolume = max(0,min(1, volume))
        self.updateVolumes()
        
    def updateVolumes(self):
        for name in self.sfx:
            self.applySFXVolume(name)
        pygame.mixer.music.set_volume(self.musicVolume * self.masterVolume)
    
    def applySFXVolume(self, name: str):
        self.sfx[name].set_volume(self.sfxVolume * self.masterVolume)