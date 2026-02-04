from GameEssentials import Component, SoundEngine
from Components import Transform

class AudioListener(Component):
    def Update(self, deltaTime):
        transform: Transform = self.GameObject.GetFirstComponentOfType(Transform)
        if not transform:
            return
        
        position = transform.WorldPosition
        SoundEngine.GetInstance().SetListenerPosition(position)
        