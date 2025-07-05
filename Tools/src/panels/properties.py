#!/usr/bin/env python3
"""
Properties panel for editing component properties
"""

import tkinter as tk
from tkinter import ttk, colorchooser
from typing import Optional
from ..components.component import Component

class PropertiesPanel:
    """Properties panel for editing selected component properties"""
    
    def __init__(self, app, parent):
        self.app = app  # Reference to main app
        self.parent = parent
        self.current_component: Optional[Component] = None
        
        self.frame = ttk.LabelFrame(parent, text="Component Properties", padding="5")
        # Don't pack automatically - let parent control when to show/hide
        
        self.property_widgets = {}
        self._create_property_widgets()
    
    def _create_property_widgets(self):
        """Create property editing widgets"""
        # Position
        ttk.Label(self.frame, text="Position & Size").pack(anchor='w', pady=(0, 5))
        
        pos_frame = ttk.Frame(self.frame)
        pos_frame.pack(fill='x', pady=2)
        
        ttk.Label(pos_frame, text="X:").pack(side='left')
        self.property_widgets['x'] = ttk.Entry(pos_frame, width=8)
        self.property_widgets['x'].pack(side='left', padx=2)
        self.property_widgets['x'].bind('<Return>', self._on_property_change)
        self.property_widgets['x'].bind('<FocusOut>', self._on_property_change)
        
        ttk.Label(pos_frame, text="Y:").pack(side='left', padx=(10, 0))
        self.property_widgets['y'] = ttk.Entry(pos_frame, width=8)
        self.property_widgets['y'].pack(side='left', padx=2)
        self.property_widgets['y'].bind('<Return>', self._on_property_change)
        self.property_widgets['y'].bind('<FocusOut>', self._on_property_change)
        
        size_frame = ttk.Frame(self.frame)
        size_frame.pack(fill='x', pady=2)
        
        ttk.Label(size_frame, text="W:").pack(side='left')
        self.property_widgets['width'] = ttk.Entry(size_frame, width=8)
        self.property_widgets['width'].pack(side='left', padx=2)
        self.property_widgets['width'].bind('<Return>', self._on_property_change)
        self.property_widgets['width'].bind('<FocusOut>', self._on_property_change)
        
        ttk.Label(size_frame, text="H:").pack(side='left', padx=(10, 0))
        self.property_widgets['height'] = ttk.Entry(size_frame, width=8)
        self.property_widgets['height'].pack(side='left', padx=2)
        self.property_widgets['height'].bind('<Return>', self._on_property_change)
        self.property_widgets['height'].bind('<FocusOut>', self._on_property_change)
        
        # Text properties
        ttk.Separator(self.frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(self.frame, text="Text Properties").pack(anchor='w', pady=(0, 5))
        
        text_frame = ttk.Frame(self.frame)
        text_frame.pack(fill='x', pady=2)
        ttk.Label(text_frame, text="Label:").pack(side='left')
        self.property_widgets['text'] = ttk.Entry(text_frame)
        self.property_widgets['text'].pack(side='left', fill='x', expand=True, padx=2)
        self.property_widgets['text'].bind('<Return>', self._on_property_change)
        self.property_widgets['text'].bind('<FocusOut>', self._on_property_change)
        
        # Default Value (for labels and other components)
        default_frame = ttk.Frame(self.frame)
        default_frame.pack(fill='x', pady=2)
        ttk.Label(default_frame, text="Value:").pack(side='left')
        self.property_widgets['default_value'] = ttk.Entry(default_frame)
        self.property_widgets['default_value'].pack(side='left', fill='x', expand=True, padx=2)
        self.property_widgets['default_value'].bind('<Return>', self._on_property_change)
        self.property_widgets['default_value'].bind('<FocusOut>', self._on_property_change)
        
        # Value ranges
        ttk.Separator(self.frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(self.frame, text="Value Range").pack(anchor='w', pady=(0, 5))
        
        range_frame = ttk.Frame(self.frame)
        range_frame.pack(fill='x', pady=2)
        
        ttk.Label(range_frame, text="Min:").pack(side='left')
        self.property_widgets['min_value'] = ttk.Entry(range_frame, width=8)
        self.property_widgets['min_value'].pack(side='left', padx=2)
        self.property_widgets['min_value'].bind('<Return>', self._on_property_change)
        self.property_widgets['min_value'].bind('<FocusOut>', self._on_property_change)
        
        ttk.Label(range_frame, text="Max:").pack(side='left', padx=(10, 0))
        self.property_widgets['max_value'] = ttk.Entry(range_frame, width=8)
        self.property_widgets['max_value'].pack(side='left', padx=2)
        self.property_widgets['max_value'].bind('<Return>', self._on_property_change)
        self.property_widgets['max_value'].bind('<FocusOut>', self._on_property_change)
        
        # Colors
        ttk.Separator(self.frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(self.frame, text="Colors").pack(anchor='w', pady=(0, 5))
        
        color_frame = ttk.Frame(self.frame)
        color_frame.pack(fill='x', pady=2)
        
        ttk.Button(color_frame, text="Background Color", 
                  command=self._choose_background_color).pack(fill='x', pady=1)
        ttk.Button(color_frame, text="Text Color", 
                  command=self._choose_text_color).pack(fill='x', pady=1)
        
        # Font size
        font_frame = ttk.Frame(self.frame)
        font_frame.pack(fill='x', pady=2)
        ttk.Label(font_frame, text="Font Size:").pack(side='left')
        self.property_widgets['font_size'] = ttk.Entry(font_frame, width=8)
        self.property_widgets['font_size'].pack(side='left', padx=2)
        self.property_widgets['font_size'].bind('<Return>', self._on_property_change)
        self.property_widgets['font_size'].bind('<FocusOut>', self._on_property_change)
    
    def _on_property_change(self, event=None):
        """Handle property value changes"""
        if not self.current_component:
            return
        
        try:
            # Update component properties from widgets
            self.current_component.x = int(self.property_widgets['x'].get())
            self.current_component.y = int(self.property_widgets['y'].get())
            self.current_component.width = int(self.property_widgets['width'].get())
            self.current_component.height = int(self.property_widgets['height'].get())
            self.current_component.text = self.property_widgets['text'].get()
            
            # Handle default_value - could be string or float
            default_val = self.property_widgets['default_value'].get()
            if self.current_component.type == 'label':
                # For labels, default_value is the display text
                self.current_component.default_value = default_val
            else:
                # For other components, try to convert to float
                try:
                    self.current_component.default_value = float(default_val)
                except ValueError:
                    self.current_component.default_value = 0.5
            
            self.current_component.min_value = float(self.property_widgets['min_value'].get())
            self.current_component.max_value = float(self.property_widgets['max_value'].get())
            self.current_component.font_size = int(self.property_widgets['font_size'].get())
            
            # Trigger redraw of the component
            if hasattr(self.app, 'canvas_frame'):
                self.app.canvas_frame.draw_component(self.current_component)
                
        except ValueError:
            # Handle invalid input gracefully
            pass
    
    def _choose_background_color(self):
        """Choose background color"""
        if self.current_component:
            color = colorchooser.askcolor(initialcolor=self.current_component.color)
            if color[1]:  # color[1] is the hex string
                self.current_component.color = color[1]
                self.app.canvas_frame.draw_component(self.current_component)
    
    def _choose_text_color(self):
        """Choose text color"""
        if self.current_component:
            color = colorchooser.askcolor(initialcolor=self.current_component.text_color)
            if color[1]:  # color[1] is the hex string
                self.current_component.text_color = color[1]
                self.app.canvas_frame.draw_component(self.current_component)
    
    def update_properties(self, component: Component):
        """Update property widgets with component values"""
        self.current_component = component
        
        # Update all property widgets
        self.property_widgets['x'].delete(0, tk.END)
        self.property_widgets['x'].insert(0, str(component.x))
        
        self.property_widgets['y'].delete(0, tk.END)
        self.property_widgets['y'].insert(0, str(component.y))
        
        self.property_widgets['width'].delete(0, tk.END)
        self.property_widgets['width'].insert(0, str(component.width))
        
        self.property_widgets['height'].delete(0, tk.END)
        self.property_widgets['height'].insert(0, str(component.height))
        
        self.property_widgets['text'].delete(0, tk.END)
        self.property_widgets['text'].insert(0, component.text)
        
        self.property_widgets['default_value'].delete(0, tk.END)
        if hasattr(component, 'default_value'):
            self.property_widgets['default_value'].insert(0, str(getattr(component, 'default_value', "")))
        else:
            self.property_widgets['default_value'].insert(0, "")
        
        self.property_widgets['min_value'].delete(0, tk.END)
        self.property_widgets['min_value'].insert(0, str(component.min_value))
        
        self.property_widgets['max_value'].delete(0, tk.END)
        self.property_widgets['max_value'].insert(0, str(component.max_value))
        
        self.property_widgets['font_size'].delete(0, tk.END)
        self.property_widgets['font_size'].insert(0, str(component.font_size))
    
    def clear_properties(self):
        """Clear all property widgets"""
        self.current_component = None
        for widget in self.property_widgets.values():
            if hasattr(widget, 'delete'):
                widget.delete(0, tk.END)