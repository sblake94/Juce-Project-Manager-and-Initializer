from __future__ import annotations
import traceback
from src.UIGeneratorApp import UIGeneratorApp

def main():
    """Main entry point"""
    try:
        app = UIGeneratorApp()
        app.run()
    except Exception as e:
        print(f"Application Error: {e}")
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()