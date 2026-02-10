from .UIStyle import Style

class ResolvedStyle(Style):
    def __init__(self, base: Style | None = None, override: Style | None = None):
        super().__init__()
        
        base = base or Style()
        override = override or Style()

        # --- layout ---
        self.display = override.display if override.display is not None else base.display
        self.flexDirection = override.flexDirection if override.flexDirection is not None else base.flexDirection
        self.gap = override.gap if override.gap is not None else base.gap
        self.overflow = override.overflow if override.overflow is not None else base.overflow
        
        self.position = (
            override.position
            if override and override.position is not None
            else base.position if base else "relative"
        )

        # --- size ---
        self.width = override.width if override.width is not None else base.width
        self.height = override.height if override.height is not None else base.height

        # --- positioning (CSS "auto" = None) ---
        self.left = override.left if override.left is not None else base.left
        self.right = override.right if override.right is not None else base.right
        self.top = override.top if override.top is not None else base.top
        self.bottom = override.bottom if override.bottom is not None else base.bottom

        # --- visuals ---
        self.background = override.background if override.background is not None else base.background
        self.borderColor = override.borderColor if override.borderColor is not None else base.borderColor
        self.borderWidth = override.borderWidth if override.borderWidth is not None else base.borderWidth
        self.color = override.color if override.color is not None else base.color

        # --- border radius (CSS-style fallback chain) ---
        radius = override.borderRadius if override.borderRadius is not None else base.borderRadius

        self.borderRadiusTopLeft = (
            override.borderRadiusTopLeft
            if override.borderRadiusTopLeft is not None
            else base.borderRadiusTopLeft
            if base.borderRadiusTopLeft is not None
            else radius
            if radius is not None
            else 0
        )

        self.borderRadiusTopRight = (
            override.borderRadiusTopRight
            if override.borderRadiusTopRight is not None
            else base.borderRadiusTopRight
            if base.borderRadiusTopRight is not None
            else radius
            if radius is not None
            else 0
        )

        self.borderRadiusBottomLeft = (
            override.borderRadiusBottomLeft
            if override.borderRadiusBottomLeft is not None
            else base.borderRadiusBottomLeft
            if base.borderRadiusBottomLeft is not None
            else radius
            if radius is not None
            else 0
        )

        self.borderRadiusBottomRight = (
            override.borderRadiusBottomRight
            if override.borderRadiusBottomRight is not None
            else base.borderRadiusBottomRight
            if base.borderRadiusBottomRight is not None
            else radius
            if radius is not None
            else 0
        )
