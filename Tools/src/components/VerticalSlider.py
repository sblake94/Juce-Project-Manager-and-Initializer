import tkinter as tk
from .component import Component

class VerticalSlider(Component):
    """Vertical slider component"""
    
    def __init__(self, id: str, x: int, y: int, text: str = ""):
        super().__init__(
            id=id, type='verticalslider', x=x, y=y,
            width=30, height=120, text=text
        )
    
    def draw(self, canvas: tk.Canvas) -> None:
        """Draw vertical slider"""
        # Draw slider track
        canvas.create_rectangle(
            self.x + self.width//2 - 2, self.y,
            self.x + self.width//2 + 2, self.y + self.height,
            fill='#DDDDDD', tags=f"comp_{self.id}"
        )
        
        # Draw slider thumb
        thumb_y = self.y + self.height - int((self.default_value - self.min_value) / 
                                           (self.max_value - self.min_value) * self.height)
        canvas.create_oval(
            self.x + self.width//2 - 8, thumb_y - 8,
            self.x + self.width//2 + 8, thumb_y + 8,
            fill=self.color, tags=f"comp_{self.id}"
        )