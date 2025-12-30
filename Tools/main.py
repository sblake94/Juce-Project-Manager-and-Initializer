import os
import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import traceback
import re
from typing import Dict, Any, List, Tuple
from src.UIGeneratorApp import UIGeneratorApp

# ---------------------------------------------------------------------------
# Configurable paths
# ---------------------------------------------------------------------------
# Users can override these defaults by exporting environment variables before
# launching the tool:
#   TEMPLATE_SRC_DIR – absolute path to the template CMake project
#   TEMPLATE_DST_DIR – absolute path where new projects will be created
# These fall back to the original hard-coded Windows paths to preserve
# behavior for existing users. Paths are normalized for cross-platform use.

DEFAULT_SRC = r"D:/Dev/Visual Studio Projects/AudioPlugins/MyAwesomePluginCompany/Template/MyCMakeProject"
DEFAULT_DST = r"D:/Dev/Visual Studio Projects/AudioPlugins/MyAwesomePluginCompany/MyAwesomePlugins"

SRC_DIR = os.path.normpath(os.getenv("TEMPLATE_SRC_DIR", DEFAULT_SRC))
DST_DIR = os.path.normpath(os.getenv("TEMPLATE_DST_DIR", DEFAULT_DST))

# The template name to replace in files and filenames
TEMPLATE_NAME = "MyCMakeProject"

def cmake_ready(build_dir: str) -> bool:
    """Check if CMake has been run successfully by looking for CMakeCache.txt."""
    cmake_cache = os.path.join(build_dir, "out", "build", "x64-Debug", "CMakeCache.txt")
    ## make sure cmake_cache uses consistent path separators
    cmake_cache = os.path.normpath(cmake_cache)
    return os.path.isfile(cmake_cache)

def scan_existing_projects() -> List[Tuple[str, str]]:
    """Scan the DST_DIR for existing plugin projects."""
    projects = []
    
    if not os.path.exists(DST_DIR):
        return projects
    
    try:
        for item in os.listdir(DST_DIR):
            project_path = os.path.join(DST_DIR, item)
            
            # Check if it's a directory and contains CMakeLists.txt
            if os.path.isdir(project_path):
                cmake_file = os.path.join(project_path, "CMakeLists.txt")
                if os.path.exists(cmake_file):
                    # Get project info
                    project_info = get_project_info(project_path)
                    projects.append((item, project_info))
        
        # Sort by project name
        projects.sort(key=lambda x: x[0].lower())
        
    except Exception as e:
        print(f"Warning: Failed to scan existing projects: {e}")
    
    return projects

