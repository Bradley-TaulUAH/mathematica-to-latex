#!/usr/bin/env python3
"""
Simple launcher for the Mathematica to LaTeX/Markdown Converter GUI
Automatically chooses the best GUI option available
"""

import sys

def main():
    """Launch the appropriate GUI"""
    # Try to use tkinter GUI first (preferred)
    try:
        import tkinter as tk
        print("Launching desktop GUI...")
        import mathematica_gui
        mathematica_gui.main()
        return 0
    except ImportError as e:
        print("tkinter not available:", str(e))
        print("\nTrying web GUI as fallback...")
        
        # Try web GUI as fallback
        try:
            import flask
            print("Starting web GUI server...")
            print("Open your browser to: http://localhost:5000")
            import web_gui
            web_gui.app.run(debug=False, host='0.0.0.0', port=5000)
            return 0
        except ImportError:
            print("\nError: Neither tkinter nor Flask is available.")
            print("\nTo use the desktop GUI (recommended):")
            print("  - On Ubuntu/Debian: sudo apt-get install python3-tk")
            print("  - On Fedora: sudo dnf install python3-tkinter")
            print("  - On Arch: sudo pacman -S tk")
            print("\nTo use the web GUI (alternative):")
            print("  pip install flask werkzeug")
            print("  python web_gui.py")
            print("\nOr use the command-line interface:")
            print("  python mathematica_converter.py <input.nb>")
            return 1

if __name__ == "__main__":
    sys.exit(main())
