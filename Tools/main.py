import os
import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import sys
import traceback
import re
from src.UIGeneratorApp import UIGeneratorApp

# Static variables
SRC_DIR = r"D:/Dev/Visual Studio Projects/AudioPlugins/MyAwesomePluginCompany/Template/MyCMakeProject"  # Example source
DST_DIR = r"D:/Dev/Visual Studio Projects/AudioPlugins/MyAwesomePluginCompany/MyAwesomePlugins"  # Example destination
TEMPLATE_NAME = "MyCMakeProject"  # The name to replace in files and filenames

def cmake_ready(build_dir: str) -> bool:
    """Check if CMake has been run successfully by looking for CMakeCache.txt."""
    cmake_cache = os.path.join(build_dir, "out", "build", "x64-Debug", "CMakeCache.txt")
    ## make sure cmake_cache uses consistent path separators
    cmake_cache = os.path.normpath(cmake_cache)
    return os.path.isfile(cmake_cache)

def copy_and_replace(src, dst, template_name, project_name, cmake_fields=None):
    """Recursively copy src to dst, replacing template_name with project_name in file contents and names. Skips 'out' directory."""
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
            with open(src_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            content = content.replace(template_name, project_name)
            
            # Apply CMake field replacements if this is a CMakeLists.txt file
            if file == "CMakeLists.txt" and cmake_fields:
                content = apply_cmake_replacements(content, cmake_fields)
            
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(content)

def apply_cmake_replacements(content, cmake_fields):
    """Apply CMake field replacements to CMakeLists.txt content."""
    # Get all replacements from the custom replacements table
    replacements = cmake_fields.get("custom_replacements", {})
    
    # Apply all replacements
    for placeholder, value in replacements.items():
        if not placeholder or not value:  # Skip empty entries
            continue
            
        # Handle direct placeholder replacement
        content = content.replace(placeholder, value)
        
        # Replace common CMake patterns for standard CMake variables
        content = content.replace(f"set({placeholder} \"placeholder\")", f"set({placeholder} \"{value}\")")
        content = content.replace(f"set({placeholder} placeholder)", f"set({placeholder} {value})")
        
        # Handle VERSION in project() declaration if it's a version placeholder
        if "VERSION" in placeholder.upper():
            content = re.sub(r'project\([^)]*VERSION\s+[\d.]+', f'project({cmake_fields.get("project_name", "MyProject")} VERSION {value}', content)
    
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
    
    # Add default entries
    default_entries = [
        ("{{PROJECT_NAME}}", "MyProject"),
        ("{{PROJECT_VERSION}}", "1.0.0"),
        ("{{PROJECT_DESCRIPTION}}", "Audio Plugin Project"),
        ("{{CMAKE_CXX_STANDARD}}", "17"),
        ("{{PLUGIN_MANUFACTURER}}", "MyCompany"),
        ("{{PLUGIN_CATEGORY}}", "Effect"),
        ("{{PLUGIN_CODE}}", "MYPG"),
        ("{{COMPANY_NAME}}", "MyCompany")
    ]
    
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

def create_cmake_fields_frame(parent):
    """Create a simplified frame for basic project information."""
    info_frame = ttk.LabelFrame(parent, text="Project Information", padding="10")
    info_frame.pack(fill="x", padx=10, pady=5)
    
    # Simple instruction text
    ttk.Label(info_frame, text="Use the Custom CMake Replacements table below to configure your project settings.").pack(anchor="w")
    
    return {}

from typing import Dict, Any

def get_cmake_field_values(fields, replacements_tree) -> dict[str, Any]:
    """Extract values from custom replacements table."""
    # Get custom replacements from table
    custom_replacements = {}
    for item in replacements_tree.get_children():
        values = replacements_tree.item(item)["values"]
        if len(values) >= 2:
            find_text = values[0].strip()
            replace_text = values[1].strip()
            if find_text:  # Only add non-empty find text
                custom_replacements[find_text] = replace_text

    # Validate version format if present
    version_keys = [key for key in custom_replacements.keys() if "VERSION" in key.upper()]
    for version_key in version_keys:
        version_value = custom_replacements[version_key]
        if version_value and not re.match(r'^\d+\.\d+\.\d+$', version_value):
            raise ValueError(f"Invalid version format for {version_key}: {version_value}. Must be in format X.Y.Z (e.g., 1.0.0)")

    # Return the custom replacements directly, not wrapped in another dict
    result: dict[str, Any] = {"custom_replacements": custom_replacements}
    return result

def run_ui_generator(target_dir):
    """Run the UI generator application with the target directory."""
    project_name = os.path.basename(target_dir)
    build_dir = os.path.join(target_dir, "build")
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
    # Prompt/check only if CMake is not ready
    should_continue = False
    while not should_continue:
        messagebox.showinfo(
            "Run CMake",
            f"Project '{project_name}' created at {target_dir}.\n\nPlease open a terminal and run CMake in the build directory:\n\n    cd {build_dir}\n    cmake ..\n\nAfter CMake completes successfully, click OK to continue."
        )
        if cmake_ready(target_dir):
            should_continue = True
        else:
            retry = messagebox.askretrycancel(
                "CMake Not Detected",
                f"CMake output not found in {target_dir}.\n\nPlease make sure you have run CMake successfully."
            )
            if not retry:
                return
    # Always run this after CMake is ready
    messagebox.showinfo("Success", f"CMake detected! Continuing to launch the UI generator.")
    app = UIGeneratorApp(target_dir)
    app.run()

def on_create():
    ## check first if the directory we are trying to create already exists
    project_name = entry.get().strip()
    if not project_name:
        messagebox.showerror("Error", "Please enter a project name.")
        return
    target_dir = os.path.join(DST_DIR, project_name)
    if os.path.exists(target_dir):
        nextAction = messagebox.showwarning("Warning", f"Project '{project_name}' already exists. \n\nDo you want to continue with project creation?")
        if nextAction != 'ok':
            messagebox.showinfo("Info", "Project creation cancelled.")
            return
        else:
            messagebox.showinfo("Info", "Continuing with project creation.")
    
    # Get CMake field values including custom replacements
    try:
        cmake_field_values = get_cmake_field_values(cmake_fields, replacements_table)
        # Add project name as a separate field, not part of custom_replacements
        cmake_field_values["project_name"] = project_name
        copy_and_replace(SRC_DIR, target_dir, TEMPLATE_NAME, project_name, cmake_field_values)
    except ValueError as e:
        messagebox.showerror("Validation Error", str(e))
        return
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process CMake fields: {e}")
        return

    try:
        run_ui_generator(target_dir)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create project: {e}")
        traceback.print_exc()
        raise e

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Project Initializer")
    root.geometry("700x600")

    # Project name section
    name_frame = ttk.Frame(root)
    name_frame.pack(fill="x", padx=10, pady=10)
    
    label = tk.Label(name_frame, text="Enter new project name:")
    label.pack(pady=(0, 5))

    entry = tk.Entry(name_frame, width=30)
    entry.pack(pady=5)

    # CMake configuration section
    cmake_fields = create_cmake_fields_frame(root)
    
    # Custom replacements table
    replacements_table = create_custom_replacements_table(root)

    # Create button
    create_btn = tk.Button(root, text="Create Project", command=on_create)
    create_btn.pack(pady=15)

    root.mainloop()