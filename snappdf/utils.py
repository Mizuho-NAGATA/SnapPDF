# -------------------------------------------------------------
# Utility functions for SnapPDF
# Copyright (c) 2023-2026 NAGATA Mizuho
# Institute of Laser Engineering, The University of Osaka
# -------------------------------------------------------------

import os
import subprocess
import sys
from datetime import datetime
from typing import Optional, Tuple

from PIL import Image


def get_timestamp() -> str:
    """
    Get current timestamp in format suitable for filenames.

    Returns:
        str: Timestamp in format YYMMDD_HHMMSS
    """
    return datetime.now().strftime("%y%m%d_%H%M%S")


def open_file(file_path: str) -> None:
    """
    Open a file with the default application.

    Args:
        file_path: Path to the file to open
    """
    try:
        if os.name == "nt":  # Windows
            os.startfile(file_path)
        elif sys.platform == "darwin":  # macOS
            subprocess.Popen(["open", file_path])
        else:  # Linux and other Unix-like systems
            subprocess.Popen(["xdg-open", file_path])
    except Exception as e:
        print(f"Error opening file: {e}")


def calculate_image_dimensions(
    original_width: int,
    original_height: int,
    max_width: float,
    max_height: float,
    maintain_aspect_ratio: bool = True,
) -> Tuple[float, float]:
    """
    Calculate new image dimensions while maintaining aspect ratio.

    Args:
        original_width: Original image width
        original_height: Original image height
        max_width: Maximum allowed width
        max_height: Maximum allowed height
        maintain_aspect_ratio: Whether to maintain aspect ratio

    Returns:
        Tuple of (new_width, new_height)
    """
    if not maintain_aspect_ratio:
        return (max_width, max_height)

    # Calculate aspect ratio
    aspect_ratio = original_width / original_height

    # Determine which dimension to constrain
    if aspect_ratio > 1:  # Landscape
        new_width = min(max_width, original_width)
        new_height = new_width / aspect_ratio

        # If height exceeds max, recalculate based on height
        if new_height > max_height:
            new_height = max_height
            new_width = new_height * aspect_ratio
    else:  # Portrait or square
        new_height = min(max_height, original_height)
        new_width = new_height * aspect_ratio

        # If width exceeds max, recalculate based on width
        if new_width > max_width:
            new_width = max_width
            new_height = new_width / aspect_ratio

    return (new_width, new_height)


def resize_image_for_thumbnail(
    image_path: str, max_size: Tuple[int, int] = (100, 100)
) -> Optional[Image.Image]:
    """
    Resize image for thumbnail display.

    Args:
        image_path: Path to the image file
        max_size: Maximum size as (width, height)

    Returns:
        PIL Image object or None if error
    """
    try:
        image = Image.open(image_path)
        image.thumbnail(max_size, Image.LANCZOS)
        return image
    except Exception as e:
        print(f"Error creating thumbnail for {image_path}: {e}")
        return None


def get_image_dimensions(image_path: str) -> Optional[Tuple[int, int]]:
    """
    Get dimensions of an image file.

    Args:
        image_path: Path to the image file

    Returns:
        Tuple of (width, height) or None if error
    """
    try:
        with Image.open(image_path) as img:
            return img.size
    except Exception as e:
        print(f"Error reading image dimensions for {image_path}: {e}")
        return None


def validate_file_path(file_path: str) -> bool:
    """
    Validate if a file path exists and is a file.

    Args:
        file_path: Path to validate

    Returns:
        True if valid, False otherwise
    """
    return os.path.isfile(file_path)


def validate_image_file(file_path: str) -> bool:
    """
    Validate if a file is a valid image.

    Args:
        file_path: Path to the image file

    Returns:
        True if valid image, False otherwise
    """
    if not validate_file_path(file_path):
        return False

    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except Exception:
        return False


def get_file_size_mb(file_path: str) -> float:
    """
    Get file size in megabytes.

    Args:
        file_path: Path to the file

    Returns:
        File size in MB
    """
    try:
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)
    except Exception:
        return 0.0


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing invalid characters.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, "_")
    return filename


def truncate_text(text: str, max_length: int = 50) -> str:
    """
    Truncate text to specified length with ellipsis.

    Args:
        text: Text to truncate
        max_length: Maximum length

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def format_error_message(error: Exception) -> str:
    """
    Format an exception into a user-friendly error message.

    Args:
        error: Exception object

    Returns:
        Formatted error message
    """
    error_type = type(error).__name__
    error_msg = str(error)
    return f"{error_type}: {error_msg}"
