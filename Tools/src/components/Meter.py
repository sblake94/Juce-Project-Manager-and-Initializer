import tkinter as tk
from .component import Component

class Meter(Component):
    """Level meter component"""
    
    def __init__(self, id: str, x: int, y: int, text: str = ""):
        super().__init__(
            id=id, type='meter', x=x, y=y,
            width=20, height=100, text=text
        )
    
    def draw(self, canvas: tk.Canvas) -> None:
        """Draw meter component"""
        canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height,
            fill='#000000', outline='#888888', width=1,
            tags=f"comp_{self.id}"
        )
        
        # Draw level (no default value, just draw empty meter or implement as needed)
        pass
    
    def draw_selection_highlight(self, canvas: tk.Canvas) -> None:
        """Override selection highlight for meters (no extra text area)"""
        canvas.create_rectangle(
            self.x - 2, self.y - 2,
            self.x + self.width + 2, self.y + self.height + 2,
            outline='#0078D4', width=2, fill='',
            tags=f"comp_{self.id}_select"
        )
