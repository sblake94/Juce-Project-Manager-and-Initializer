import math
import tkinter as tk
from .component import Component

class Knob(Component):
    """Knob/rotary control component"""
    
    def __init__(self, id: str, x: int, y: int, text: str = ""):
        super().__init__(
            id=id, type='knob', x=x, y=y,
            width=60, height=60, text=text
        )
    
    def draw(self, canvas: tk.Canvas) -> None:
        """Draw knob component"""
        # Draw knob as circle
        canvas.create_oval(
            self.x, self.y, self.x + self.width, self.y + self.height,
            fill=self.color, outline='#888888', width=2,
            tags=f"comp_{self.id}"
        )
        
        # Draw pointer
        center_x, center_y = self.x + self.width//2, self.y + self.height//2
        angle = (self.default_value - self.min_value) / (self.max_value - self.min_value) * 270 - 90
        pointer_x = center_x + math.cos(math.radians(angle)) * (self.width//2 - 5)
        pointer_y = center_y + math.sin(math.radians(angle)) * (self.height//2 - 5)
        canvas.create_line(
            center_x, center_y, pointer_x, pointer_y,
            fill=self.text_color, width=2, tags=f"comp_{self.id}"
        )