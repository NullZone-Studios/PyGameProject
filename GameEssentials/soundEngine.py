from pygame import Vector3
from openal import oalInit, oalQuit, oalOpen, oalGetListener, Listener, Source
from Components.transform import Transform
from typing import Optional

class SoundEngine:
    instance = None
    @staticmethod
    def GetInstance():
        if SoundEngine.instance is None:
            SoundEngine()
        return SoundEngine.instance
    
    def __init__(self):
        if SoundEngine.instance:
            raise Exception("SoundEngine is a singleton! Use SoundEngine.GetInstance()")
        SoundEngine.instance = self
        
        oalInit()
        self.sounds: dict[str, Source] = {}
        self.music: dict[str, Source] = {}
        self.listenerTransform: Optional[Transform] = None
        self.listener: Listener = oalGetListener()
        self.masterVolume: float = 1.0
        self.sfxVolume: float = 1.0
        self.musicVolume: float = 1.0
        
    def SetListenerTransform(self, listenerTransform: Transform):
        self.listenerTransform = listenerTransform
        
    def LoadSFX(self, name: str, path: str):
        if name in self.sounds :
            return
        source = oalOpen(path)
        self.sounds[name] = source
        source.set_gain(self.sfxVolume * self.masterVolume)
        
    def LoadMusic(self, name: str, path: str):
        if name in self.music:
            return
        source = oalOpen(path)
        self.music[name] = source
        source.set_gain(self.musicVolume * self.masterVolume)
        
    def UnloadSFX(self, name: str):
        if name not in self.sounds:
            return
        source = self.sounds[name]
        source.stop()
        del self.sounds[name]
        
    def UnloadMusic(self, name:str):
        if name not in self.music:
            return
        source = self.sounds[name]
        source.stop()
        del self.music[name]
        
    def PlaySFX3D(self, name: str, position: Vector3, maxDistance: float = 200):
        if name not in self.sounds:
            print(f"[SoundEngine] Missing SFX: {name}")
            return None
        source: Source = self.sounds[name]
        source.set_position((position.x, position.y, position.z))
        
        source.set_reference_distance(5.0)
        source.set_max_distance(maxDistance)
        source.set_rolloff_factor(1)
        
        source.set_gain(self.sfxVolume * self.masterVolume)
        source.play()
        return source
    
    def PlayMusic(self, name: str, position: Vector3, maxDistance: float = 200):
        if name not in self.music:
            print(f"[SoundEngine] Mussing Music: {name}")
            return None
        source: Source = self.music[name]
        source.set_position((position.x, position.y, position.z))
        source.set_reference_distance(5.0)
        source.set_max_distance(maxDistance)
        source.set_rolloff_factor(1)
        source.set_gain(self.musicVolume * self.masterVolume)
        source.play()
        return source
    
    def UpdateListener(self):
        if not self.listenerTransform:
            return
        position = self.listenerTransform.WorldPosition

        forward = self.listenerTransform.Forward
        up = self.listenerTransform.Up
        
        self.listener.set_position((position.x, position.y, position.z))
        self.listener.set_orientation((forward.x, forward.y, forward.z, up.x, up.y, up.z))
        self.listener.set_gain(self.masterVolume)
        
    def SetMasterVolume(self, volume: float):
        self.masterVolume = max(0, min(1, volume))
        self.UpdateListener()
        self.UpdateMusic()
        self.UpdateSound()
        
    def SetMusicVolume(self, volume: float):
        self.musicVolume = max(0, min(1, volume))
        self.UpdateMusic()
    
    def SetSFXVolume(self, volume: float):
        self.sfxVolume = max(0, min(1, volume))
        self.UpdateSound()
        
    def UpdateMusic(self):
        for music in self.music:
            source = self.music[music]
            source.set_gain(self.musicVolume * self.masterVolume)
    
    def UpdateSound(self):
        for sound in self.sounds:
            source = self.sounds[sound]
            source.set_gain(self.sfxVolume * self.masterVolume)
    
