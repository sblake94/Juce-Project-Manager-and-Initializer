#!/usr/bin/env python3
"""
Component classes for the GUI Designer
"""

from dataclasses import dataclass
import tkinter as tk
import math

@dataclass
class Component:
    """Base component class with common properties"""
    id: str
    type: str
    x: int
    y: int
    width: int
    height: int
    text: str = ""
    min_value: float = 0.0
    max_value: float = 1.0
    default_value: float = 0.5
    color: str = "#CCCCCC"
    text_color: str = "#000000"
    font_size: int = 12
    
    def draw(self, canvas: tk.Canvas) -> None:
        """Base draw method - should be overridden by subclasses"""
        raise NotImplementedError("Subclasses must implement draw method")
    
    def draw_selection_highlight(self, canvas: tk.Canvas) -> None:
        """Draw selection highlight around component"""
        # Default implementation - can be overridden
        text_height = 12 if self.text and self.type not in ['meter', 'label'] else 0
        canvas.create_rectangle(
            self.x - 2, self.y - 2, 
            self.x + self.width + 2, self.y + self.height + text_height + 14,
            outline='#0078D4', width=2, fill='',
            tags=f"comp_{self.id}_select"
        )
    
    def draw_text_label(self, canvas: tk.Canvas) -> None:
        """Draw text label below component (for most component types)"""
        if self.text and self.type not in ['meter', 'label']:
            canvas.create_text(
                self.x + self.width//2, self.y + self.height + 12,
                text=self.text, fill=self.text_color,
                font=('Arial', self.font_size),
                tags=f"comp_{self.id}"
            )
