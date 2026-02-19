from GameEssentials.component import Component
from GameEssentials.soundEngine import SoundEngine

class AudioSource(Component):
    def __init__(self, soundName: str, soundPath: str, autoPlay=False, loop=False):
        super().__init__()
        self.soundName = soundName
        self.soundPath = soundPath
        self.autoPlay = autoPlay
        self.loop = loop
        self.source = None

    def Start(self):
        SoundEngine.GetInstance().LoadSFX(self.soundName, self.soundPath)
        if self.autoPlay:
            self.Play()

    def Play(self):
        transform = self.GameObject.Transform
        self.source = SoundEngine.GetInstance().PlaySFX3D(self.soundName, transform.WorldPosition)
        if self.loop and self.source:
            self.source.set_looping(True)
    
    def Stop(self):
        if self.source:
            self.source.stop()
            self.source = None

    def Update(self, deltaTime):
        if not self.source:
            return
        pos = self.GameObject.Transform.WorldPosition
        self.source.set_position((pos.x, pos.y, pos.z))
        
    def OnDestroy(self):
        self.Stop()
        SoundEngine.GetInstance().UnloadSFX(self.soundName)
        return super().OnDestroy()
