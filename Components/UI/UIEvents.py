from typing import Callable

class Events:
    def __init__(self):
        self.onClick: Callable = None
        self.onHover: Callable = None