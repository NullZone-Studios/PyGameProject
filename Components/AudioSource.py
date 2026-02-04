from GameEssentials import Component, SoundEngine
from Components import Transform

class AudioSource(Component):
    def __init__(self, soundName: str, autoPlay: bool = False, loop: bool = False):
        super().__init__()
        self.soundName = soundName
        self.autoPlay = autoPlay
        self.loop = loop
        self.channel = None
        
    def Start(self):
        if self.autoPlay:
            self.Play()
            
    def Play(self):
        transform: Transform = self.GameObject.GetFirstComponentOfType(Transform)
        if not transform:
            return
        
        position = transform.WorldPosition
        soundEngine = SoundEngine.GetInstance()
        
        if self.loop:
            self.channel = soundEngine.PlaySFX3DLoop(
                self.soundName,
                (position.x,position.y,position.z)
            )
        else:
            soundEngine.PlaySFX3D(
                self.soundName,
                (position.x,position.y,position.z)
            )
        
    def Update(self, deltaTime):
        if not self.channel:
            return
        
        transform: Transform = self.GameObject.GetFirstComponentOfType(Transform)
        if not transform:
            return
        
        position = transform.WorldPosition
        left, right = SoundEngine.GetInstance().compute3D(
            (position.x,position.y,position.z)
        )
        self.channel.set_volume(left,right)
        
        