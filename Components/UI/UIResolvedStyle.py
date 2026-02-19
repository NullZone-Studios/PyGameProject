from .UIStyle import Style
from typing import Optional

class ResolvedStyle(Style):
    def __init__(self, base: Optional[Style] = None, override: Optional[Style] = None, states: dict = None):
        super().__init__()
        
        base = base or Style()
        override = override or Style()
        states = states or {}

        self.ApplyOverride(base)
        self.ApplyOverride(override, onlyInheritance=False)
        
        for stateName in Style.PSEUDO_FIELDS:
            if states.get(stateName):
                overrideState = getattr(override, stateName, None)
                if overrideState:
                    self.ApplyOverride(overrideState, onlyInheritance=False)
                    
        self.ResolveShorthand()
            

