from Components.UI.UIElement import Element

class Container(Element):
    
    class LayoutDirection:
        VERTICAL = 0
        HORIZONTAL = 1
    
    def __init__(self, layout: int = LayoutDirection.VERTICAL, spacing: int = 5):
        super().__init__()
        self.layout: int = layout
        self.spacing: int = spacing
        
    def ApplyLayout(self):
        offset = 0
        
        for childObj in self.GameObject.Children:
            child: Element = childObj.GetComponent(Element)
            if not child:
                continue
            
            if self.layout == Container.LayoutDirection.VERTICAL:
                child.position.y = offset
                offset += child.size.y + self.spacing
            elif self.layout == Container.LayoutDirection.HORIZONTAL:
                child.position.x = offset
                offset += child.size.x + self.spacing