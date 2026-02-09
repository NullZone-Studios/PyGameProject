from Components.UI.UIStyle import Style
from Components.UI.UIComputedStyle import ComputedStyle
from Components.UI.UITransform import Transform
from Components.UI.Layout.UILayoutBox import LayoutBox
from Components.UI.UIEvents import Events

from typing import Optional

class Element:
    def __init__(self, tag: str = "div", parent: Optional["Element"] = None, style: Optional[Style] = None):
        self.tag: str = tag
        self.parent: Optional["Element"] = parent
        self.children: list["Element"] = []
        self.style = style if style else Style()
        self.computedStyle = ComputedStyle()
        self.layout = LayoutBox()
        self.transform = Transform()
        self.events = Events()
        self.renderer = None
        
    def Add(self, child: "Element"):
        child.parent = self
        self.children.append(child)
        return child
