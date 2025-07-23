#!/usr/bin/env python3
"""
JUCE Controls Toolbox
A toolbox panel for adding common JUCE audio plugin controls
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Optional, Callable, List
from ..juce_controls import JUCEControlFactory, COMMON_AUDIO_CONTROLS

class JUCEControlsToolbox:
    """Toolbox for JUCE audio plugin controls"""
    
    def __init__(self, parent: tk.Widget, on_control_selected: Optional[Callable] = None):
        self.parent = parent
        self.on_control_selected = on_control_selected
        self.frame = ttk.LabelFrame(parent, text="JUCE Controls", padding="5")
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the toolbox widgets"""
        # Instructions
        instructions = ttk.Label(
            self.frame, 
            text="Click to add JUCE audio controls:",
            font=("TkDefaultFont", 8)
        )
        instructions.pack(anchor="w", pady=(0, 5))
        
        # Create buttons for common controls
        self._create_control_buttons()
        
        # Separator
        separator = ttk.Separator(self.frame, orient="horizontal")
        separator.pack(fill="x", pady=5)
        
        # Custom control section
        custom_frame = ttk.Frame(self.frame)
        custom_frame.pack(fill="x", pady=2)
        
        ttk.Label(custom_frame, text="Custom:", font=("TkDefaultFont", 8)).pack(anchor="w")
        
        # Control type selection
        type_frame = ttk.Frame(self.frame)
        type_frame.pack(fill="x", pady=2)
        
        self.control_type_var = tk.StringVar(value="slider")
        type_combo = ttk.Combobox(
            type_frame,
            textvariable=self.control_type_var,
            values=JUCEControlFactory.get_available_types(),
            state="readonly",
            width=12
        )
        type_combo.pack(side="left", padx=(0, 5))
        
        add_custom_btn = ttk.Button(
            type_frame,
            text="+ Add",
            command=self._add_custom_control,
            width=8
        )
        add_custom_btn.pack(side="left")
    
    def _create_control_buttons(self):
        """Create buttons for common audio controls"""
        button_configs = [
            ("🎚️ Gain", "gain_slider", "Add gain/volume slider"),
            ("🎛️ Frequency", "frequency_slider", "Add frequency control knob"),
            ("⏯️ Bypass", "bypass_button", "Add bypass toggle button"),
            ("🔥 Drive", "drive_slider", "Add drive/saturation control"),
        ]
        
        for text, control_key, tooltip in button_configs:
            btn = ttk.Button(
                self.frame,
                text=text,
                command=lambda key=control_key: self._add_predefined_control(key),
                width=15
            )
            btn.pack(fill="x", pady=1)
            
            # Add tooltip (simplified - you could use a proper tooltip library)
            self._add_tooltip(btn, tooltip)
    
    def _add_tooltip(self, widget: tk.Widget, text: str):
        """Add a simple tooltip to a widget"""
        # Simplified - just bind for future use
        widget.bind("<Enter>", lambda e: None)
        widget.bind("<Leave>", lambda e: None)
    
    def _add_predefined_control(self, control_key: str):
        """Add a predefined control to the canvas"""
        if control_key not in COMMON_AUDIO_CONTROLS:
            messagebox.showerror("Error", f"Unknown control: {control_key}")
            return
        
        config = COMMON_AUDIO_CONTROLS[control_key].copy()
        control_type = config.pop("type")
        
        # Default position (center of canvas)
        config.setdefault("x", 200)
        config.setdefault("y", 150)
        
        if self.on_control_selected:
            self.on_control_selected(control_type, config)
    
    def _add_custom_control(self):
        """Add a custom control of the selected type"""
        control_type = self.control_type_var.get()
        width, height = JUCEControlFactory.get_default_size(control_type)
        
        config = {
            "name": f"Custom{control_type.title()}",
            "x": 200,
            "y": 150,
            "width": width,
            "height": height
        }
        
        if self.on_control_selected:
            self.on_control_selected(control_type, config)
    
    def pack(self, **kwargs):
        """Pack the toolbox frame"""
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the toolbox frame"""
        self.frame.grid(**kwargs)

class JUCEControlPropertiesPanel:
    """Properties panel for editing JUCE control properties"""
    
    def __init__(self, parent: tk.Widget):
        self.parent = parent
        self.current_control = None
        self.property_widgets = {}
        self.frame = ttk.LabelFrame(parent, text="JUCE Control Properties", padding="10")
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the properties panel widgets"""
        # Create a scrollable frame
        self.canvas = tk.Canvas(self.frame, height=400)
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Initial message
        self.no_selection_label = ttk.Label(
            self.scrollable_frame,
            text="Select a JUCE control to edit its properties",
            foreground="gray"
        )
        self.no_selection_label.pack(pady=20)
    
    def update_properties(self, control):
        """Update the properties panel for the given control"""
        self.current_control = control
        
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.property_widgets.clear()
        
        if control is None:
            self.no_selection_label = ttk.Label(
                self.scrollable_frame,
                text="Select a JUCE control to edit its properties",
                foreground="gray"
            )
            self.no_selection_label.pack(pady=20)
            return
        
        # Title
        title_label = ttk.Label(
            self.scrollable_frame,
            text=f"{control.control_type.title()} Properties",
            font=("TkDefaultFont", 10, "bold")
        )
        title_label.pack(anchor="w", pady=(0, 10))
        
        # Common properties
        self._add_property("Name", control.name, "string")
        self._add_property("X Position", control.x, "int")
        self._add_property("Y Position", control.y, "int")
        self._add_property("Width", control.width, "int")
        self._add_property("Height", control.height, "int")
        
        # Control-specific properties
        if hasattr(control, 'parameter_id'):
            self._add_property("Parameter ID", control.parameter_id, "string")
        
        if control.control_type == "slider":
            self._add_separator("Slider Settings")
            self._add_property("Min Value", control.min_value, "float")
            self._add_property("Max Value", control.max_value, "float")
            self._add_property("Default Value", control.default_value, "float")
            self._add_property("Step Size", control.step_size, "float")
            self._add_property("Suffix", control.suffix, "string")
            self._add_property("Slider Style", control.slider_style, "combo", 
                             ["LinearHorizontal", "LinearVertical", "Rotary", "RotaryHorizontalDrag"])
            self._add_property("Text Box Style", control.text_box_style, "combo",
                             ["TextBoxBelow", "TextBoxAbove", "TextBoxLeft", "TextBoxRight", "NoTextBox"])
        
        elif control.control_type == "button":
            self._add_separator("Button Settings")
            self._add_property("Button Text", control.button_text, "string")
            self._add_property("Button Type", control.button_type, "combo",
                             ["TextButton", "ToggleButton"])
            if control.button_type == "ToggleButton":
                self._add_property("Toggle State", control.toggle_state, "bool")
        
        elif control.control_type == "label":
            self._add_separator("Label Settings")
            self._add_property("Text", control.text, "string")
            self._add_property("Font Size", control.font_size, "float")
            self._add_property("Justification", control.justification, "combo",
                             ["left", "right", "centred", "centredLeft", "centredRight"])
            self._add_property("Editable", control.editable, "bool")
        
        elif control.control_type == "combobox":
            self._add_separator("ComboBox Settings")
            self._add_property("Items", ", ".join(control.items), "string")
            self._add_property("Default Index", control.default_index, "int")
        
        # Update button
        update_btn = ttk.Button(
            self.scrollable_frame,
            text="Apply Changes",
            command=self._apply_changes
        )
        update_btn.pack(pady=(10, 0))
    
    def _add_separator(self, text: str):
        """Add a separator with text"""
        sep_frame = ttk.Frame(self.scrollable_frame)
        sep_frame.pack(fill="x", pady=(10, 5))
        
        ttk.Label(sep_frame, text=text, font=("TkDefaultFont", 9, "bold")).pack(anchor="w")
        ttk.Separator(sep_frame, orient="horizontal").pack(fill="x", pady=(2, 0))
    
    def _add_property(self, label: str, value: Any, prop_type: str, options: Optional[List[str]] = None):
        """Add a property editor widget"""
        frame = ttk.Frame(self.scrollable_frame)
        frame.pack(fill="x", pady=2)
        
        ttk.Label(frame, text=f"{label}:", width=12).pack(side="left", anchor="w")
        
        if prop_type == "string":
            widget = ttk.Entry(frame, width=20)
            widget.insert(0, str(value))
        elif prop_type == "int":
            widget = ttk.Entry(frame, width=20)
            widget.insert(0, str(value))
        elif prop_type == "float":
            widget = ttk.Entry(frame, width=20)
            widget.insert(0, str(value))
        elif prop_type == "bool":
            var = tk.BooleanVar(value=value)
            widget = ttk.Checkbutton(frame, variable=var)
            # Store the variable reference for later access
            setattr(widget, '_bool_var', var)
        elif prop_type == "combo":
            widget = ttk.Combobox(frame, values=options or [], state="readonly", width=17)
            widget.set(str(value))
        else:
            widget = ttk.Entry(frame, width=20)
            widget.insert(0, str(value))
        
        widget.pack(side="left", padx=(5, 0))
        self.property_widgets[label.lower().replace(" ", "_")] = (widget, prop_type)
    
    def _apply_changes(self):
        """Apply changes from the property widgets to the control"""
        if not self.current_control:
            return
        
        try:
            # Update properties from widgets
            for prop_name, (widget, prop_type) in self.property_widgets.items():
                if prop_type == "bool":
                    value = getattr(widget, '_bool_var').get()
                elif prop_type == "int":
                    value = int(widget.get())
                elif prop_type == "float":
                    value = float(widget.get())
                elif prop_name == "items":  # Special case for combobox items
                    value = [item.strip() for item in widget.get().split(",")]
                else:
                    value = widget.get()
                
                # Map property names to control attributes
                attr_name = self._map_property_name(prop_name)
                if hasattr(self.current_control, attr_name):
                    setattr(self.current_control, attr_name, value)
            
            # Notify that properties have changed (you might want to add a callback here)
            messagebox.showinfo("Success", "Properties updated successfully!")
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid value: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update properties: {e}")
    
    def _map_property_name(self, prop_name: str) -> str:
        """Map property display names to control attribute names"""
        mapping = {
            "name": "name",
            "x_position": "x",
            "y_position": "y", 
            "width": "width",
            "height": "height",
            "parameter_id": "parameter_id",
            "min_value": "min_value",
            "max_value": "max_value",
            "default_value": "default_value",
            "step_size": "step_size",
            "suffix": "suffix",
            "slider_style": "slider_style",
            "text_box_style": "text_box_style",
            "button_text": "button_text",
            "button_type": "button_type",
            "toggle_state": "toggle_state",
            "text": "text",
            "font_size": "font_size",
            "justification": "justification",
            "editable": "editable",
            "items": "items",
            "default_index": "default_index"
        }
        return mapping.get(prop_name, prop_name)
    
    def pack(self, **kwargs):
        """Pack the properties panel frame"""
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the properties panel frame"""
        self.frame.grid(**kwargs)
