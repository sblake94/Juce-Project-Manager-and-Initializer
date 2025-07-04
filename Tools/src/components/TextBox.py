import tkinter as tk
from .component import Component


class TextBox(Component):
    """Text input box component"""
    
    def __init__(self, id: str, x: int, y: int, text: str = ""):
        super().__init__(
            id=id, type='textbox', x=x, y=y,
            width=100, height=25, text=text
        )
    
    def draw(self, canvas: tk.Canvas) -> None:
        """Draw textbox component"""
        canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height,
            fill='#FFFFFF', outline='#888888', width=1,
            tags=f"comp_{self.id}"
        )
