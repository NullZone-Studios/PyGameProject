import pygame

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
        pygame.mixer.init()
        
        self.sfx: dict[str, pygame.mixer.Sound] = {}
        self.channels: dict[str, pygame.mixer.Channel] = {
            BasicChannels.UI: pygame.mixer.Channel(0),
            BasicChannels.PLAYER: pygame.mixer.Channel(1)
        }
        
        self.worldChannels = [
            pygame.mixer.Channel(i) for i in range(2,16)
        ]
        
        self.masterVolume = 1.0
        self.musicVolume = 1.0
        self.sfxVolume = 1.0
        
        self.maxDistance = 1200.0
        self.maxPanDistance = 600.0
        self.listenerPosition: pygame.Vector3 = pygame.Vector3(0,0,0)
        
    def SetListenerPosition(self, position: pygame.Vector3):
        self.listenerPosition = position
        
    def LoadSFX(self, name:str, path:str):
        self.sfx[name] = pygame.mixer.Sound(path)
        self.applySFXVolume(name)
        
    def PlaySFX(self, name: str, channel: str = BasicChannels.WORLD):
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
            return
        channel: pygame.mixer.Channel = self.getFreeChannel()
        if channel is None:
            return
        left,right = self.compute3D(position)
        channel.set_volume(left, right)
        channel.play(self.sfx[name])
        
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
        lx, ly, lz = self.listenerPosition
        sx, sy, sz = position
        
        dx = sx-lx
        dy = sy-ly
        dz = sz-lz
        
        distance = (dx**2 + dy**2 + dz**2)**.5
        volume = max(0, 1 - (distance / self.maxDistance))
        volume *= self.masterVolume * self.sfxVolume
        
        pan = max(-1, min(1,dx/self.maxPanDistance))
        
        left = volume * (1.0 - pan) * .5
        right = volume * (1.0 + pan) * .5
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