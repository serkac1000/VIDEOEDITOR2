#!/usr/bin/env python3
"""
Main entry point for the Video Editor GUI application.
Cross-platform compatible version.
"""

import tkinter as tk
import sys
import os
import platform
from video_editor_gui import VideoEditorGUI

def check_environment():
    """Check and configure environment for cross-platform compatibility."""
    system = platform.system()
    print(f"Running on {system} {platform.release()}")
    
    # Windows-specific configuration
    if system == "Windows":
        try:
            # Enable DPI awareness on Windows
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass
    
    # macOS-specific configuration
    elif system == "Darwin":
        # Ensure proper focus behavior on macOS
        os.environ['TK_SILENCE_DEPRECATION'] = '1'

def main():
    """Initialize and run the Video Editor GUI application."""
    try:
        print("Video Editor GUI - Cross Platform Version")
        print("=" * 45)
        
        # Check environment
        check_environment()
        
        # Create root window with cross-platform settings
        root = tk.Tk()
        
        # Set window properties for better cross-platform behavior
        root.title("Voice-Controlled Video Editor")
        root.geometry("1200x800")
        
        # Platform-specific window behavior
        system = platform.system()
        if system == "Windows":
            root.state('normal')
            root.lift()
            root.focus_force()
        elif system == "Darwin":  # macOS
            root.lift()
            root.call('wm', 'attributes', '.', '-topmost', True)
            root.after_idle(root.call, 'wm', 'attributes', '.', '-topmost', False)
        else:  # Linux/Unix
            root.lift()
            root.attributes('-topmost', True)
            root.after_idle(root.attributes, '-topmost', False)
        
        # Initialize the application
        print("Initializing GUI components...")
        app = VideoEditorGUI(root)
        
        print("Video Editor GUI started successfully!")
        print("You can now use the application.")
        
        # Start the main loop
        root.mainloop()
        
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please run setup.py to install required packages.")
        input("Press Enter to exit...")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting GUI: {e}")
        print(f"System: {platform.system()}")
        print(f"Python: {sys.version}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
