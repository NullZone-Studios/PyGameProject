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

    def Layout(self, available: pygame.Rect):
        style = self.computedStyle
        padding = style.padding or BoxSpacing()
        margin = style.margin or BoxSpacing()

        # -----------------------------
        # 1. Resolve own rectangle
        # -----------------------------
        width = style.width
        height = style.height

        x = available.x + margin.left
        y = available.y + margin.top

        if style.position == "absolute":
            width = width or available.width
            height = height or available.height

            x = style.left if style.left is not None else x
            y = style.top if style.top is not None else y

            if style.right is not None:
                x = available.width - width - style.right
            if style.bottom is not None:
                y = available.height - height - style.bottom

            self.rectangle = pygame.Rect(x, y, width, height)

            for child in self.children:
                child.Layout(pygame.Rect(0, 0, width, height))
            return

        # Temporary size if auto
        tempWidth = width if width is not None else available.width - margin.left - margin.right
        tempHeight = height if height is not None else available.height - margin.top - margin.bottom

        self.rectangle = pygame.Rect(x, y, tempWidth, tempHeight)

        # -----------------------------
        # 2. Measure children
        # -----------------------------
        flowChildren = [c for c in self.children if c.computedStyle.position != "absolute"]

        if style.display == "flex":
            intrinsicW, intrinsicH = self._measureFlex(flowChildren, padding)
        else:
            intrinsicW, intrinsicH = self._measureBlock(flowChildren, padding)

        if style.width is None:
            self.rectangle.width = intrinsicW + padding.left + padding.right

        if style.height is None:
            self.rectangle.height = intrinsicH + padding.top + padding.bottom

        # -----------------------------
        # 3. Place children
        # -----------------------------
        if style.display == "flex":
            self._layoutFlex(flowChildren, padding)
        else:
            self._layoutBlock(flowChildren, padding)

        # Absolute children last
        for child in self.children:
            if child.computedStyle.position == "absolute":
                child.Layout(pygame.Rect(0, 0, self.rectangle.width, self.rectangle.height))

    def _measureBlock(self, children, padding):
        y = 0
        maxWidth = 0

        for child in children:
            child.Layout(pygame.Rect(0, 0, 10_000, 10_000))
            m = child.computedStyle.margin or BoxSpacing()

            y += child.rectangle.height + m.top + m.bottom
            maxWidth = max(maxWidth, child.rectangle.width + m.left + m.right)

        return maxWidth, y


    def _layoutBlock(self, children, padding):
        y = padding.top

        for child in children:
            m = child.computedStyle.margin or BoxSpacing()

            child.Layout(pygame.Rect(
                padding.left + m.left,
                y + m.top,
                self.rectangle.width - padding.left - padding.right - m.left - m.right,
                self.rectangle.height
            ))

            y += child.rectangle.height + m.top + m.bottom
            
    def _measureFlex(self, children, padding):
        style = self.computedStyle
        gap = style.gap or 0

        main = 0
        cross = 0

        for child in children:
            child.Layout(pygame.Rect(0, 0, 10_000, 10_000))
            m = child.computedStyle.margin or BoxSpacing()

            if style.flexDirection == "row":
                main += child.rectangle.width + m.left + m.right + gap
                cross = max(cross, child.rectangle.height + m.top + m.bottom)
            else:
                main += child.rectangle.height + m.top + m.bottom + gap
                cross = max(cross, child.rectangle.width + m.left + m.right)

        return (main, cross) if style.flexDirection == "row" else (cross, main)


    def _layoutFlex(self, children, padding):
        style = self.computedStyle
        gap = style.gap or 0

        cursor = 0

        for child in children:
            m = child.computedStyle.margin or BoxSpacing()

            w = child.computedStyle.width or child.rectangle.width
            h = child.computedStyle.height or child.rectangle.height

            if style.flexDirection == "row":
                x = padding.left + cursor + m.left
                y = padding.top + m.top

                child.Layout(pygame.Rect(x, y, w, h))

                cursor += w + m.left + m.right + gap

            else:  # column
                x = padding.left + m.left
                y = padding.top + cursor + m.top

                child.Layout(pygame.Rect(x, y, w, h))

                cursor += h + m.top + m.bottom + gap




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

    def Render(self, surface: pygame.Surface, parentClip: Optional[pygame.Rect] = None, offset: Optional[Vector2] = None):
        if not self.computedStyle:
            return
        if not self.visible:
            return
        
        offset = offset if offset is not None else Vector2(0,0)

        style = self.computedStyle
        padding = style.padding or BoxSpacing()
        
        rectangle: pygame.Rect = pygame.Rect(
            offset.x + self.rectangle.x,
            offset.y + self.rectangle.y,
            self.rectangle.width,
            self.rectangle.height
        )
        
        effectiveClip = parentClip
        
        hidden = style.overflow in ("hidden", "scroll", "scroll-x", "scroll-y")
        rounded = (style.borderRadiusTopLeft or style.borderRadiusTopRight or style.borderRadiusBottomLeft or style.borderRadiusBottomRight)
        hasRoundedMask = hidden and rounded
        
        if hidden:
            if effectiveClip:
                effectiveClip = rectangle.clip(effectiveClip)
            else:
                effectiveClip = rectangle.copy()
        
        oldClip = surface.get_clip()
        if effectiveClip:
            surface.set_clip(effectiveClip)
            
        self.Draw(surface, rectangle)
        
        childOffset: Vector2 = Vector2(
            rectangle.x - self.scrollOffset.x,
            rectangle.y - self.scrollOffset.y
        )
        
        if hasRoundedMask:
            temp = pygame.Surface(rectangle.size, pygame.SRCALPHA)
            
            localOffset = Vector2(
                -self.scrollOffset.x,
                -self.scrollOffset.y
            )
            for child in self.children:
                    child.Render(temp, None, localOffset)

            mask = pygame.Surface(rectangle.size, pygame.SRCALPHA)
            pygame.draw.rect(
                mask,
                (255,255,255,255),
                mask.get_rect(),
                border_top_left_radius=style.borderRadiusTopLeft or 0,
                border_top_right_radius=style.borderRadiusTopRight or 0,
                border_bottom_left_radius=style.borderRadiusBottomLeft or 0,
                border_bottom_right_radius=style.borderRadiusBottomRight or 0
            )
            
            temp.blit(mask, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
            
            if parentClip:
                surface.set_clip(parentClip)
            
            surface.blit(temp, rectangle.topleft)
        else:
            
            for child in self.children:
                    child.Render(surface, effectiveClip, childOffset)

        surface.set_clip(oldClip)

    def HitTest(self, point: Vector2, offset: Optional[Vector2] = None) -> Optional["Element"]:
        if not self.computedStyle:
            return None
        if not self.visible:
            return None
        
        offset = offset if offset is not None else Vector2(0,0)
        padding = self.computedStyle.padding or BoxSpacing()
        
        rectangle = pygame.Rect(
            offset.x + self.rectangle.x,
            offset.y + self.rectangle.y,
            self.rectangle.width,
            self.rectangle.height
        )
        
        style = self.computedStyle
        
        if style.overflow in ("hidden", "scroll", "scroll-x", "scroll-y"):
            if not rectangle.collidepoint(point):
                return None
        else:
            if not rectangle.collidepoint(point):
                return None
        
        childOffset = Vector2(
            rectangle.x - self.scrollOffset.x,
            rectangle.y - self.scrollOffset.y
        )
        
        for child in reversed(self.children):
            hit = child.HitTest(point, childOffset)
            if hit:
                return hit
            
        return self
    
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