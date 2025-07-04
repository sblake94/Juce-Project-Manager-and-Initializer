import tkinter as tk
from .component import Component

class HorizontalSlider(Component):
    """Horizontal slider component"""
    
    def __init__(self, id: str, x: int, y: int, text: str = "", default_value: float = 0.5):
        super().__init__(
            id=id, type='horizontalslider', x=x, y=y,
            width=120, height=30, text=text
        )
        self.default_value: float = default_value
    
    def draw(self, canvas: tk.Canvas) -> None:
        """Draw horizontal slider"""
        # Draw slider track
        canvas.create_rectangle(
            self.x, self.y + self.height//2 - 2,
            self.x + self.width, self.y + self.height//2 + 2,
            fill='#DDDDDD', tags=f"comp_{self.id}"
        )
        
        # Draw slider thumb
        thumb_x = self.x + int((self.default_value - self.min_value) / 
                              (self.max_value - self.min_value) * self.width)
        canvas.create_oval(
            thumb_x - 8, self.y + self.height//2 - 8,
            thumb_x + 8, self.y + self.height//2 + 8,
            fill=self.color, tags=f"comp_{self.id}"
        )