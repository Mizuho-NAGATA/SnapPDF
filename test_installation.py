#!/usr/bin/env python3
# -------------------------------------------------------------
# Installation Test Script for SnapPDF v2.0
# Copyright (c) 2023-2026 NAGATA Mizuho
# Institute of Laser Engineering, The University of Osaka
# -------------------------------------------------------------

"""
Test script to validate SnapPDF v2.0 installation.

This script checks:
1. Python version
2. Required dependencies
3. Optional dependencies
4. Module imports
5. Basic functionality
"""

import os
import sys

print("=" * 70)
print("SnapPDF v2.0 Installation Test")
print("=" * 70)
print()

# Test 1: Python Version
print("Test 1: Python Version")
print("-" * 70)
version_info = sys.version_info
print(f"Python version: {sys.version}")
if version_info >= (3, 7):
    print("✓ Python version is compatible (>= 3.7)")
else:
    print("✗ Python version is too old. Please use Python 3.7 or higher.")
    sys.exit(1)
print()

# Test 2: Required Dependencies
print("Test 2: Required Dependencies")
print("-" * 70)
required_packages = {
    "PIL": "Pillow",
    "reportlab": "reportlab",
    "pandas": "pandas",
    "tkinter": "tkinter (standard library)",
}

all_required_ok = True
for module_name, package_name in required_packages.items():
    try:
        if module_name == "PIL":
            import PIL

            print(f"✓ {package_name}: version {PIL.__version__}")
        elif module_name == "reportlab":
            import reportlab

            print(f"✓ {package_name}: version {reportlab.Version}")
        elif module_name == "pandas":
            import pandas

            print(f"✓ {package_name}: version {pandas.__version__}")
        elif module_name == "tkinter":
            import tkinter

            print(f"✓ {package_name}: available")
    except ImportError as e:
        print(f"✗ {package_name}: NOT FOUND")
        print(f"  Install with: pip install {package_name.split()[0]}")
        all_required_ok = False

print()

# Test 3: Optional Dependencies
print("Test 3: Optional Dependencies")
print("-" * 70)
optional_packages = {
    "tkinterdnd2": "tkinterdnd2 (for drag-and-drop)",
    "PyPDF2": "PyPDF2 (for SnapSearch)",
}

for package_name, description in optional_packages.items():
    try:
        if package_name == "tkinterdnd2":
            import tkinterdnd2

            print(f"✓ {description}: available")
        elif package_name == "PyPDF2":
            import PyPDF2

            print(f"✓ {description}: version {PyPDF2.__version__}")
    except ImportError:
        print(f"⚠ {description}: NOT FOUND (optional)")
        print(f"  Install with: pip install {package_name}")

print()

# Test 4: SnapPDF Module Import
print("Test 4: SnapPDF Module Import")
print("-" * 70)
try:
    from snappdf import __author__, __license__, __version__

    print(f"✓ SnapPDF package imported successfully")
    print(f"  Version: {__version__}")
    print(f"  Author: {__author__}")
    print(f"  License: {__license__}")
except ImportError as e:
    print(f"✗ Failed to import SnapPDF package")
    print(f"  Error: {e}")
    all_required_ok = False

print()

# Test 5: SnapPDF Components
print("Test 5: SnapPDF Components")
print("-" * 70)
components = [
    ("AppConfig", "snappdf.config"),
    ("LayoutConfig", "snappdf.config"),
    ("PDFGenerator", "snappdf.core"),
    ("create_application", "snappdf.ui"),
]

all_components_ok = True
for component, module in components:
    try:
        if module == "snappdf.config":
            from snappdf.config import AppConfig, LayoutConfig
        elif module == "snappdf.core":
            from snappdf.core import PDFGenerator
        elif module == "snappdf.ui":
            from snappdf.ui import create_application
        print(f"✓ {component} from {module}")
    except ImportError as e:
        print(f"✗ {component} from {module}: FAILED")
        print(f"  Error: {e}")
        all_components_ok = False

print()

# Test 6: Layout Configuration
print("Test 6: Layout Configuration")
print("-" * 70)
try:
    from snappdf.config import AppConfig

    print("Available layouts:")
    for layout_name, layout in AppConfig.LAYOUTS.items():
        print(f"  • {layout.display_name}")
        print(f"    - Name: {layout.name}")
        print(f"    - Images per page: {layout.images_per_page}")
        print(f"    - Grid: {layout.columns}x{layout.rows}")
        print(f"    - Description: {layout.description}")
    print(f"✓ Total layouts available: {len(AppConfig.LAYOUTS)}")
except Exception as e:
    print(f"✗ Failed to load layout configuration")
    print(f"  Error: {e}")
    all_components_ok = False

print()

# Test 7: Font Configuration
print("Test 7: Font Configuration")
print("-" * 70)
try:
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    font_file = "BIZ-UDGothicR.ttc"
    if os.path.exists(font_file):
        try:
            pdfmetrics.registerFont(TTFont("BIZ-UDGothicR", font_file))
            print(f"✓ Japanese font '{font_file}' found and registered")
        except Exception as e:
            print(f"⚠ Font file found but registration failed: {e}")
            print(f"  Will use fallback font (Helvetica)")
    else:
        print(f"⚠ Japanese font '{font_file}' not found in current directory")
        print(f"  Will use fallback font (Helvetica)")
        print(f"  Note: This is OK - the application will still work")
except Exception as e:
    print(f"✗ Font test failed: {e}")

print()

# Test 8: Basic Functionality Test
print("Test 8: Basic Functionality Test")
print("-" * 70)
try:
    from snappdf.config import AppConfig
    from snappdf.core import PDFGenerator

    # Create a generator
    layout = AppConfig.get_layout("standard")
    generator = PDFGenerator(layout)

    print(f"✓ Created PDFGenerator with layout: {layout.display_name}")
    print(f"  Image count: {generator.get_image_count()}")
    print(f"  Has Excel data: {generator.has_excel_data()}")
    print(f"  Layout info: {generator.get_layout_info()}")

    # Test utility functions
    from snappdf.utils import calculate_image_dimensions, get_timestamp

    timestamp = get_timestamp()
    print(f"✓ Utility functions working")
    print(f"  Timestamp: {timestamp}")

    # Test image dimension calculation
    new_w, new_h = calculate_image_dimensions(1920, 1080, 800, 600)
    print(f"  Image resize test: (1920, 1080) -> ({new_w:.1f}, {new_h:.1f})")

except Exception as e:
    print(f"✗ Basic functionality test failed")
    print(f"  Error: {e}")
    import traceback

    traceback.print_exc()
    all_components_ok = False

print()

# Final Summary
print("=" * 70)
print("Installation Test Summary")
print("=" * 70)

if all_required_ok and all_components_ok:
    print("✓ All tests passed!")
    print()
    print("You can now run SnapPDF with:")
    print("  python snappdf_unified.py")
    print()
    print("Or run SnapSearch with:")
    print("  python SnapSearch.py")
    print()
else:
    print("✗ Some tests failed. Please install missing dependencies:")
    print("  pip install -r requirements.txt")
    print()
    sys.exit(1)

print("=" * 70)
