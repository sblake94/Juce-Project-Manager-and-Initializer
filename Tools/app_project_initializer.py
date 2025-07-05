import os
import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import traceback

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

def copy_and_replace(src, dst, template_name, project_name):
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
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(content)

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
    subprocess.Popen([
        sys.executable,
        os.path.join(os.path.dirname(__file__), 'app_ui_generator.py'),
        target_dir
    ])

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
    else:
        copy_and_replace(SRC_DIR, target_dir, TEMPLATE_NAME, project_name)

    try:
        run_ui_generator(target_dir)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create project: {e}")
        traceback.print_exc()
        raise e

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Project Initializer")
    root.geometry("400x150")

    label = tk.Label(root, text="Enter new project name:")
    label.pack(pady=10)

    entry = tk.Entry(root, width=30)
    entry.pack(pady=5)

    create_btn = tk.Button(root, text="Create Project", command=on_create)
    create_btn.pack(pady=15)

    root.mainloop()