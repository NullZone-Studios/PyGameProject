from GameEssentials.Input import InputLayer, InputEvent, DeviceType, ButtonState, MouseCodes
from .UIEvent import Event, EventType
from pygame import Vector2, mouse, cursors
import pygame
from typing import Optional

class UILayer(InputLayer):
    def __init__(self, canvas: "Canvas"):
        self.canvas = canvas
        self.lastMousePos: Optional[Vector2] = None
        self.hovered: Optional["Element"] = None
        self.focused: Optional["Element"] = None
        self.pressed: bool = False

    def HandleEvent(self, event: InputEvent):
        if event.device != DeviceType.MOUSE:
            return

        # --- get current mouse position ---
        pos = Vector2(event.position) if event.position else None

        canvasRoot = self.canvas.root

        # --- MOUSE MOVE ---
        if event.code == MouseCodes.MOVE and pos:  # reserved code for mouse move
            # hover detection
            hoverTarget = canvasRoot.HitTest(pos)
            if hoverTarget != self.hovered:
                if self.hovered:
                    e = Event(EventType.MOUSE_LEAVE, position=pos)
                    event.consumed = self.hovered.HandleEvent(e)
                if hoverTarget:
                    e = Event(EventType.MOUSE_ENTER, position=pos)
                    event.consumed = hoverTarget.HandleEvent(e)
                self.hovered = hoverTarget
                
                # --- Cursor changing ---
                if self.hovered and self.hovered.cursor:
                    mouse.set_cursor(self.hovered.cursor)
                elif self.hovered and self.hovered.parent and self.hovered.parent.cursor:
                    mouse.set_cursor(self.hovered.parent.cursor)
                else:
                    mouse.set_cursor(cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))

            # drag detection
            if self.lastMousePos:
                delta = pos - self.lastMousePos
                if self.pressed and delta.length_squared() > 0 and self.hovered:
                    e = Event(EventType.MOUSE_DRAG, position=pos, delta=delta)
                    event.consumed = self.hovered.HandleEvent(e)

            self.lastMousePos = pos
            return  # handled move event

        # --- SCROLL WHEEL ---
        if event.code == MouseCodes.SCROLL and event.delta:  # reserved code for wheel
            if self.hovered:
                e = Event(EventType.MOUSE_SCROLL, delta=event.delta, position=pos)
                event.consumed = self.hovered.HandleEvent(e)
            return  # handled scroll

        # --- BUTTON EVENTS (click, down, up) ---
        if not pos or event.state is None:
            return

        # button down
        if event.state == ButtonState.PRESSED:
            if self.hovered:
                e = Event(EventType.MOUSE_DOWN, position=pos)
                event.consumed = self.hovered.HandleEvent(e)
            self.pressed = True

        # button up
        elif event.state == ButtonState.RELEASED:
            if self.hovered:
                if self.focused and self.focused != self.hovered:
                    e = Event(EventType.BLUR)
                    event.consumed = self.focused.HandleEvent(e)
                self.focused = self.hovered
                e = Event(EventType.FOCUS)
                event.consumed = self.focused.HandleEvent(e)
                e = Event(EventType.MOUSE_UP, position=pos)
                event.consumed = self.hovered.HandleEvent(e)
                e = Event(EventType.MOUSE_CLICK, position=pos)
                event.consumed = self.hovered.HandleEvent(e)
            self.pressed = False