#!/usr/bin/env python3
"""
Setup script for Video Editor GUI - Cross Platform Support
"""

import sys
import subprocess
import os
import platform

# Required packages
REQUIRED_PACKAGES = [
    'moviepy==2.2.1',
    'yt-dlp>=2025.6.9',
    'scipy>=1.15.3',
    'numpy>=2.3.0',
    'transformers>=4.52.4',
    'requests>=2.32.4',
    'opencv-python>=4.11.0.86',
    'pillow>=11.2.1',
    'sounddevice>=0.5.2'
]

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required.")
        sys.exit(1)
    print(f"Python {sys.version} detected - OK")

def install_packages():
    """Install required packages."""
    print("Installing required packages...")
    for package in REQUIRED_PACKAGES:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to install {package}: {e}")
            if 'sounddevice' in package and platform.system() == 'Windows':
                print("Note: Audio recording may not work on this system.")
            continue

def check_audio_support():
    """Check if audio recording is supported."""
    try:
        import sounddevice
        print("Audio recording support: Available")
        return True
    except (ImportError, OSError):
        print("Audio recording support: Not available (optional)")
        return False

def main():
    """Main setup function."""
    print("Video Editor GUI - Cross Platform Setup")
    print("=" * 40)
    
    check_python_version()
    install_packages()
    check_audio_support()
    
    print("\nSetup complete!")
    print("Run 'python main.py' to start the application.")

if __name__ == "__main__":
    main()