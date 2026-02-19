from Components.script import Script
from GameEssentials.soundEngine import SoundEngine
from Components.UI.UILabel import Label

class MasterVolumeLabel(Script):
    def __init__(self, label: Label):
        self.label = label
        
    def Update(self, deltaTime):
        self.label.Text = f"{SoundEngine.GetInstance().masterVolume * 100}%"
        return super().Update(deltaTime)
    
class MusicVolumeLabel(Script):
    def __init__(self, label: Label):
        self.label = label
        
    def Update(self, deltaTime):
        self.label.Text = f"{SoundEngine.GetInstance().musicVolume * 100}%"
        return super().Update(deltaTime)
    
class SFXVolumeLabel(Script):
    def __init__(self, label: Label):
        self.label = label
        
    def Update(self, deltaTime):
        self.label.Text = f"{SoundEngine.GetInstance().sfxVolume * 100}%"
        return super().Update(deltaTime)
    
