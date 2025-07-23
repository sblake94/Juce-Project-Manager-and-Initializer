#!/usr/bin/env python3
"""
Audio Plugin GUI Designer
A drag-and-drop interface designer for audio plugins
"""

import os
import sys
import traceback
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Import our modules
try:
    from .code_writer import CodeWriter
    from .components.component import Component
    from .panels.canvas import DragDropCanvas
    from .panels.toolbox import ComponentToolbox
    from .panels.properties import PropertiesPanel
    from .panels.juce_toolbox import JUCEControlsToolbox, JUCEControlPropertiesPanel
    from .code_generator import CodeGenerator
    from .file_manager import FileManager
    from .panels.gui_properties import GUIProperties, GUIPropertiesPanel
    from .juce_controls import JUCEControl, JUCEControlFactory, JUCECodeGenerator
except ImportError as e:
    print(f"Import Error: {e}")
    print("Missing module files. Please ensure all required Python files exist.")
    input("Press Enter to exit...")
    exit(1)

class UIGeneratorApp:
    """Main application class"""

    def __init__(self, juce_target_dir: str):
        try:
            self.root = tk.Tk()
            self.root.title("Audio Plugin GUI Designer")
            self.root.geometry("1400x900")  # Increased width for JUCE controls panel
            
            # Initialize GUI properties
            self.gui_properties = GUIProperties()
            
            # Initialize status variable first
            self.status_var = tk.StringVar()
            self.status_var.set("Ready")
            self.filename = None
            
            self.juce_target_dir = juce_target_dir
            
            # Initialize JUCE controls list
            self.juce_controls = []
            
            self._create_menu()
            self._create_layout()
            self._create_status_bar()
        except Exception as e:
            print(f"Initialization Error: {e}")
            traceback.print_exc()
            input("Press Enter to exit...")
            exit(1)
    
    def _create_menu(self):
        """Create application menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Export Code", command=self.export_code)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Clear All", command=self.clear_all)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Reset Canvas Size", command=self.reset_canvas_size)
        view_menu.add_separator()
        view_menu.add_checkbutton(label="Show Grid", command=self.toggle_grid)
        view_menu.add_separator()
        view_menu.add_command(label="GUI Properties", command=self.focus_gui_properties)
        view_menu.add_command(label="JUCE Controls", command=self.focus_juce_controls)
        
        # JUCE menu
        juce_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="JUCE", menu=juce_menu)
        juce_menu.add_command(label="Export JUCE Code", command=self.export_juce_code)
        juce_menu.add_command(label="Clear JUCE Controls", command=self.clear_juce_controls)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.new_file())
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-S>', lambda e: self.save_as_file())
    
    def _create_layout(self):
        """Create main application layout"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Left side - toolboxes in a notebook (tabs)
        left_panel = ttk.Notebook(main_frame)
        left_panel.pack(side='left', fill='y', padx=(0, 5))
        
        # Original UI components toolbox
        ui_toolbox_frame = ttk.Frame(left_panel)
        self.toolbox = ComponentToolbox(ui_toolbox_frame)
        left_panel.add(ui_toolbox_frame, text="UI Components")
        
        # JUCE controls toolbox  
        juce_toolbox_frame = ttk.Frame(left_panel)
        self.juce_toolbox = JUCEControlsToolbox(juce_toolbox_frame, self.on_juce_control_selected)
        self.juce_toolbox.pack(fill="both", expand=True)
        left_panel.add(juce_toolbox_frame, text="JUCE Controls")
        
        # Center - canvas
        canvas_container = ttk.Frame(main_frame)
        canvas_container.pack(side='left', fill='both', expand=True, padx=5)
        
        canvas_frame = ttk.Frame(canvas_container)
        canvas_frame.pack(fill='both', expand=True)
        
        self.canvas_frame = DragDropCanvas(canvas_frame, 
                                         self.gui_properties.width, 
                                         self.gui_properties.height, 
                                         self)
        
        # Set canvas reference in toolbox
        self.toolbox.canvas = self.canvas_frame
        
        # Right side - properties panels in a notebook (tabs)
        right_panel = ttk.Notebook(main_frame)
        right_panel.pack(side='right', fill='y', padx=(5, 0))
        
        # GUI properties panel
        gui_props_frame = ttk.Frame(right_panel)
        self.gui_properties_panel = GUIPropertiesPanel(
            gui_props_frame, 
            self.gui_properties, 
            self.on_gui_properties_changed
        )
        right_panel.add(gui_props_frame, text="GUI Properties")
        
        # Component properties panel
        comp_props_frame = ttk.Frame(right_panel)
        self.properties = PropertiesPanel(self, comp_props_frame)
        right_panel.add(comp_props_frame, text="Component Props")
        
        # JUCE control properties panel
        juce_props_frame = ttk.Frame(right_panel)
        self.juce_properties = JUCEControlPropertiesPanel(juce_props_frame)
        right_panel.add(juce_props_frame, text="JUCE Props")
        
        # Update canvas with initial GUI properties
        self._apply_gui_properties()
        
        # Update status
        self.status_var.set("GUI Designer ready - Add components from the toolbox")
    
    def _create_status_bar(self):
        """Create status bar"""
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief='sunken')
        self.status_bar.pack(side='bottom', fill='x')
    
    def on_component_selected(self, component: Component):
        """Handle component selection"""
        if component:
            self.properties.update_properties(component)
            self.status_var.set(f"Selected: {component.type} - {component.text}")
        else:
            self.status_var.set("No component selected")
    
    def show_properties_dialog(self, component: Component):
        """Show properties dialog (for double-click)"""
        # The properties panel already shows the properties
        pass
    
    def new_file(self):
        """Create new file"""
        if messagebox.askokcancel(title="New File", message="Clear current design?", options={ "default": True }):
            self.canvas_frame.components.clear()
            self.canvas_frame.canvas.delete("all")
            self.canvas_frame.selected_component = None
            self.properties.clear_properties()
            
            # Clear JUCE controls
            self.juce_controls.clear()
            self.juce_properties.update_properties(None)
            
            # Reset GUI properties
            self.gui_properties = GUIProperties()
            self.gui_properties_panel.gui_properties = self.gui_properties
            self.gui_properties_panel.update_widgets()
            self._apply_gui_properties()
            
            self.filename = None
            self.root.title("Audio Plugin GUI Designer - Untitled")
            self.status_var.set("New file created")
    
    def open_file(self):
        """Open design file"""
        filename = filedialog.askopenfilename(
            title="Open GUI Design",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                components, width, height, gui_properties_data, juce_controls = FileManager.load_design(filename)
                
                # Clear current design
                self.canvas_frame.components.clear()
                self.canvas_frame.canvas.delete("all")
                
                # Load components
                self.canvas_frame.components = components
                
                # Load JUCE controls
                self.juce_controls = juce_controls
                for control in self.juce_controls:
                    self._draw_juce_control_on_canvas(control)
                
                # Load GUI properties
                if gui_properties_data:
                    self.gui_properties.from_dict(gui_properties_data)
                    self.gui_properties_panel.update_widgets()
                    self._apply_gui_properties()
                
                # Redraw all components
                self.canvas_frame.redraw_all()
                
                self.filename = filename
                self.root.title(f"Audio Plugin GUI Designer - {os.path.basename(filename)}")
                self.status_var.set(f"Loaded {len(self.canvas_frame.components)} components and {len(self.juce_controls)} JUCE controls")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {str(e)}")
    
    def save_file(self):
        """Save current design"""
        if self.filename:
            self._save_to_file(self.filename)
        else:
            self.save_as_file()
    
    def save_as_file(self):
        """Save design as new file"""
        filename = filedialog.asksaveasfilename(
            title="Save GUI Design",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            self._save_to_file(filename)
            self.filename = filename
            self.root.title(f"Audio Plugin GUI Designer - {os.path.basename(filename)}")
    
    def _save_to_file(self, filename: str):
        """Save design to file"""
        try:
            # Get the actual drawing area size by subtracting total widget padding
            # The canvas widget includes border (bd=2) plus additional internal padding
            canvas_widget_width = self.canvas_frame.canvas.winfo_width()
            canvas_widget_height = self.canvas_frame.canvas.winfo_height()
            
            # Empirical observation: widget reports 4px larger than intended canvas size
            # Need to subtract 8px per dimension to get correct size (double the observed offset)
            total_offset = 8
            actual_drawing_width = canvas_widget_width - total_offset
            actual_drawing_height = canvas_widget_height - total_offset
            
            FileManager.save_design(
                filename, 
                self.canvas_frame.components,
                actual_drawing_width,
                actual_drawing_height,
                self.gui_properties,
                self.juce_controls
            )
            
            self.status_var.set(f"Saved {len(self.canvas_frame.components)} components and {len(self.juce_controls)} JUCE controls")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def export_code(self):
        """Export as code"""
        if not self.canvas_frame.components:
            messagebox.showwarning("Warning", "No components to export")
            return
        
        self._show_export_dialog()
    
    def _get_juce_target_directory(self) -> str:
        """Get target directory for JUCE code export"""
        if self.juce_target_dir:
            return self.juce_target_dir
        return filedialog.askdirectory(
            title="Select JUCE Target Directory",
            mustexist=True
        )

    def _show_export_dialog(self):
        """Show export dialog"""
        export_window = tk.Toplevel(self.root)
        export_window.title("Export Code")
        export_window.geometry("600x400")
        
        # Format selection
        format_frame = ttk.Frame(export_window)
        format_frame.pack(fill='x', padx=10, pady=5)
        ttk.Label(format_frame, text="Export Format:").pack(side='left')
        
        format_var = tk.StringVar(value="JUCE")
        format_combo = ttk.Combobox(format_frame, textvariable=format_var, 
                                   values=["JUCE", "VST3", "Generic XML", "JSON"])
        format_combo.pack(side='left', padx=5)
        
        # Code display
        code_text = tk.Text(export_window, wrap='none')
        scrollbar_y = ttk.Scrollbar(export_window, orient='vertical', command=code_text.yview)
        scrollbar_x = ttk.Scrollbar(export_window, orient='horizontal', command=code_text.xview)
        code_text.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        code_text.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=5)
        scrollbar_y.pack(side='right', fill='y', pady=5)
        scrollbar_x.pack(side='bottom', fill='x', padx=10)
        
        def update_code():
            format_type = format_var.get()
            # Get the actual drawing area size by subtracting total widget padding
            # The canvas widget includes border (bd=2) plus additional internal padding
            canvas_widget_width = self.canvas_frame.canvas.winfo_width()
            canvas_widget_height = self.canvas_frame.canvas.winfo_height()
            
            # Empirical observation: widget reports 4px larger than intended canvas size
            # Need to subtract 8px per dimension to get correct size (double the observed offset)
            total_offset = 8  
            actual_drawing_width = canvas_widget_width - total_offset
            actual_drawing_height = canvas_widget_height - total_offset
            
            # Debug output (temporary)
            print(f"DEBUG: Widget size: {canvas_widget_width}x{canvas_widget_height}")
            print(f"DEBUG: Drawing area: {actual_drawing_width}x{actual_drawing_height}")
            
            generator = CodeGenerator(
                self.canvas_frame.components,
                actual_drawing_width,
                actual_drawing_height,
                self.gui_properties.background_color,
            )
            
            if format_type == "JUCE":
                juce_output = generator.generate_juce_code()
                code_writer = CodeWriter()
                target_directory = self._get_juce_target_directory()
                code_writer.write_code(juce_output, target_directory)
                code = juce_output.get_formatted_output()
            elif format_type == "JSON":
                code = generator.generate_json_code()
            elif format_type == "Generic XML":
                code = generator.generate_xml_code()
            else:
                code = f"// Code generation for {format_type} not implemented yet\n"
                
            code_text.delete(1.0, tk.END)
            code_text.insert(1.0, code)
        
        format_combo.bind('<<ComboboxSelected>>', lambda e: update_code())
        update_code()  # Initial load
        
        # Buttons
        btn_frame = ttk.Frame(export_window)
        btn_frame.pack(fill='x', padx=10, pady=5)
        ttk.Button(btn_frame, text="Save to File", 
                  command=lambda: self._save_code(code_text.get(1.0, tk.END))).pack(side='right', padx=5)
        ttk.Button(btn_frame, text="Copy to Clipboard", 
                  command=lambda: self._copy_to_clipboard(code_text.get(1.0, tk.END))).pack(side='right')
    
    

    def _save_code(self, code: str):
        """Save generated code to file"""
        filename = filedialog.asksaveasfilename(
            title="Save Generated Code",
            filetypes=[("C++ files", "*.cpp"), ("Header files", "*.h"), 
                      ("JSON files", "*.json"), ("XML files", "*.xml"), 
                      ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                FileManager.save_code(filename, code)
                self.status_var.set(f"Code exported to {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save code: {str(e)}")
    
    def _copy_to_clipboard(self, text: str):
        """Copy text to clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status_var.set("Code copied to clipboard")
    
    def clear_all(self):
        """Clear all components"""
        if messagebox.askokcancel("Clear All", "Remove all components and JUCE controls?"):
            self.canvas_frame.components.clear()
            self.canvas_frame.canvas.delete("all")
            self.canvas_frame.selected_component = None
            self.properties.clear_properties()
            
            # Clear JUCE controls
            self.juce_controls.clear()
            self.juce_properties.update_properties(None)
            
            self.status_var.set("All components and JUCE controls cleared")
    
    def reset_canvas_size(self):
        """Reset canvas to default size"""
        self.canvas_frame.canvas.configure(width=400, height=300)
        self.status_var.set("Canvas size reset to 400x300")
    
    def toggle_grid(self):
        """Toggle grid display"""
        self.gui_properties.show_grid = not self.gui_properties.show_grid
        self.gui_properties_panel.update_widgets()
        self._apply_gui_properties()
        self.status_var.set(f"Grid {'enabled' if self.gui_properties.show_grid else 'disabled'}")
    
    def focus_gui_properties(self):
        """Focus on GUI properties panel"""
        # Clear any component selection and show GUI properties
        self.canvas_frame.select_component(None)
        self.status_var.set("Showing GUI properties panel")
    
    def on_gui_properties_changed(self, gui_properties: 'GUIProperties'):
        """Handle changes to GUI properties"""
        self._apply_gui_properties()
        self.status_var.set("GUI properties updated")
    
    def _apply_gui_properties(self):
        """Apply GUI properties to the canvas and interface"""
        # Update canvas background color
        self.canvas_frame.canvas.configure(bg=self.gui_properties.background_color)
        
        # Update canvas size using the new method
        print(f"Updating canvas size to {self.gui_properties.width}x{self.gui_properties.height}")  # Debug
        self.canvas_frame.update_canvas_size(self.gui_properties.width, self.gui_properties.height)
        
        # Update window title
        title = f"Audio Plugin GUI Designer - {self.gui_properties.title}"
        if self.filename:
            title += f" - {os.path.basename(self.filename)}"
        self.root.title(title)
        
        # Redraw grid if enabled
        if hasattr(self.canvas_frame, 'draw_grid'):
            self.canvas_frame.draw_grid(self.gui_properties.show_grid, self.gui_properties.grid_size)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()
    
    # JUCE Controls Methods
    def on_juce_control_selected(self, control_type: str, config: dict):
        """Handle JUCE control selection from toolbox"""
        try:
            # Create JUCE control
            control = JUCEControlFactory.create_control(
                control_type=control_type,
                **config
            )
            
            # Add to controls list
            self.juce_controls.append(control)
            
            # Visualize on canvas (simple rectangle for now)
            self._draw_juce_control_on_canvas(control)
            
            # Update properties panel
            self.juce_properties.update_properties(control)
            
            self.status_var.set(f"Added JUCE {control_type}: {control.name}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add JUCE control: {e}")
    
    def _draw_juce_control_on_canvas(self, control: JUCEControl):
        """Draw a visual representation of the JUCE control on canvas"""
        # Color coding for different control types
        colors = {
            "slider": "#4CAF50",    # Green
            "button": "#2196F3",    # Blue
            "label": "#FF9800",     # Orange
            "combobox": "#9C27B0"   # Purple
        }
        
        color = colors.get(control.control_type, "#607D8B")
        
        # Draw rectangle
        rect_id = self.canvas_frame.canvas.create_rectangle(
            control.x, control.y,
            control.x + control.width, control.y + control.height,
            fill=color, outline="black", width=2,
            tags=("juce_control", f"juce_{id(control)}")
        )
        
        # Draw text label
        text_id = self.canvas_frame.canvas.create_text(
            control.x + control.width // 2,
            control.y + control.height // 2,
            text=f"{control.control_type}\n{control.name}",
            fill="white", font=("TkDefaultFont", 8, "bold"),
            tags=("juce_control", f"juce_{id(control)}")
        )
        
        # Bind click events
        self.canvas_frame.canvas.tag_bind(f"juce_{id(control)}", "<Button-1>", 
                                        lambda e: self.on_juce_control_clicked(control))
    
    def on_juce_control_clicked(self, control: JUCEControl):
        """Handle clicking on a JUCE control"""
        # Clear any component selection
        self.canvas_frame.select_component(None)
        
        # Update JUCE properties panel
        self.juce_properties.update_properties(control)
        
        self.status_var.set(f"Selected JUCE {control.control_type}: {control.name}")
    
    def focus_juce_controls(self):
        """Focus on JUCE controls tab"""
        self.status_var.set("Showing JUCE controls toolbox")
    
    def export_juce_code(self):
        """Export JUCE code for all controls"""
        if not self.juce_controls:
            messagebox.showwarning("Warning", "No JUCE controls to export")
            return
        
        try:
            generator = JUCECodeGenerator(self.juce_controls)
            
            # Create export dialog
            export_window = tk.Toplevel(self.root)
            export_window.title("Export JUCE Code")
            export_window.geometry("800x600")
            
            # Create notebook for different code sections
            notebook = ttk.Notebook(export_window)
            notebook.pack(fill='both', expand=True, padx=10, pady=10)
            
            # Header declarations
            header_frame = ttk.Frame(notebook)
            header_text = tk.Text(header_frame, wrap='none')
            header_scrollbar_y = ttk.Scrollbar(header_frame, orient='vertical', command=header_text.yview)
            header_scrollbar_x = ttk.Scrollbar(header_frame, orient='horizontal', command=header_text.xview)
            header_text.configure(yscrollcommand=header_scrollbar_y.set, xscrollcommand=header_scrollbar_x.set)
            
            header_text.insert(1.0, generator.generate_header_declarations())
            header_text.pack(side='left', fill='both', expand=True)
            header_scrollbar_y.pack(side='right', fill='y')
            header_scrollbar_x.pack(side='bottom', fill='x')
            notebook.add(header_frame, text="Header (.h)")
            
            # Constructor code
            constructor_frame = ttk.Frame(notebook)
            constructor_text = tk.Text(constructor_frame, wrap='none')
            constructor_scrollbar_y = ttk.Scrollbar(constructor_frame, orient='vertical', command=constructor_text.yview)
            constructor_scrollbar_x = ttk.Scrollbar(constructor_frame, orient='horizontal', command=constructor_text.xview)
            constructor_text.configure(yscrollcommand=constructor_scrollbar_y.set, xscrollcommand=constructor_scrollbar_x.set)
            
            constructor_text.insert(1.0, generator.generate_constructor_code())
            constructor_text.pack(side='left', fill='both', expand=True)
            constructor_scrollbar_y.pack(side='right', fill='y')
            constructor_scrollbar_x.pack(side='bottom', fill='x')
            notebook.add(constructor_frame, text="Constructor (.cpp)")
            
            # Resized method
            resized_frame = ttk.Frame(notebook)
            resized_text = tk.Text(resized_frame, wrap='none')
            resized_scrollbar_y = ttk.Scrollbar(resized_frame, orient='vertical', command=resized_text.yview)
            resized_scrollbar_x = ttk.Scrollbar(resized_frame, orient='horizontal', command=resized_text.xview)
            resized_text.configure(yscrollcommand=resized_scrollbar_y.set, xscrollcommand=resized_scrollbar_x.set)
            
            resized_text.insert(1.0, generator.generate_resized_code())
            resized_text.pack(side='left', fill='both', expand=True)
            resized_scrollbar_y.pack(side='right', fill='y')
            resized_scrollbar_x.pack(side='bottom', fill='x')
            notebook.add(resized_frame, text="resized() Method")
            
            # Parameter layout
            params_frame = ttk.Frame(notebook)
            params_text = tk.Text(params_frame, wrap='none')
            params_scrollbar_y = ttk.Scrollbar(params_frame, orient='vertical', command=params_text.yview)
            params_scrollbar_x = ttk.Scrollbar(params_frame, orient='horizontal', command=params_text.xview)
            params_text.configure(yscrollcommand=params_scrollbar_y.set, xscrollcommand=params_scrollbar_x.set)
            
            params_code = generator.generate_parameter_layout()
            if params_code:
                params_text.insert(1.0, params_code)
            else:
                params_text.insert(1.0, "// No parameters to export")
            params_text.pack(side='left', fill='both', expand=True)
            params_scrollbar_y.pack(side='right', fill='y')
            params_scrollbar_x.pack(side='bottom', fill='x')
            notebook.add(params_frame, text="Parameters")
            
            # Buttons
            btn_frame = ttk.Frame(export_window)
            btn_frame.pack(fill='x', padx=10, pady=5)
            
            def save_to_files():
                """Save generated code to files"""
                target_dir = self.juce_target_dir
                if not target_dir:
                    target_dir = filedialog.askdirectory(title="Select JUCE Project Directory")
                    if not target_dir:
                        return
                
                try:
                    # Save to PluginEditor.h and PluginEditor.cpp
                    header_file = os.path.join(target_dir, "Source", "PluginEditor.h")
                    cpp_file = os.path.join(target_dir, "Source", "PluginEditor.cpp")
                    
                    messagebox.showinfo("Info", f"Code would be saved to:\n{header_file}\n{cpp_file}\n\n(Integration with existing files not implemented yet)")
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save files: {e}")
            
            ttk.Button(btn_frame, text="Save to Files", command=save_to_files).pack(side='right', padx=5)
            ttk.Button(btn_frame, text="Close", command=export_window.destroy).pack(side='right')
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export JUCE code: {e}")
    
    def clear_juce_controls(self):
        """Clear all JUCE controls"""
        if not self.juce_controls:
            messagebox.showinfo("Info", "No JUCE controls to clear")
            return
        
        if messagebox.askokcancel("Clear JUCE Controls", f"Remove all {len(self.juce_controls)} JUCE controls?"):
            # Clear from canvas
            self.canvas_frame.canvas.delete("juce_control")
            
            # Clear list
            self.juce_controls.clear()
            
            # Clear properties panel
            self.juce_properties.update_properties(None)
            
            self.status_var.set("All JUCE controls cleared")