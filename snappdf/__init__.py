"""
SnapPDF - A simple and powerful tool to combine multiple images into a single PDF file.

Copyright (c) 2023-2026 NAGATA Mizuho
Institute of Laser Engineering, The University of Osaka
"""

__version__ = "2.0.0"
__author__ = "NAGATA Mizuho"
__license__ = "MIT"

from .config import AppConfig
from .core import LayoutConfig, PDFGenerator

__all__ = ["PDFGenerator", "LayoutConfig", "AppConfig"]
