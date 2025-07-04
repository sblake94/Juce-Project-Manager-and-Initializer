from .component import Component
import tkinter as tk

class Toggle(Component):
    """Toggle switch component"""
    
    def __init__(self, id: str, x: int, y: int, text: str = "", default_value: bool = False):
        super().__init__(
            id=id, type='toggle', x=x, y=y,
            width=60, height=30, text=text
        )
        self.default_value: bool = default_value
    
    def draw(self, canvas: tk.Canvas) -> None:
        """Draw toggle switch component"""
        canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height,
            fill='#DDDDDD', outline='#888888', width=1,
            tags=f"comp_{self.id}"
        )
        
        if getattr(self, 'default_value', False):
            canvas.create_rectangle(
                self.x + self.width//2, self.y + 2,
                self.x + self.width - 2, self.y + self.height - 2,
                fill=self.color, tags=f"comp_{self.id}"
            )
        else:
            canvas.create_rectangle(
                self.x + 2, self.y + 2,
                self.x + self.width//2, self.y + self.height - 2,
                fill='#FFFFFF', tags=f"comp_{self.id}"
            )
