from typing import Optional

class UIElement:
    def __init__(self, tag="div"):
        self.tag = tag
        self.parent = Optional["UIElement"] = None
        self.children: list["UIElement"] = []
        
        self.style = Style()
        self.computedStyle = ComputedStyle()
        
        self.transform = UITransform()
        self.layout = LayoutBox()
        
        self.renderer: Optional["UIRenderer"] = None
        self.events = UIEvents()
        
    def Add(self, child: "UIElement"):
        child.parent = self
        self.children.append(child)