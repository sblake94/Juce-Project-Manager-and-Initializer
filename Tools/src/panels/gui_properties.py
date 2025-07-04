#!/usr/bin/env python3
"""
GUI Properties panel for editing overall plugin GUI properties
"""

import tkinter as tk
from tkinter import ttk, colorchooser
from typing import Dict, Any, Callable

class GUIProperties:
    """Class to hold overall GUI properties"""
    
    def __init__(self):
        self.background_color = "#F0F0F0"
        self.width = 400
        self.height = 300
        self.title = "Audio Plugin"
        self.grid_size = 10
        self.show_grid = False
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert properties to dictionary for saving"""
        return {
            'background_color': self.background_color,
            'width': self.width,
            'height': self.height,
            'title': self.title,
            'grid_size': self.grid_size,
            'show_grid': self.show_grid
        }
    
    def from_dict(self, data: Dict[str, Any]):
        """Load properties from dictionary"""
        self.background_color = data.get('background_color', self.background_color)
        self.width = data.get('width', self.width)
        self.height = data.get('height', self.height)
        self.title = data.get('title', self.title)
        self.grid_size = data.get('grid_size', self.grid_size)
        self.show_grid = data.get('show_grid', self.show_grid)


class GUIPropertiesPanel:
    """Panel for editing overall GUI properties"""
    
    def __init__(self, parent, gui_properties: GUIProperties, on_change_callback: Callable = None):
        self.parent = parent
        self.gui_properties = gui_properties
        self.on_change_callback = on_change_callback
        
        self.frame = ttk.LabelFrame(parent, text="GUI Properties", padding="5")
        self.frame = ttk.LabelFrame(parent, text="GUI Properties", padding="5")
        # Don't pack automatically - let parent control when to show/hide
        
        self.property_widgets = {}
        self._create_property_widgets()
        self.update_widgets()
    
    def _create_property_widgets(self):
        """Create property editing widgets"""
        
        # GUI Title
        title_frame = ttk.Frame(self.frame)
        title_frame.pack(fill='x', pady=2)
        ttk.Label(title_frame, text="Title:").pack(side='left')
        self.property_widgets['title'] = ttk.Entry(title_frame)
        self.property_widgets['title'].pack(side='left', fill='x', expand=True, padx=2)
        self.property_widgets['title'].bind('<Return>', self._on_property_change)
        self.property_widgets['title'].bind('<FocusOut>', self._on_property_change)
        
        # Canvas Size
        ttk.Separator(self.frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(self.frame, text="Canvas Size").pack(anchor='w', pady=(0, 5))
        
        size_frame = ttk.Frame(self.frame)
        size_frame.pack(fill='x', pady=2)
        
        ttk.Label(size_frame, text="Width:").pack(side='left')
        self.property_widgets['width'] = ttk.Entry(size_frame, width=8)
        self.property_widgets['width'].pack(side='left', padx=2)
        self.property_widgets['width'].bind('<Return>', self._on_property_change)
        self.property_widgets['width'].bind('<FocusOut>', self._on_property_change)
        
        ttk.Label(size_frame, text="Height:").pack(side='left', padx=(10, 0))
        self.property_widgets['height'] = ttk.Entry(size_frame, width=8)
        self.property_widgets['height'].pack(side='left', padx=2)
        self.property_widgets['height'].bind('<Return>', self._on_property_change)
        self.property_widgets['height'].bind('<FocusOut>', self._on_property_change)
        
        # Background Color
        ttk.Separator(self.frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(self.frame, text="Appearance").pack(anchor='w', pady=(0, 5))
        
        color_frame = ttk.Frame(self.frame)
        color_frame.pack(fill='x', pady=2)
        ttk.Label(color_frame, text="Background:").pack(side='left')
        
        self.property_widgets['background_color'] = tk.Frame(color_frame, width=30, height=20, relief='sunken', bd=1)
        self.property_widgets['background_color'].pack(side='left', padx=5)
        self.property_widgets['background_color'].bind('<Button-1>', self._choose_background_color)
        
        ttk.Button(color_frame, text="Choose", command=self._choose_background_color).pack(side='left', padx=5)
        
        # Grid Settings
        ttk.Separator(self.frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(self.frame, text="Grid Settings").pack(anchor='w', pady=(0, 5))
        
        grid_frame = ttk.Frame(self.frame)
        grid_frame.pack(fill='x', pady=2)
        
        self.property_widgets['show_grid'] = tk.BooleanVar()
        ttk.Checkbutton(grid_frame, text="Show Grid", 
                       variable=self.property_widgets['show_grid'],
                       command=self._on_property_change).pack(side='left')
        
        grid_size_frame = ttk.Frame(self.frame)
        grid_size_frame.pack(fill='x', pady=2)
        ttk.Label(grid_size_frame, text="Grid Size:").pack(side='left')
        self.property_widgets['grid_size'] = ttk.Entry(grid_size_frame, width=8)
        self.property_widgets['grid_size'].pack(side='left', padx=2)
        self.property_widgets['grid_size'].bind('<Return>', self._on_property_change)
        self.property_widgets['grid_size'].bind('<FocusOut>', self._on_property_change)
        
        # Apply Button
        ttk.Separator(self.frame, orient='horizontal').pack(fill='x', pady=10)
        apply_frame = ttk.Frame(self.frame)
        apply_frame.pack(fill='x', pady=5)
        ttk.Button(apply_frame, text="Apply Changes", command=self._apply_changes).pack(pady=5)
        
        # Reset Button
        ttk.Button(apply_frame, text="Reset to Default", command=self._reset_to_default).pack(pady=2)
    
    def _choose_background_color(self, event=None):
        """Open color chooser for background color"""
        color = colorchooser.askcolor(
            initialcolor=self.gui_properties.background_color,
            title="Choose Background Color"
        )
        
        if color[1]:  # color[1] is the hex color string
            self.gui_properties.background_color = color[1]
            self._update_color_display()
            self._on_property_change()
    
    def _update_color_display(self):
        """Update the color display widget"""
        self.property_widgets['background_color'].configure(bg=self.gui_properties.background_color)
    
    def _on_property_change(self, event=None):
        """Handle property change"""
        try:
            # Update GUI properties from widgets
            self.gui_properties.title = self.property_widgets['title'].get()
            self.gui_properties.width = int(self.property_widgets['width'].get())
            self.gui_properties.height = int(self.property_widgets['height'].get())
            self.gui_properties.grid_size = int(self.property_widgets['grid_size'].get())
            self.gui_properties.show_grid = self.property_widgets['show_grid'].get()
            
            # Call the callback to notify of changes
            if self.on_change_callback:
                self.on_change_callback(self.gui_properties)
                
        except ValueError:
            # Handle invalid numeric input gracefully
            pass
    
    def _apply_changes(self):
        """Apply all current changes"""
        self._on_property_change()
    
    def _reset_to_default(self):
        """Reset all properties to default values"""
        self.gui_properties.__init__()  # Reset to defaults
        self.update_widgets()
        if self.on_change_callback:
            self.on_change_callback(self.gui_properties)
    
    def update_widgets(self):
        """Update widget values from GUI properties"""
        self.property_widgets['title'].delete(0, tk.END)
        self.property_widgets['title'].insert(0, self.gui_properties.title)
        
        self.property_widgets['width'].delete(0, tk.END)
        self.property_widgets['width'].insert(0, str(self.gui_properties.width))
        
        self.property_widgets['height'].delete(0, tk.END)
        self.property_widgets['height'].insert(0, str(self.gui_properties.height))
        
        self.property_widgets['grid_size'].delete(0, tk.END)
        self.property_widgets['grid_size'].insert(0, str(self.gui_properties.grid_size))
        
        self.property_widgets['show_grid'].set(self.gui_properties.show_grid)
        
        self._update_color_display()
