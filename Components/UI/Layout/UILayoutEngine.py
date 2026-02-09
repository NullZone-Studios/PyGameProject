from Components.UI.UIElement import Element

def ApplyFlexLayout(element: Element):
    offset = 0
    
    for child in element.children:
        if element.computedStyle.flexDirection == "row":
            child.layout.x = offset
            child.layout.y = 0
            offset += child.layout.width
        else:
            child.layout.y = offset
            child.layout.x = 0
            offset += child.layout.height

def LayoutElement(element: Element):
    element.layout.width = element.style.width or 100
    element.layout.height = element.style.height or 50
    
    for child in element.children:
        LayoutElement(child)
        
    if element.computedStyle.display == "flex":
        ApplyFlexLayout(element)