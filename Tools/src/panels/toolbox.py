#!/usr/bin/env python3
"""
Component toolbox panel for adding new components
"""

import tkinter as tk
from tkinter import ttk

class ComponentToolbox:
    """Toolbox with draggable components"""
    
    def __init__(self, parent, canvas=None):
        self.parent = parent
        self.canvas = canvas
        
        self.frame = ttk.LabelFrame(parent, text="Components", padding="5")
        self.frame.pack(side='left', fill='y', padx=5, pady=5)
        
        self._create_component_buttons()
    
    def _create_component_buttons(self):
        """Create buttons for all available components"""
        components = [
            ("Horizontal Slider", "horizontalslider"),
            ("Vertical Slider", "verticalslider"),
            ("Knob", "knob"),
            ("Button", "button"),
            ("Toggle", "toggle"),
            ("Label", "label"),
            ("TextBox", "textbox"),
            ("Meter", "meter")
        ]
        
        for display_name, comp_type in components:
            btn = ttk.Button(
                self.frame, 
                text=display_name,
                command=lambda t=comp_type: self.add_component(t)
            )
            btn.pack(fill='x', pady=2)
    
    def add_component(self, comp_type: str):
        """Add a component to the canvas"""
        if self.canvas:
            # Add component to center of canvas
            x = 200  # Default x position
            y = 150  # Default y position
            self.canvas.add_component(comp_type, x, y)
