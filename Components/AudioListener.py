from GameEssentials.component import Component
from GameEssentials.soundEngine import SoundEngine
from Components.transform import Transform

class AudioListener(Component):
    
    def Start(self):
        SoundEngine.GetInstance().SetListenerTransform(self.GameObject.Transform)
    
    def Update(self, deltaTime):
        transform: Transform = self.GameObject.Transform
        if not transform:
            return
        