def get_project_info(project_path: str) -> str:
    """Get brief info about a project by examining its CMakeLists.txt file."""
    try:
        cmake_file = os.path.join(project_path, "CMakeLists.txt")
        if not os.path.exists(cmake_file):
            return "No CMakeLists.txt found"
        
        with open(cmake_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Extract some key information
        info_parts = []
        
        # Look for project name
        project_match = re.search(r'project\s*\(\s*([^)]+)\)', content, re.IGNORECASE)
        if project_match:
            info_parts.append(f"Project: {project_match.group(1).strip()}")
        
        # Look for JUCE plugin info
        if 'juce_add_plugin' in content.lower():
            # Extract product name
            product_match = re.search(r'PRODUCT_NAME\s+"([^"]+)"', content)
            if product_match:
                info_parts.append(f"Product: {product_match.group(1)}")
            
            # Extract formats
            formats_match = re.search(r'FORMATS\s+([^\n]+)', content)
            if formats_match:
                formats = formats_match.group(1).strip()
                info_parts.append(f"Formats: {formats}")
        
        # Check modification time
        mod_time = os.path.getmtime(cmake_file)
        import datetime
        mod_date = datetime.datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d")
        info_parts.append(f"Modified: {mod_date}")
        
        return " | ".join(info_parts) if info_parts else "JUCE Plugin Project"
        
    except Exception as e:
        return f"Error reading project: {str(e)}"

def extract_cmake_values_from_project(project_path: str) -> Dict[str, str]:
    """Extract CMake placeholder values from an existing project."""
    cmake_values = {}
    
    try:
        # Check main CMakeLists.txt
        cmake_file = os.path.join(project_path, "CMakeLists.txt")
        if os.path.exists(cmake_file):
            cmake_values.update(_extract_values_from_file(cmake_file))
        
        # Check Source/CMakeLists.txt
        source_cmake = os.path.join(project_path, "Source", "CMakeLists.txt")
        if os.path.exists(source_cmake):
            cmake_values.update(_extract_values_from_file(source_cmake))
        
        # Check source files for any additional values
        source_dir = os.path.join(project_path, "Source")
        if os.path.exists(source_dir):
            for file in os.listdir(source_dir):
                if file.endswith(('.cpp', '.h', '.hpp')):
                    file_path = os.path.join(source_dir, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                        values = _extract_values_from_content(content)
                        cmake_values.update(values)
                    except Exception:
                        continue
        
    except Exception as e:
        print(f"Warning: Failed to extract CMake values from {project_path}: {e}")
    
    return cmake_values

def _extract_values_from_file(file_path: str) -> Dict[str, str]:
    """Extract values from a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        return _extract_values_from_content(content)
    except Exception:
        return {}

def _extract_values_from_content(content: str) -> Dict[str, str]:
    """Extract placeholder values from file content by analyzing actual values."""
    values = {}
    
    # Common JUCE plugin patterns to extract actual values
    patterns = {
        # JUCE plugin configuration
        r'PRODUCT_NAME\s+"([^"]+)"': '{{PRODUCT_NAME}}',
        r'COMPANY_NAME\s+"([^"]+)"': '{{COMPANY_NAME}}',
        r'PLUGIN_MANUFACTURER_CODE\s+([A-Za-z0-9]{4})': '{{PLUGIN_MANUFACTURER_CODE}}',
        r'PLUGIN_CODE\s+([A-Za-z0-9]{4})': '{{PLUGIN_CODE}}',
        r'VERSION\s+(\d+\.\d+\.\d+)': '{{PROJECT_VERSION}}',
        r'project\s*\(\s*([^)\s]+)': '{{PROJECT_NAME}}',
        
        # Additional patterns
        r'DESCRIPTION\s+"([^"]+)"': '{{DESCRIPTION}}',
        r'PLUGIN_CATEGORY\s+([^\s\n]+)': '{{PLUGIN_CATEGORY}}',
        r'set\s*\(\s*CMAKE_CXX_STANDARD\s+(\d+)': '{{CXX_STANDARD}}',
    }
    
    for pattern, placeholder in patterns.items():
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            actual_value = match.group(1).strip().strip('"')
            if actual_value and placeholder not in values:
                values[placeholder] = actual_value
    
    return values

def copy_and_replace(src, dst, template_name, project_name, cmake_fields=None):
    """Recursively copy src to dst, replacing template_name with project_name in file contents and names. 
    Skips 'out' and '.vs' directories."""
    if not os.path.exists(dst):
        os.makedirs(dst)
        
    for root, dirs, files in os.walk(src):
        # Skip 'out' and '.vs' directories at any level
        dirs[:] = [d for d in dirs if d not in ('out', '.vs')]
        
        rel_path = os.path.relpath(root, src)
        target_root = os.path.join(dst, rel_path.replace(template_name, project_name))
        
        if not os.path.exists(target_root):
            os.makedirs(target_root)
            
        for file in files:
            src_file = os.path.join(root, file)
            target_file = os.path.join(target_root, file.replace(template_name, project_name))
            
            try:
                with open(src_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Replace template name in content
                content = content.replace(template_name, project_name)
                
                # Apply CMake field replacements to all files (not just CMakeLists.txt)
                # This allows placeholders in source files too
                if cmake_fields:
                    content = apply_cmake_replacements(content, cmake_fields)
                
                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
            except Exception as e:
                print(f"Warning: Could not process file {src_file}: {e}")
                # Copy file as-is if processing fails
                try:
                    with open(src_file, 'rb') as src_f, open(target_file, 'wb') as dst_f:
                        dst_f.write(src_f.read())
                except Exception as copy_error:
                    print(f"Error: Could not copy file {src_file}: {copy_error}")

def apply_cmake_replacements(content, cmake_fields):
    """Apply CMake field replacements to CMakeLists.txt content.
    
    Since templates now use consistent {{PLACEHOLDER}} format,
    we can simplify the replacement logic.
    """
    replacements = cmake_fields.get("custom_replacements", {})
    
    # Apply all placeholder replacements
    for placeholder, value in replacements.items():
        if not placeholder or not value:  # Skip empty entries
            continue
        
        # Direct placeholder replacement (templates use {{PLACEHOLDER}} format)
        content = content.replace(placeholder, value)
    
    return content


def create_custom_replacements_table(parent):
    """Create a table for custom find/replace relationships."""
    table_frame = ttk.LabelFrame(parent, text="Custom CMake Replacements", padding="10")
    table_frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    # Instructions
    instructions = ttk.Label(table_frame, text="Define custom find/replace pairs for CMakeLists.txt files:")
    instructions.pack(anchor="w", pady=(0, 2))
    
    # Create treeview for the table
    columns = ("find", "replace")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=6)
    tree.heading("find", text="Find (Placeholder)")
    tree.heading("replace", text="Replace With")
    tree.column("find", width=200)
    tree.column("replace", width=200)
    
    # Add scrollbar
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Pack tree and scrollbar directly without extra frame
    tree.pack(side="left", fill="both", expand=True, pady=(0, 5))
    scrollbar.pack(side="right", fill="y", pady=(0, 5))
    
    # Button frame
    button_frame = ttk.Frame(table_frame)
    button_frame.pack(fill="x", pady=5)

    # Find and replace all replaceable strings in all CMakeLists.txt files
    default_entries = []
    
    def scan_template_files():
        """Scan template files for placeholders and return sensible defaults."""
        found_placeholders = set()
        
        if not os.path.exists(SRC_DIR):
            return get_fallback_defaults()
        
        # Get all text files that might contain placeholders
        text_extensions = {'.txt', '.cmake', '.cpp', '.h', '.hpp', '.c', '.cc', '.cxx'}
        
        for root, dirs, files in os.walk(SRC_DIR):
            # Skip build directories
            dirs[:] = [d for d in dirs if d not in ('out', '.vs', 'build', '.git')]
            
            for file in files:
                file_path = os.path.join(root, file)
                _, ext = os.path.splitext(file)
                
                # Check if file might contain placeholders
                if ext.lower() in text_extensions or file == 'CMakeLists.txt':
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                        
                        # Find all {{PLACEHOLDER}} patterns
                        placeholders = re.findall(r'\{\{([A-Z_][A-Z0-9_]*)\}\}', content)
                        for placeholder in placeholders:
                            placeholder_full = f"{{{{{placeholder}}}}}"
                            found_placeholders.add(placeholder_full)
                            
                    except Exception as e:
                        # Skip files that can't be read
                        continue
        
        # Convert to list with sensible defaults
        return [(placeholder, get_default_value(placeholder)) for placeholder in sorted(found_placeholders)]
    
    def get_default_value(placeholder):
        """Get a sensible default value for a placeholder."""
        placeholder_upper = placeholder.upper()
        
        if 'VERSION' in placeholder_upper:
            return "1.0.0"
        elif 'PROJECT_NAME' in placeholder_upper or placeholder_upper == '{{PROJECT_NAME}}':
            return "MyProject"
        elif 'PRODUCT_NAME' in placeholder_upper:
            return "My Product"
        elif 'COMPANY' in placeholder_upper or 'MANUFACTURER' in placeholder_upper:
            if 'CODE' in placeholder_upper:
                return "Mcmp"  # 4-char manufacturer code
            else:
                return "MyCompany"
        elif 'PLUGIN_CODE' in placeholder_upper:
            return "MYPG"  # 4-char plugin code
        elif 'STANDARD' in placeholder_upper:
            return "17"
        elif 'CATEGORY' in placeholder_upper:
            return "Effect"
        elif 'DESCRIPTION' in placeholder_upper:
            return "Audio Plugin Project"
        else:
            # Generic default: convert SNAKE_CASE to Title Case
            return placeholder.strip('{}').replace('_', ' ').title()
    
    def get_fallback_defaults():
        """Return fallback defaults if template scanning fails."""
        return [
            ("{{PROJECT_NAME}}", "DriveR"),
            ("{{PROJECT_VERSION}}", "1.0.0"),
            ("{{PLUGIN_MANUFACTURER_CODE}}", "Mcmp"),
            ("{{PLUGIN_CODE}}", "Drvr"),
            ("{{PRODUCT_NAME}}", "Drive R"),
        ]
    
    try:
        default_entries = scan_template_files()
    except Exception as e:
        print(f"Warning: Template scanning failed, using fallback defaults: {e}")
        default_entries = get_fallback_defaults()

    
    for find_text, replace_text in default_entries:
        tree.insert("", "end", values=(find_text, replace_text))
    
    # Functions for table management
    def add_entry():
        """Add a new entry to the table."""
        dialog = tk.Toplevel(parent)
        dialog.title("Add Custom Replacement")
        dialog.geometry("400x150")
        dialog.transient(parent)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (150 // 2)
        dialog.geometry(f"400x150+{x}+{y}")
        
        ttk.Label(dialog, text="Find (Placeholder):").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        find_entry = ttk.Entry(dialog, width=40)
        find_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Replace With:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        replace_entry = ttk.Entry(dialog, width=40)
        replace_entry.grid(row=1, column=1, padx=10, pady=5)
        
        def save_entry():
            find_text = find_entry.get().strip()
            replace_text = replace_entry.get().strip()
            
            if not find_text:
                messagebox.showerror("Error", "Find field cannot be empty")
                return
            
            # Check for duplicates
            for item in tree.get_children():
                if tree.item(item)["values"][0] == find_text:
                    messagebox.showerror("Error", "This placeholder already exists")
                    return
            
            tree.insert("", "end", values=(find_text, replace_text))
            dialog.destroy()
        
        def cancel_entry():
            dialog.destroy()
        
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Add", command=save_entry).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=cancel_entry).pack(side="left", padx=5)
        
        find_entry.focus()
    
    def remove_entry():
        """Remove selected entry from the table."""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an entry to remove")
            return
        
        for item in selection:
            tree.delete(item)
    
    def edit_entry():
        """Edit the selected entry."""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an entry to edit")
            return
        
        if len(selection) > 1:
            messagebox.showwarning("Warning", "Please select only one entry to edit")
            return
        
        # Get the first (and only) selected item
        item = selection[0] if selection else None
        if not item:
            messagebox.showwarning("Warning", "No entry selected")
            return
            
        current_values = tree.item(item)["values"]
        
        # Ensure we have valid values
        if not current_values or len(current_values) < 2:
            messagebox.showerror("Error", "Invalid entry selected")
            return
        
        dialog = tk.Toplevel(parent)
        dialog.title("Edit Custom Replacement")
        dialog.geometry("400x150")
        dialog.transient(parent)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (150 // 2)
        dialog.geometry(f"400x150+{x}+{y}")
        
        ttk.Label(dialog, text="Find (Placeholder):").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        find_entry = ttk.Entry(dialog, width=40)
        find_entry.insert(0, current_values[0])
        find_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Replace With:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        replace_entry = ttk.Entry(dialog, width=40)
        replace_entry.insert(0, current_values[1])
        replace_entry.grid(row=1, column=1, padx=10, pady=5)
        
        def save_changes():
            find_text = find_entry.get().strip()
            replace_text = replace_entry.get().strip()
            
            if not find_text:
                messagebox.showerror("Error", "Find field cannot be empty")
                return
            
            # Check for duplicates (excluding current item)
            for other_item in tree.get_children():
                if other_item != item and tree.item(other_item)["values"][0] == find_text:
                    messagebox.showerror("Error", "This placeholder already exists")
                    return
            
            tree.item(item, values=(find_text, replace_text))
            dialog.destroy()
        
        def cancel_changes():
            dialog.destroy()
        
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Save", command=save_changes).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=cancel_changes).pack(side="left", padx=5)
        
        find_entry.focus()
    
    # Buttons
    ttk.Button(button_frame, text="+ Add", command=add_entry).pack(side="left", padx=5)
    ttk.Button(button_frame, text="- Remove", command=remove_entry).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Edit", command=edit_entry).pack(side="left", padx=5)
    
    # Double-click to edit
    tree.bind("<Double-1>", lambda e: edit_entry())
    
    return tree

def create_project_selector_frame(parent):
    """Create a frame for selecting existing projects or creating new ones."""
    global project_mode_var, new_project_frame, existing_project_frame
    
    selector_frame = ttk.LabelFrame(parent, text="Project Selection", padding="10")
    selector_frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    # Mode selection
    mode_frame = ttk.Frame(selector_frame)
    mode_frame.pack(fill="x", pady=(0, 10))
    
    project_mode_var = tk.StringVar(value="new")
    
    # Radio buttons for mode selection
    new_radio = ttk.Radiobutton(mode_frame, text="Create New Project", 
                               variable=project_mode_var, value="new",
                               command=lambda: toggle_project_mode("new"))
    new_radio.pack(anchor="w")
    
    existing_radio = ttk.Radiobutton(mode_frame, text="Load Existing Project", 
                                   variable=project_mode_var, value="existing",
                                   command=lambda: toggle_project_mode("existing"))
    existing_radio.pack(anchor="w")
    
    # Container for mode-specific content
    content_frame = ttk.Frame(selector_frame)
    content_frame.pack(fill="both", expand=True)
    
    # New project frame
    new_project_frame = ttk.Frame(content_frame)
    
    ttk.Label(new_project_frame, text="Enter new project name:").pack(anchor="w", pady=(0, 5))
    global entry  # Make it accessible globally
    entry = ttk.Entry(new_project_frame, width=40, font=("TkDefaultFont", 10))
    entry.pack(fill="x", pady=5)
    entry.focus()
    
    # Existing project frame
    existing_project_frame = ttk.Frame(content_frame)
    
    ttk.Label(existing_project_frame, text="Select an existing project:").pack(anchor="w", pady=(0, 5))
    
    # Project list with scrollbar
    list_frame = ttk.Frame(existing_project_frame)
    list_frame.pack(fill="both", expand=True, pady=5)
    
    # Create Treeview for project list
    columns = ("name", "info")
    global project_tree  # Make it accessible globally
    project_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=8)
    project_tree.heading("name", text="Project Name")
    project_tree.heading("info", text="Project Info")
    project_tree.column("name", width=200)
    project_tree.column("info", width=400)
    
    # Scrollbars
    v_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=project_tree.yview)
    h_scrollbar = ttk.Scrollbar(list_frame, orient="horizontal", command=project_tree.xview)
    project_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
    
    project_tree.pack(side="left", fill="both", expand=True)
    v_scrollbar.pack(side="right", fill="y")
    h_scrollbar.pack(side="bottom", fill="x")
    
    # Bind selection event
    project_tree.bind("<<TreeviewSelect>>", on_project_selected)
    
    # Refresh button
    refresh_btn = ttk.Button(existing_project_frame, text="🔄 Refresh Project List", 
                           command=refresh_project_list)
    refresh_btn.pack(anchor="w", pady=(5, 0))
    
    # Status label
    global project_status_label
    project_status_label = ttk.Label(existing_project_frame, text="", 
                                   font=("TkDefaultFont", 8), foreground="gray")
    project_status_label.pack(anchor="w", pady=(2, 0))
    
    # Load project button
    load_btn = ttk.Button(existing_project_frame, text="Load Selected Project", 
                         command=load_selected_project)
    load_btn.pack(anchor="w", pady=(5, 0))
    
    def toggle_project_mode(mode):
        """Switch between new and existing project modes."""
        if mode == "new":
            existing_project_frame.pack_forget()
            new_project_frame.pack(fill="both", expand=True)
            entry.focus()
        else:
            new_project_frame.pack_forget()
            existing_project_frame.pack(fill="both", expand=True)
            refresh_project_list()
    
    # Initially show new project mode
    toggle_project_mode("new")
    
    return selector_frame, project_mode_var

def refresh_project_list():
    """Refresh the list of existing projects."""
    # Clear existing items
    for item in project_tree.get_children():
        project_tree.delete(item)
    
    # Scan for projects
    projects = scan_existing_projects()
    
    if not projects:
        # Add a message if no projects found
        project_tree.insert("", "end", values=("No projects found", f"No projects found in {DST_DIR}"))
        status_text = "No existing projects found"
    else:
        # Populate the tree
        for project_name, project_info in projects:
            project_tree.insert("", "end", values=(project_name, project_info))
        status_text = f"Found {len(projects)} existing project(s)"
    
    # Update status if we have a status label
    if 'project_status_label' in globals():
        project_status_label.config(text=status_text)

def on_project_selected(event):
    """Handle project selection in the tree."""
    selection = project_tree.selection()
    if not selection:
        return
    
    item = selection[0]
    values = project_tree.item(item)["values"]
    
    if values and values[0] != "No projects found":
        project_name = values[0]
        # Update status or provide feedback
        print(f"Selected project: {project_name}")

def load_selected_project():
    """Load the selected project and populate CMake fields."""
    selection = project_tree.selection()
    if not selection:
        messagebox.showwarning("Warning", "Please select a project to load")
        return
    
    item = selection[0]
    values = project_tree.item(item)["values"]
    
    if not values or values[0] == "No projects found":
        messagebox.showwarning("Warning", "No valid project selected")
        return
    
    project_name = values[0]
    project_path = os.path.join(DST_DIR, project_name)
    
    try:
        # Extract CMake values from the project
        cmake_values = extract_cmake_values_from_project(project_path)
        
        if not cmake_values:
            messagebox.showinfo("Info", f"No CMake values found in project '{project_name}'")
        
        # Clear existing replacements table
        for item in replacements_table.get_children():
            replacements_table.delete(item)
        
        # Populate table with extracted values
        for placeholder, value in cmake_values.items():
            replacements_table.insert("", "end", values=(placeholder, value))
        
        # Update entry with project name
        entry.delete(0, tk.END)
        entry.insert(0, project_name)
        
        # Switch to new project mode for editing
        project_mode_var.set("new")
        new_project_frame.pack(fill="both", expand=True)
        existing_project_frame.pack_forget()
        
        messagebox.showinfo("Success", 
                          f"Loaded project '{project_name}' with {len(cmake_values)} CMake values.\n\n"
                          f"You can now modify the settings and create/update the project.")
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load project '{project_name}':\n\n{str(e)}")

def create_cmake_fields_frame(parent):
    """Create a simplified frame for basic project information."""
    info_frame = ttk.LabelFrame(parent, text="Project Information", padding="10")
    info_frame.pack(fill="x", padx=10, pady=5)
    
    # Simple instruction text
    ttk.Label(info_frame, text="Use the Custom CMake Replacements table below to configure your project settings.").pack(anchor="w")
    
    return {}

from typing import Dict, Any
def get_cmake_field_values(fields, replacements_tree) -> Dict[str, Any]:
    """Extract values from custom replacements table."""
    custom_replacements = {}
    
    for item in replacements_tree.get_children():
        values = replacements_tree.item(item)["values"]
        if len(values) >= 2:
            find_text = values[0].strip()
            replace_text = values[1].strip()
            if find_text:  # Only add non-empty find text
                custom_replacements[find_text] = replace_text

    # Validate specific field formats
    for placeholder, value in custom_replacements.items():
        placeholder_upper = placeholder.upper()
        
        # Version validation
        if "VERSION" in placeholder_upper and value:
            if not re.match(r'^\d+\.\d+\.\d+$', value):
                raise ValueError(f"Invalid version format for {placeholder}: '{value}'. Must be in format X.Y.Z (e.g., 1.0.0)")
        
        # Plugin code validation (should be 4 characters)
        if "PLUGIN_CODE" in placeholder_upper and value:
            if not re.match(r'^[A-Za-z0-9]{4}$', value):
                raise ValueError(f"Invalid plugin code format for {placeholder}: '{value}'. Must be exactly 4 alphanumeric characters")
        
        # Manufacturer code validation (should be 4 characters)
        if "MANUFACTURER_CODE" in placeholder_upper and value:
            if not re.match(r'^[A-Za-z0-9]{4}$', value):
                raise ValueError(f"Invalid manufacturer code format for {placeholder}: '{value}'. Must be exactly 4 alphanumeric characters")

    return {"custom_replacements": custom_replacements}

def run_cmake_configure(target_dir):
    """Run CMake configuration for the project."""
    project_name = os.path.basename(target_dir)
    build_dir = os.path.join(target_dir, "build")
    
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
    
    # Show progress dialog
    progress_window = tk.Toplevel()
    progress_window.title("Running CMake")
    progress_window.geometry("400x150")
    progress_window.transient()
    progress_window.grab_set()
    
    # Center the progress window
    progress_window.update_idletasks()
    x = (progress_window.winfo_screenwidth() // 2) - (200)
    y = (progress_window.winfo_screenheight() // 2) - (75)
    progress_window.geometry(f"400x150+{x}+{y}")
    
    status_label = ttk.Label(progress_window, text=f"Configuring CMake for '{project_name}'...")
    status_label.pack(pady=20)
    
    progress_bar = ttk.Progressbar(progress_window, mode='indeterminate')
    progress_bar.pack(pady=10, padx=20, fill='x')
    progress_bar.start()
    
    # Force window to show
    progress_window.update()
    
    try:
        # Run CMake configuration
        result = subprocess.run(
            ["cmake", ".."],
            cwd=build_dir,
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout
        )
        
        progress_bar.stop()
        progress_window.destroy()
        
        if result.returncode == 0:
            messagebox.showinfo("Success", f"CMake configuration completed successfully!\nLaunching UI generator...")
            return True
        else:
            error_msg = f"CMake configuration failed!\n\nReturn code: {result.returncode}\n\nError output:\n{result.stderr}"
            if result.stdout:
                error_msg += f"\n\nStandard output:\n{result.stdout}"
            messagebox.showerror("CMake Error", error_msg)
            return False
            
    except subprocess.TimeoutExpired:
        progress_bar.stop()
        progress_window.destroy()
        messagebox.showerror("Timeout", "CMake configuration timed out after 2 minutes.")
        return False
        
    except FileNotFoundError:
        progress_bar.stop()
        progress_window.destroy()
        messagebox.showerror(
            "CMake Not Found", 
            "CMake is not installed or not found in PATH.\n\nPlease install CMake and ensure it's available in your system PATH."
        )
        return False
        
    except Exception as e:
        progress_bar.stop()
        progress_window.destroy()
        messagebox.showerror("Error", f"An error occurred while running CMake:\n\n{str(e)}")
        return False

def run_ui_generator(target_dir):
    """Run the UI generator application with the target directory."""
    project_name = os.path.basename(target_dir)
    
    # Check if CMake is already configured
    if cmake_ready(target_dir):
        messagebox.showinfo("CMake Ready", f"CMake is already configured for '{project_name}'.\nLaunching UI generator...")
    else:
        # Run CMake configuration automatically
        if not run_cmake_configure(target_dir):
            return  # CMake failed, don't continue
    
    # Launch the UI generator
    app = UIGeneratorApp(target_dir)
    app.run()

def on_create():
    """Handle project creation button click."""
    project_name = entry.get().strip()
    if not project_name:
        messagebox.showerror("Error", "Please enter a project name.")
        return
        
    target_dir = os.path.join(DST_DIR, project_name)
    
    # Determine if this is a new project or updating existing
    is_existing_project = os.path.exists(target_dir)
    action_verb = "update" if is_existing_project else "create"
    
    # Check if project already exists and confirm action
    if is_existing_project:
        response = messagebox.askyesno(
            "Project Exists", 
            f"Project '{project_name}' already exists.\n\nDo you want to update it with the current settings?"
        )
        if not response:
            messagebox.showinfo("Info", "Project update cancelled.")
            return
    
    # Get CMake field values including custom replacements
    try:
        cmake_field_values = get_cmake_field_values(cmake_fields, replacements_table)
        cmake_field_values["project_name"] = project_name
        
        # Show what will be updated
        num_replacements = len(cmake_field_values.get("custom_replacements", {}))
        if is_existing_project:
            confirm_msg = (f"About to update project '{project_name}' with:\n"
                          f"• {num_replacements} CMake replacements\n"
                          f"• Project type: {project_type_var.get()}\n\n"
                          f"This will overwrite existing files. Continue?")
            if not messagebox.askyesno("Confirm Update", confirm_msg):
                return
        
        # Create/update the project
        copy_and_replace(SRC_DIR, target_dir, TEMPLATE_NAME, project_name, cmake_field_values)
        
        # Show success message
        success_msg = f"Project '{project_name}' {action_verb}d successfully!"
        if is_existing_project:
            success_msg += f"\n\nUpdated {num_replacements} CMake values."
        messagebox.showinfo("Success", success_msg)
        
        # Launch UI generator
        run_ui_generator(target_dir)
        
    except ValueError as e:
        messagebox.showerror("Validation Error", str(e))
        return
    except Exception as e:
        messagebox.showerror("Error", f"Failed to {action_verb} project: {e}")
        traceback.print_exc()
        return

if __name__ == "__main__":
    # Initialize main window
    root = tk.Tk()
    root.title("Project Initializer")
    root.geometry("900x800")  # Increased size for project list
    root.resizable(True, True)

    # Create project info frame
    info_frame = ttk.LabelFrame(root, text="Project Type", padding="10")
    info_frame.pack(fill="x", padx=10, pady=5)
    
    project_type_var = tk.StringVar(value="standard")
    ttk.Radiobutton(info_frame, text="Standard JUCE Plugin", variable=project_type_var, value="standard").pack(anchor="w")
    ttk.Radiobutton(info_frame, text="JUCE Plugin with UI Builder", variable=project_type_var, value="with_ui_builder").pack(anchor="w")
    
    # Info text
    info_text = ttk.Label(info_frame, text="UI Builder option includes predefined JUCE controls for common audio plugin interfaces.", 
                         font=("TkDefaultFont", 8), foreground="gray")
    info_text.pack(anchor="w", pady=(5, 0))

    # Project selector (replaces simple name entry)
    project_selector, project_mode_var = create_project_selector_frame(root)

    # CMake configuration section (simplified info frame)
    cmake_fields = create_cmake_fields_frame(root)
    
    # Custom replacements table
    replacements_table = create_custom_replacements_table(root)

    # Create button
    button_frame = ttk.Frame(root)
    button_frame.pack(fill="x", padx=10, pady=15)
    
    create_btn = ttk.Button(button_frame, text="Create/Update Project", command=on_create)
    create_btn.pack()

    # Bind Enter key to create project
    root.bind('<Return>', lambda event: on_create())

    root.mainloop()