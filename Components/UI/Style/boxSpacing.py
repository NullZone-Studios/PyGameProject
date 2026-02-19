class BoxSpacing:
    def __init__(self, top=0, left=0, bottom=0, right=0):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left
        
    def from_value(value):
        if isinstance(value,(int, float)):
            return BoxSpacing(value, value, value, value)
        if isinstance(value, tuple):
            if len(value) == 2:
                return BoxSpacing(value[0], value[1], value[0], value[1])
            elif len(value) == 4:
                return BoxSpacing(*value)
        if value is None:
            return None
        return BoxSpacing()