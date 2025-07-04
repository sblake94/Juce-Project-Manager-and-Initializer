from .component import Component
import tkinter as tk

class Button(Component):
    """Button component"""
    
    def __init__(self, id: str, x: int, y: int, text: str = ""):
        super().__init__(
            id=id, type='button', x=x, y=y,
            width=80, height=30, text=text
        )
    
    def draw(self, canvas: tk.Canvas) -> None:
        """Draw button component"""
        canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height,
            fill=self.color, outline='#888888', width=1,
            tags=f"comp_{self.id}"
        )