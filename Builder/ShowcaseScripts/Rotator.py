from Components import Script, Transform

class Rotator(Script):
    def Update(self, deltaTime: float):
        transform: Transform = self.GameObject.Transform
        if transform:
            transform.Rotate(1*deltaTime,1*deltaTime)