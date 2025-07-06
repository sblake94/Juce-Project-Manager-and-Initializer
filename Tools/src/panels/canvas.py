#!/usr/bin/env python3
"""
Canvas widget for drag-and-drop component operations
"""

import tkinter as tk
import uuid
from typing import Dict, Optional
from ..components.component import Component
from ..components import create_component

class DragDropCanvas:
    """Canvas that supports drag and drop operations"""
    
    def __init__(self, parent, width=400, height=300, app=None):
        self.parent = parent
        self.app = app
        
        # Create the canvas with the specified size
        self.canvas = tk.Canvas(parent, width=width, height=height, bg='#F0F0F0', relief='sunken', bd=2)
        self.canvas.pack(expand=True)
        
        self.components: Dict[str, Component] = {}
        self.selected_component: Optional[str] = None
        self.drag_data = {"x": 0, "y": 0, "item": None}
        
        self._setup_events()
        self._setup_context_menu()
        
    def _setup_events(self):
        """Setup mouse and keyboard event bindings"""
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Double-Button-1>", self.on_double_click)
        self.canvas.bind("<Button-3>", self.show_context_menu)
        
    def _setup_context_menu(self):
        """Setup right-click context menu"""
        self.context_menu = tk.Menu(self.canvas, tearoff=0)
        self.context_menu.add_command(label="Delete", command=self.delete_selected)
        self.context_menu.add_command(label="Duplicate", command=self.duplicate_selected)
        self.context_menu.add_command(label="Properties", command=self.show_properties)
        
    def add_component(self, comp_type: str, x: int, y: int):
        """Add a new component to the canvas"""
        comp_id = str(uuid.uuid4())
        text = f"{comp_type.title()} {len(self.components) + 1}"
        
        # Use factory function to create the appropriate component
        component = create_component(comp_type, comp_id, x, y, text)
        
        self.components[comp_id] = component
        self.draw_component(component)
        self.select_component(comp_id)
        
    def draw_component(self, component: Component):
        """Draw a component on the canvas"""
        # Clear existing drawing for this component including selection highlight
        self.canvas.delete(f"comp_{component.id}")
        self.canvas.delete(f"comp_{component.id}_select")

        # Use the component's own draw method
        component.draw(self.canvas)
        
        # Draw text label (handled by base class method)
        component.draw_text_label(self.canvas)
        
        # Draw selection highlight if selected
        if self.selected_component == component.id:
            component.draw_selection_highlight(self.canvas)
    
    def draw_grid(self, show_grid: bool, grid_size: int = 10):
        """Draw or remove grid lines on the canvas"""
        # Remove existing grid
        self.canvas.delete("grid")
        
        if not show_grid:
            return
        
        # Get canvas dimensions
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        # Draw vertical lines
        for x in range(0, width, grid_size):
            self.canvas.create_line(x, 0, x, height, fill="#E0E0E0", tags="grid")
        
        # Draw horizontal lines
        for y in range(0, height, grid_size):
            self.canvas.create_line(0, y, width, y, fill="#E0E0E0", tags="grid")
        
        # Send grid to back
        self.canvas.tag_lower("grid")
    
    def redraw_all(self):
        """Redraw all components"""
        for component in self.components.values():
            self.draw_component(component)
    
    def on_click(self, event):
        """Handle mouse click"""
        item = self.canvas.find_closest(event.x, event.y)[0]
        
        # Find which component was clicked
        tags = self.canvas.gettags(item)
        clicked_comp = None
        for comp_id in self.components:
            if f"comp_{comp_id}" in tags or f"comp_{comp_id}_select" in tags:
                clicked_comp = comp_id
                break
        
        if clicked_comp:
            self.select_component(clicked_comp)
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
            self.drag_data["item"] = clicked_comp
        else:
            self.select_component(None)
    
    def on_drag(self, event):
        """Handle dragging"""
        if self.drag_data["item"]:
            comp_id = self.drag_data["item"]
            component = self.components[comp_id]
            
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            
            component.x += dx
            component.y += dy
            
            # Keep within canvas bounds
            component.x = max(0, min(component.x, self.canvas.winfo_width() - component.width))
            component.y = max(0, min(component.y, self.canvas.winfo_height() - component.height))
            
            self.draw_component(component)
            
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
    
    def on_release(self, event):
        """Handle mouse release"""
        # If we were dragging a component, update the properties panel
        if self.drag_data["item"] and self.selected_component:
            component = self.components[self.selected_component]
            # Notify parent about property changes
            if self.app and hasattr(self.app, 'on_component_selected'):
                self.app.on_component_selected(component)
        
        self.drag_data["item"] = None
    
    def on_double_click(self, event):
        """Handle double click to show properties"""
        if self.selected_component:
            self.show_properties()
    
    def select_component(self, comp_id: Optional[str]):
        """Select a component"""
        if self.selected_component:
            # Remove previous selection highlight
            self.canvas.delete(f"comp_{self.selected_component}_select")
        
        self.selected_component = comp_id
        
        if comp_id:
            component = self.components[comp_id]
            self.draw_component(component)
            # Notify parent about selection change
            if self.app and hasattr(self.app, 'on_component_selected'):
                self.app.on_component_selected(component)
        else:
            # No component selected - notify parent with None
            if self.app and hasattr(self.app, 'on_component_selected'):
                self.app.on_component_selected(None)
    
    def show_context_menu(self, event):
        """Show context menu"""
        if self.selected_component:
            self.context_menu.post(event.x_root, event.y_root)
    
    def delete_selected(self):
        """Delete selected component"""
        if self.selected_component:
            self.canvas.delete(f"comp_{self.selected_component}")
            self.canvas.delete(f"comp_{self.selected_component}_select")
            del self.components[self.selected_component]
            self.selected_component = None
    
    def duplicate_selected(self):
        """Duplicate selected component"""
        if self.selected_component:
            component = self.components[self.selected_component]
            self.add_component(component.type, component.x + 20, component.y + 20)
    
    def show_properties(self):
        """Show properties dialog for selected component"""
        if self.selected_component and hasattr(self.parent.master, 'show_properties_dialog'):
            self.parent.master.show_properties_dialog(self.components[self.selected_component])
    
    def update_canvas_size(self, width: int, height: int):
        """Update canvas size"""
        self.canvas.configure(width=width, height=height)
