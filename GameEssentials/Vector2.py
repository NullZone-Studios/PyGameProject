from typing import Optional


class Vector2:
    def __init__(self, x: Optional[float] = 0, y: Optional[float] = 0):
        self.X: float = x
        self.Y: float = y
        
    def __add__(self, other: "Vector2") -> "Vector2":
        return Vector2(self.X + other.X, self.Y + other.Y)
    
    def __sub__(self, other: "Vector2") -> "Vector2":
        return Vector2(self.X - other.X, self.Y - other.Y)
    
    def __mul__(self, scalar: float) -> "Vector2":
        return Vector2(self.X * scalar, self.Y * scalar)
    
    def Magnitude(self) -> float:
        return (self.X**2 + self.Y**2)**.5
    
    def Normalize(self) -> "Vector2":
        mag = self.Magnitude()
        if mag == 0:
            return Vector2()
        return Vector2(self.X / mag, self.Y / mag)
    
    def Dot(self, other: "Vector2") -> float:
        return self.X * other.X + self.Y * other.Y
    
    def Perpendicular(self) -> "Vector2":
        return Vector2(-self.Y, self.X)
    
    def Perpendicular_Normal(self):
        perp = self.Perpendicular()
        return perp.Normalize()
    
    def __repr__(self):
        return f"Vector2({self.X}, {self.Y})"