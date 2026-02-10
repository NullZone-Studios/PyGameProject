# Components/UI/Utils/HitTest.py

def hitTest(element, rect, mouse_pos):
    if not rect.collidepoint(mouse_pos):
        return None

    for child in reversed(element.children):
        hit = hitTest(child, child._worldRect, mouse_pos)
        if hit:
            return hit

    return element
