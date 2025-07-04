from .component import Component
import tkinter as tk

class Label(Component):
    """Label component"""
    
    def __init__(self, id: str, x: int, y: int, text: str = "", default_value: str = "Label Text"):
        super().__init__(
            id=id, type='label', x=x, y=y,
            width=60, height=20, text=text
        )
        self.displayed_text: str = default_value
    
    def draw(self, canvas: tk.Canvas) -> None:
        """Draw label component"""
        # Draw the label background rectangle
        canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height,
            fill='#FFFFFF', outline='#CCCCCC', width=1,
            tags=f"comp_{self.id}"
        )
        
        # Draw the text inside the label rectangle
        display_text = str(self.displayed_text) if hasattr(self, 'default_value') and self.displayed_text is not None else ""
        if display_text:
            canvas.create_text(
                self.x + self.width//2, self.y + self.height//2,
                text=display_text, fill=self.text_color,
                font=('Arial', self.font_size), tags=f"comp_{self.id}"
            )
    
    def draw_selection_highlight(self, canvas: tk.Canvas) -> None:
        """Override selection highlight for labels (no extra text area)"""
        canvas.create_rectangle(
            self.x - 2, self.y - 2,
            self.x + self.width + 2, self.y + self.height + 2,
            outline='#0078D4', width=2, fill='',
            tags=f"comp_{self.id}_select"
        )