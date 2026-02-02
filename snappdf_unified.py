#!/usr/bin/env python3
# -------------------------------------------------------------
# SnapPDF Unified - Main Entry Point
# A simple and powerful tool to combine multiple images into a single PDF file.
#
# This program was developed with the assistance of ChatGPT.
# Copyright (c) 2023-2026 NAGATA Mizuho
# Institute of Laser Engineering, The University of Osaka
#
# Created on: 2023-09-29
# Updated to unified version: 2026
# Version: 2.0.0
# -------------------------------------------------------------

"""
SnapPDF Unified Application

This is the main entry point for the unified SnapPDF application.
It combines all previous versions (SnapPDF, SnapPDF2, SnapPDF4, SnapPDF6, SnapPDF15)
into a single configurable application.

Features:
- Multiple layout options (2, 4, 6, 15 images per page)
- Excel data integration
- Image reordering (move up/down, delete)
- Thumbnail preview
- Drag and drop support (if tkinterdnd2 is available)
- User-friendly GUI with layout selection

Usage:
    python snappdf_unified.py
"""

import os
import sys

# Add the parent directory to the path so we can import snappdf package
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from snappdf import __author__, __license__, __version__
    from snappdf.ui import create_application
except ImportError as e:
    print("Error: Could not import SnapPDF modules.")
    print(f"Details: {e}")
    print("\nPlease ensure all required dependencies are installed:")
    print("  pip install Pillow reportlab pandas")
    print("  pip install tkinterdnd2  # Optional, for drag-and-drop support")
    sys.exit(1)


def main():
    """Main entry point for the application"""
    print(f"SnapPDF Unified v{__version__}")
    print(f"Copyright (c) 2023-2026 {__author__}")
    print(f"License: {__license__}")
    print("-" * 60)
    print("Starting SnapPDF application...")
    print()

    try:
        # Create and run the application
        app = create_application()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
