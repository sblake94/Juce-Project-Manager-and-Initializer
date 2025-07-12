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
    from .code_generator import CodeGenerator
    from .file_manager import FileManager
    from .panels.gui_properties import GUIProperties, GUIPropertiesPanel
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
            self.root.geometry("1200x800")
            
            # Initialize GUI properties
            self.gui_properties = GUIProperties()
            
            # Initialize status variable first
            self.status_var = tk.StringVar()
            self.status_var.set("Ready")
            self.filename = None
            
            self.juce_target_dir = juce_target_dir
            
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
        
        # Left side - toolbox
        self.toolbox = ComponentToolbox(main_frame)
        
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
        
        # Right side - dynamic properties panel container
        properties_container = ttk.Frame(main_frame)
        properties_container.pack(side='right', fill='y', padx=5)
        
        # Create both panels but initially show only GUI properties
        self.gui_properties_panel = GUIPropertiesPanel(
            properties_container, 
            self.gui_properties, 
            self.on_gui_properties_changed
        )
        
        self.properties = PropertiesPanel(self, properties_container)
        
        # Initially show GUI properties panel and hide component properties
        self._show_gui_properties_panel()
        
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
            # Show component properties panel
            self._show_component_properties_panel()
            self.properties.update_properties(component)
            self.status_var.set(f"Selected: {component.type} - {component.text}")
        else:
            # Show GUI properties panel when no component is selected
            self._show_gui_properties_panel()
            self.status_var.set("No component selected - Showing GUI properties")
    
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
            
            # Reset GUI properties
            self.gui_properties = GUIProperties()
            self.gui_properties_panel.gui_properties = self.gui_properties
            self.gui_properties_panel.update_widgets()
            self._apply_gui_properties()
            
            # Show GUI properties panel since no components exist
            self._show_gui_properties_panel()
            
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
                components, width, height, gui_properties_data = FileManager.load_design(filename)
                
                # Clear current design
                self.canvas_frame.components.clear()
                self.canvas_frame.canvas.delete("all")
                
                # Load components
                self.canvas_frame.components = components
                
                # Load GUI properties
                if gui_properties_data:
                    self.gui_properties.from_dict(gui_properties_data)
                    self.gui_properties_panel.update_widgets()
                    self._apply_gui_properties()
                
                # Redraw all components
                self.canvas_frame.redraw_all()
                
                self.filename = filename
                self.root.title(f"Audio Plugin GUI Designer - {os.path.basename(filename)}")
                self.status_var.set(f"Loaded {len(self.canvas_frame.components)} components")
                
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
                self.gui_properties
            )
            
            self.status_var.set(f"Saved {len(self.canvas_frame.components)} components")
            
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
        if messagebox.askokcancel("Clear All", "Remove all components?"):
            self.canvas_frame.components.clear()
            self.canvas_frame.canvas.delete("all")
            self.canvas_frame.selected_component = None
            self.properties.clear_properties()
            # Show GUI properties panel since no components remain
            self._show_gui_properties_panel()
            self.status_var.set("All components cleared")
    
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
        self._show_gui_properties_panel()
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

    def _show_gui_properties_panel(self):
        """Show GUI properties panel and hide component properties panel"""
        self.gui_properties_panel.frame.pack(side='right', fill='y', padx=5, pady=5)
        self.properties.frame.pack_forget()
    
    def _show_component_properties_panel(self):
        """Show component properties panel and hide GUI properties panel"""
        self.gui_properties_panel.frame.pack_forget()
        self.properties.frame.pack(side='right', fill='y', padx=5, pady=5)