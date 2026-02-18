from pygame import Vector2, Surface
from typing import Optional, Callable
import pygame
from .UIStyle import Style, BoxSpacing
from .UIResolvedStyle import ResolvedStyle
from .UIEvent import Event, EventType


class Element:
    def __init__(self, tag: str = "div"):
        self.tag = tag
        self.style: Optional[Style] = None
        self.computedStyle: Optional[ResolvedStyle] = None
        self.children: list["Element"] = []
        self.parent: Optional["Element"] = None

        self.rectangle: pygame.Rect = pygame.Rect(0, 0, 0, 0)
        self.scrollOffset: Vector2 = Vector2(0, 0)
        self.cursor: pygame.Cursor = None
        
        self.states = {key: False for key in Style.PSEUDO_FIELDS}
        self._listeners: dict[str, dict[str, Callable[[Event], None]]] = {}
        self.visible = True

    def AddEventListener(self, eventType: str, callback: Callable[[Event], None], capture: bool = False):
        if eventType not in self._listeners:
            self._listeners[eventType] = {
                "capture": [],
                "bubble": []
            }
        phase = "capture" if capture else "bubble"
        self._listeners[eventType][phase].append(callback)
        
    def RemoveEventListener(self, eventName: str, callback: Callable[[Event], None]):
        """Unsubscribe a callback from an event"""
        lst: list = getattr(self, f"_{eventName}", None)
        if lst is not None and callback in lst:
            lst.remove(callback)

    def SetState(self, state: str, value: bool):
        if state in self.states and self.states[state] != value:
            self.states[state] = value
            self.ResolveStyle(
                self.parent.computedStyle if self.parent else None
            )

    def AddChild(self, child: "Element") -> "Element":
        child.parent = self
        self.children.append(child)
        return child

    def RemoveChild(self, child: "Element"):
        if child in self.children:
            child.parent = None
            self.children.remove(child)
            
    def Query(self, elementType: Optional[type] = None, tag: Optional[str] = None) -> Optional["Element"]:
        if (elementType is None or isinstance(self, elementType)) and (tag is None or self.tag == tag):
            return self
        for child in self.children:
            result = child.Query(elementType, tag)
            if result:
                return result
        return None

        
    def Q(self, elementType: Optional[type] = None, tag: Optional[str] = None):
        return self.Query(elementType = elementType, tag = tag)

    @property
    def AbsoluteRectangle(self) -> pygame.Rect:
        if not self.parent:
            return self.rectangle

        parent_rect = self.parent.AbsoluteRectangle
        return pygame.Rect(
            parent_rect.x + self.rectangle.x,
            parent_rect.y + self.rectangle.y,
            self.rectangle.width,
            self.rectangle.height,
        )

    def ResolveStyle(self, base: Optional[Style] = None):
        self.computedStyle = ResolvedStyle(base=base, override=self.style, states=self.states)
        for child in self.children:
            child.ResolveStyle(self.computedStyle)

    def Layout(self, available: pygame.Rect, measureOnly: bool = False):
        style = self.computedStyle
        padding = style.padding or BoxSpacing()
        margin = style.margin or BoxSpacing()
        position = style.position or "relative"
        display = style.display or "block"
        flexDirection = style.flexDirection or "row"
        gap = style.gap or 0
        left = style.left
        right = style.right
        top = style.top
        bottom = style.bottom
        width = style.width
        height = style.height
        availableWidth = available.width
        availableHeight = available.height
        
        if availableWidth <= 0 or availableHeight <= 0:
             self.rectangle = pygame.Rect(available.x, available.y, 0, 0)
             return
        
        x = None
        y = None
        
        if width is None and left is not None and right is not None:
            width = availableWidth - left - right
        
        if height is None and top is not None and bottom is not None:
            height = availableHeight - top - bottom 
        
        if width is None or height is None:
            relevantChildren = [child for child in self.children if child.computedStyle and (child.computedStyle.position or "relative") != "absolute"]
            if display == "flex":
                availableMainAxis = availableWidth if flexDirection == "row" else availableHeight
                availableMainAxis -= padding.left + padding.right if flexDirection == "row" else padding.top + padding.bottom
                intrinsicWidth, intrinsicHeight = self.measureFlex(relevantChildren, padding, gap, flexDirection, availableMainAxis)
            else:
                intrinsicWidth, intrinsicHeight = self.measureBlock(relevantChildren, padding, availableWidth - padding.left - padding.right)
                
            if width is None:
                width = intrinsicWidth + padding.left + padding.right
            if height is None:
                height = intrinsicHeight + padding.top + padding.bottom
            
        if position == "absolute":
            if left is not None:
                x = available.x +left
            elif right is not None:
                x = available.x + availableWidth - width - right
            else:
                x = available.x
                
            if top is not None:
                y = available.y + top
            elif bottom is not None:
                y = available.y + availableHeight - height - bottom
            else:
                y = available.y
        else:    
            x = available.x + margin.left
            y = available.y + margin.top
            
        self.rectangle = pygame.Rect(x, y, width, height)
        content = self.contentRectangle
        flowChildren = []
        absoluteChildren = []
        
        for child in self.children:
            if not child.computedStyle:
                continue
            if (child.computedStyle.position or "relative") == "absolute":
                absoluteChildren.append(child)
            else:
                flowChildren.append(child)

        if not measureOnly:
            if display == "flex":
                self.layoutFlex(flowChildren, content, gap, flexDirection)
            else:
                self.layoutBlock(flowChildren, content)
            
            for child in absoluteChildren:
                child.Layout(content)

    def measureBlock(self, children: "Element", padding: BoxSpacing, availableWidth: int):
        maxWidth = 0
        totalHeight = 0
                    
        for child in children:
            child.Layout(pygame.Rect(0,0, max(0, availableWidth), 10000), measureOnly=True)
            margin  = child.computedStyle.margin or BoxSpacing()
            
            totalHeight += child.rectangle.height + margin.top + margin.bottom
            maxWidth = max(maxWidth, child.rectangle.width + margin.left + margin.right)
        return maxWidth, totalHeight
    
    def layoutBlock(self, children: "Element", content: pygame.Rect):
        cursorY = content.y
        for child in children:
            style = child.computedStyle
            margin = style.margin or BoxSpacing()
        
            childAvailable = pygame.Rect(
                content.x + margin.left,
                cursorY + margin.top,
                max(0, content.width - margin.left - margin.right),
                max(0, content.height)
            )
            
            child.Layout(childAvailable)
            cursorY += child.rectangle.height + margin.top + margin.bottom
    
    def layoutFlex(self, children: "Element", content: pygame.Rect, gap: int, flexDirection: str):
        cursor = 0
        
        for child in children:
            style = child.computedStyle
            margin = style.margin or BoxSpacing()
            
            if flexDirection == "row":
                childAvailable = pygame.Rect(
                    content.x + cursor + margin.left,
                    content.y + margin.top,
                    max(0, content.width - cursor - margin.left - margin.right),
                    max(0, content.height - margin.top - margin.bottom)
                )
                child.Layout(childAvailable)
                cursor += child.rectangle.width + margin.left + margin.right + gap
            else:
                childAvailable = pygame.Rect(
                    content.x + margin.left,
                    content.y + cursor + margin.top,
                    max(0, content.width - margin.left - margin.right),
                    max(0, content.height - cursor - margin.top - margin.bottom)
                )
                child.Layout(childAvailable)
                cursor += child.rectangle.height + margin.top + margin.bottom + gap
        
    def measureFlex(self, children: "Element", padding: BoxSpacing, gap: int, flexDirection: str, availableMainAxis: int):
        main, cross = 0, 0
        for child in children:
            margin = child.computedStyle.margin or BoxSpacing()
            if flexDirection == "row":
                child.Layout(pygame.Rect(0,0,max(0, availableMainAxis),10000), measureOnly=True)
                main += child.rectangle.width + margin.left + margin.right + gap
                cross = max(cross, child.rectangle.height + margin.top + margin.bottom)
            else:
                child.Layout(pygame.Rect(0,0,10000,max(0, availableMainAxis)), measureOnly=True)
                main += child.rectangle.height + margin.top + margin.bottom + gap
                cross = max(cross, child.rectangle.width + margin.left + margin.right)
        
        if children:
            main -= gap
        
        if flexDirection == "row":
            return main, cross
        else:
            return cross, main
        
    @property
    def contentRectangle(self) -> pygame.Rect:
        padding = self.computedStyle.padding if self.computedStyle and self.computedStyle.padding else BoxSpacing()
        return pygame.Rect(
            self.rectangle.x + padding.left,
            self.rectangle.y + padding.top,
            self.rectangle.width - padding.left - padding.right,
            self.rectangle.height - padding.top - padding.bottom
        )

    def Draw(self, surface: Surface, rectangle: pygame.Rect):
        if not self.computedStyle:
            return
        
        style = self.computedStyle

        if style.background:
            pygame.draw.rect(
                surface,
                style.background,
                rectangle,
                border_top_left_radius=style.borderRadiusTopLeft or 0,
                border_top_right_radius=style.borderRadiusTopRight or 0,
                border_bottom_left_radius=style.borderRadiusBottomLeft or 0,
                border_bottom_right_radius=style.borderRadiusBottomRight or 0,
            )

        if style.borderWidth and style.borderWidth > 0 and style.borderColor:
            pygame.draw.rect(
                surface,
                style.borderColor,
                rectangle,
                width=style.borderWidth,
                border_top_left_radius=style.borderRadiusTopLeft or 0,
                border_top_right_radius=style.borderRadiusTopRight or 0,
                border_bottom_left_radius=style.borderRadiusBottomLeft or 0,
                border_bottom_right_radius=style.borderRadiusBottomRight or 0,
            )

    def Render(self, surface: pygame.Surface, parentClip: Optional[pygame.Rect] = None, offset: Optional[Vector2] = Vector2(0,0)):
        if not self.computedStyle or not self.visible:
            return
        
        rectangle = self.rectangle.move(offset.x, offset.y)
        clipRectangle = rectangle.clip(parentClip) if parentClip else rectangle

    def HitTest(self, point: Vector2, offset: Vector2 = Vector2(0, 0)) -> Optional["Element"]:
        if not self.computedStyle or not self.visible:
            return None
        px, py = point.x - offset.x, point.y - offset.y
        
        rectangle = self.rectangle
        absoluteChildren = []
        flowChildren = []
        for child in self.children:
            if not child.computedStyle:
                continue
            if (child.computedStyle.position or "relative") == "absolute":
                absoluteChildren.append(child)
            else:
                flowChildren.append(child)
        
        for child in reversed(absoluteChildren):
            hit = child.HitTest(point)
            if hit:
                return hit
            
        for child in reversed(flowChildren):
            hit = child.HitTest(point)
            if hit:
                return hit
        
        if self.rectangle.collidepoint(px, py):
            return self
        
        return None
    
    def buildPath(self):
        path = []
        node = self
        while node:
            path.append(node)
            node = node.parent
        return list(reversed(path))
    
    def DispatchEvent(self, event: Event):
        self.updateStateBasedOnEvent(event)
        event.target = self
        path = self.buildPath()
        
        for node in path[:-1]:
            node.updateStateBasedOnEvent(event)
            if event.stopped:
                return
            event.currentTarget = node
            listeners = node._listeners.get(event.type, {})
            for callback in listeners.get("capture", []):
                callback(event)
                if event.immediateStopped:
                    return
        
        if not event.stopped:
            event.currentTarget = self
            listeners = self._listeners.get(event.type, {})
            
            for callback in listeners.get("capture", []):
                callback(event)
                if event.immediateStopped:
                    return
            
            for callback in listeners.get("bubble", []):
                callback(event)
                if event.immediateStopped:
                    return
                    
        for node in reversed(path[:-1]):
            if event.stopped:
                return
            event.currentTarget = node
            listeners = node._listeners.get(event.type, {})
            for callback in listeners.get("bubble", []):
                callback(event)
                if event.immediateStopped:
                    return
    
    def updateStateBasedOnEvent(self, event: Event):
        eventMapping = {
            EventType.MOUSE_ENTER: ("hover", True),
            EventType.MOUSE_LEAVE: ("hover", False),
            EventType.MOUSE_DOWN: ("active", True),
            EventType.MOUSE_UP: ("active", False),
            EventType.FOCUS: ("focus", True),
            EventType.BLUR: ("focus", False)
        }
        
        if event.type in eventMapping:
            state, value = eventMapping[event.type]
            self.SetState(state, value)