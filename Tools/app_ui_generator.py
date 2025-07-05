from __future__ import annotations
import traceback
import sys
from src.UIGeneratorApp import UIGeneratorApp

def main():
    """Main entry point"""
    try:
        # Require directory argument
        if len(sys.argv) < 2:
            print("Error: No project directory provided.\nUsage: python app_ui_generator.py <project_directory>")
            input("Press Enter to exit...")
            return
        directory = sys.argv[1]
        app = UIGeneratorApp(directory)
        app.run()
    except Exception as e:
        print(f"Application Error: {e}")
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()