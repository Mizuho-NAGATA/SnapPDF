# -------------------------------------------------------------
# Configuration module for SnapPDF
# Copyright (c) 2023-2026 NAGATA Mizuho
# Institute of Laser Engineering, The University of Osaka
# -------------------------------------------------------------

from dataclasses import dataclass
from typing import Tuple

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import inch


@dataclass
class LayoutConfig:
    """Configuration for PDF layout"""

    name: str
    display_name: str
    images_per_page: int
    columns: int
    rows: int
    description: str

    @property
    def images_per_row(self) -> int:
        """Number of images per row"""
        return self.columns


class AppConfig:
    """Application-wide configuration"""

    # Available layouts
    LAYOUTS = {
        "large": LayoutConfig(
            name="large",
            display_name="Large (2 per page)",
            images_per_page=2,
            columns=2,
            rows=1,
            description="2 photos per page - Best for detailed viewing",
        ),
        "medium": LayoutConfig(
            name="medium",
            display_name="Medium (4 per page)",
            images_per_page=4,
            columns=2,
            rows=2,
            description="4 photos per page - Balanced size",
        ),
        "standard": LayoutConfig(
            name="standard",
            display_name="Standard (6 per page)",
            images_per_page=6,
            columns=3,
            rows=2,
            description="6 photos per page - Good balance",
        ),
        "compact": LayoutConfig(
            name="compact",
            display_name="Compact (15 per page)",
            images_per_page=15,
            columns=5,
            rows=3,
            description="15 photos per page - Maximum density",
        ),
        "excel": LayoutConfig(
            name="excel",
            display_name="Excel + Images (5 per page)",
            images_per_page=5,
            columns=5,
            rows=1,
            description="Excel data with images below",
        ),
    }

    # PDF settings
    PAGE_SIZE = landscape(A4)
    TOP_MARGIN = 1.5 * inch
    BOTTOM_MARGIN = 0.1 * inch
    LEFT_MARGIN = 1.0 * inch
    RIGHT_MARGIN = 1.0 * inch

    # Font settings
    DEFAULT_FONT_NAME = "BIZ-UDGothicR"
    DEFAULT_FONT_FILE = "BIZ-UDGothicR.ttc"
    FALLBACK_FONT_NAME = "Helvetica"
    TITLE_FONT_SIZE = 16
    NORMAL_FONT_SIZE = 10

    # Image settings
    MAX_THUMBNAIL_SIZE = (100, 100)
    IMAGE_SPACING = 10
    MAX_IMAGE_WIDTH = 200
    MAX_IMAGE_HEIGHT = 200

    # GUI settings
    WINDOW_TITLE = "SnapPDF - Unified Image to PDF Converter"
    THUMBNAIL_COLUMNS = 10
    DEFAULT_BUTTON_FONT = ("BIZ-UDGothicR", 14)

    # File settings
    SUPPORTED_IMAGE_FORMATS = [
        ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff"),
        ("JPEG files", "*.jpg *.jpeg"),
        ("PNG files", "*.png"),
        ("BMP files", "*.bmp"),
        ("All files", "*.*"),
    ]

    SUPPORTED_EXCEL_FORMATS = [
        ("Excel files", "*.xlsx *.xls"),
        ("XLSX files", "*.xlsx"),
        ("XLS files", "*.xls"),
        ("All files", "*.*"),
    ]

    @classmethod
    def get_layout(cls, layout_name: str) -> LayoutConfig:
        """Get layout configuration by name"""
        return cls.LAYOUTS.get(layout_name, cls.LAYOUTS["standard"])

    @classmethod
    def get_layout_names(cls) -> list:
        """Get list of available layout names"""
        return list(cls.LAYOUTS.keys())

    @classmethod
    def get_layout_display_names(cls) -> list:
        """Get list of layout display names for GUI"""
        return [layout.display_name for layout in cls.LAYOUTS.values()]

    @classmethod
    def get_available_width(cls) -> float:
        """Calculate available width for content"""
        return cls.PAGE_SIZE[0] - cls.LEFT_MARGIN - cls.RIGHT_MARGIN

    @classmethod
    def get_available_height(cls) -> float:
        """Calculate available height for content"""
        return cls.PAGE_SIZE[1] - cls.TOP_MARGIN - cls.BOTTOM_MARGIN
