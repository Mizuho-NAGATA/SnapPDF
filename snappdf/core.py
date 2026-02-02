# -------------------------------------------------------------
# Core PDF generation module for SnapPDF
# Copyright (c) 2023-2026 NAGATA Mizuho
# Institute of Laser Engineering, The University of Osaka
# -------------------------------------------------------------

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional, Tuple

import pandas as pd
from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image as PlatypusImage,
)
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from .config import AppConfig, LayoutConfig
from .utils import (
    calculate_image_dimensions,
    format_error_message,
    get_timestamp,
    validate_image_file,
)


class PDFGenerator:
    """Main PDF generator class for SnapPDF"""

    def __init__(self, layout: LayoutConfig):
        """
        Initialize PDF generator with specified layout.

        Args:
            layout: LayoutConfig object defining the page layout
        """
        self.layout = layout
        self.image_paths: List[str] = []
        self.excel_data: List[List] = []
        self.excel_headers: List[str] = []
        self.styles = None
        self._setup_fonts()
        self._setup_styles()

    def _setup_fonts(self) -> None:
        """Setup fonts for PDF generation with fallback"""
        try:
            # Try to register the Japanese font
            pdfmetrics.registerFont(
                TTFont(AppConfig.DEFAULT_FONT_NAME, AppConfig.DEFAULT_FONT_FILE)
            )
            self.font_name = AppConfig.DEFAULT_FONT_NAME
        except Exception as e:
            print(f"Warning: Could not load font {AppConfig.DEFAULT_FONT_FILE}: {e}")
            print(f"Falling back to {AppConfig.FALLBACK_FONT_NAME}")
            self.font_name = AppConfig.FALLBACK_FONT_NAME

    def _setup_styles(self) -> None:
        """Setup paragraph styles for PDF"""
        self.styles = getSampleStyleSheet()

        # Update Normal style
        self.styles["Normal"].fontName = self.font_name
        self.styles["Normal"].fontSize = AppConfig.NORMAL_FONT_SIZE

        # Update Title style
        self.styles["Title"].fontName = self.font_name
        self.styles["Title"].fontSize = AppConfig.TITLE_FONT_SIZE
        self.styles["Title"].alignment = 1  # Center alignment

    def add_images(self, image_paths: List[str]) -> Tuple[int, int]:
        """
        Add images to the generator.

        Args:
            image_paths: List of image file paths

        Returns:
            Tuple of (successful_count, failed_count)
        """
        successful = 0
        failed = 0

        for path in image_paths:
            if validate_image_file(path):
                self.image_paths.append(path)
                successful += 1
            else:
                print(f"Warning: Invalid image file: {path}")
                failed += 1

        return (successful, failed)

    def clear_images(self) -> None:
        """Clear all loaded images"""
        self.image_paths.clear()

    def remove_image(self, index: int) -> bool:
        """
        Remove an image at specified index.

        Args:
            index: Index of image to remove

        Returns:
            True if successful, False otherwise
        """
        try:
            if 0 <= index < len(self.image_paths):
                del self.image_paths[index]
                return True
            return False
        except Exception:
            return False

    def move_image(self, from_index: int, to_index: int) -> bool:
        """
        Move an image from one position to another.

        Args:
            from_index: Current index of image
            to_index: Target index

        Returns:
            True if successful, False otherwise
        """
        try:
            if 0 <= from_index < len(self.image_paths) and 0 <= to_index < len(
                self.image_paths
            ):
                image = self.image_paths.pop(from_index)
                self.image_paths.insert(to_index, image)
                return True
            return False
        except Exception:
            return False

    def load_excel_data(self, excel_path: str) -> bool:
        """
        Load data from Excel file.

        Args:
            excel_path: Path to Excel file

        Returns:
            True if successful, False otherwise
        """
        try:
            df = pd.read_excel(excel_path)
            df = df.fillna("")  # Convert missing values to empty strings
            self.excel_data = df.values.tolist()
            self.excel_headers = df.columns.tolist()
            return True
        except Exception as e:
            print(f"Error loading Excel file: {format_error_message(e)}")
            return False

    def clear_excel_data(self) -> None:
        """Clear loaded Excel data"""
        self.excel_data.clear()
        self.excel_headers.clear()

    def _process_image_for_pdf(
        self, file_path: str, max_width: float, max_height: float
    ) -> Tuple[PlatypusImage, Paragraph]:
        """
        Process a single image for PDF inclusion.

        Args:
            file_path: Path to image file
            max_width: Maximum width for image
            max_height: Maximum height for image

        Returns:
            Tuple of (PlatypusImage, Paragraph with filename)
        """
        try:
            # Open and get image dimensions
            with Image.open(file_path) as img:
                original_width, original_height = img.size

            # Calculate new dimensions
            new_width, new_height = calculate_image_dimensions(
                original_width, original_height, max_width, max_height
            )

            # Create ReportLab image
            pdf_image = PlatypusImage(file_path, width=new_width, height=new_height)

            # Create filename paragraph
            filename = os.path.basename(file_path)
            filename_para = Paragraph(filename, self.styles["Normal"])

            return (pdf_image, filename_para)

        except Exception as e:
            print(f"Error processing image {file_path}: {format_error_message(e)}")
            # Return a placeholder
            placeholder = Paragraph(
                f"[Error loading image: {os.path.basename(file_path)}]",
                self.styles["Normal"],
            )
            return (placeholder, placeholder)

    def _create_excel_table(self) -> Optional[Table]:
        """
        Create a table from Excel data.

        Returns:
            Table object or None if no data
        """
        if not self.excel_headers:
            return None

        # Prepare data with headers
        table_data = [self.excel_headers] + self.excel_data

        # Create table
        table = Table(table_data, colWidths=None)

        # Define table style
        table_style = [
            ("BACKGROUND", (0, 0), (-1, 0), (0.8, 0.9, 1.0)),  # Header background
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),  # Grid lines
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # Center alignment
            ("FONT", (0, 0), (-1, -1), self.font_name, AppConfig.NORMAL_FONT_SIZE),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),  # Vertical alignment
        ]

        # Add alternating row colors
        for row in range(2, len(table_data), 2):
            table_style.append(("BACKGROUND", (0, row), (-1, row), (0.95, 0.95, 0.95)))

        table.setStyle(TableStyle(table_style))

        return table

    def _add_header_footer(
        self, canvas, doc, title_text: str, remarks_text: str
    ) -> None:
        """
        Add title and page number to each page.

        Args:
            canvas: ReportLab canvas object
            doc: Document object
            title_text: Title text to display
            remarks_text: Remarks text to display
        """
        page_width, page_height = AppConfig.PAGE_SIZE

        # Add title
        if title_text:
            title = Paragraph(title_text, self.styles["Title"])
            title.wrapOn(canvas, page_width, page_height)
            x = (page_width - title.width) / 2
            y = page_height - inch * 1
            title.drawOn(canvas, x, y)

        # Add remarks
        if remarks_text:
            remarks = Paragraph(remarks_text, self.styles["Normal"])
            remarks.wrapOn(canvas, page_width, page_height)
            remarks.drawOn(canvas, inch, page_height - inch * 1.5)

        # Add page number
        page_num = canvas.getPageNumber()
        canvas.setFont(self.font_name, AppConfig.NORMAL_FONT_SIZE)
        canvas.setFillColor(colors.black)
        text = f"Page {page_num}"
        canvas.drawCentredString(page_width / 2, inch * 0.1, text)

    def generate_pdf(
        self,
        output_path: Optional[str] = None,
        title: str = "",
        remarks: str = "",
        open_after_creation: bool = True,
    ) -> Tuple[bool, str]:
        """
        Generate PDF file from loaded images and data.

        Args:
            output_path: Output PDF file path (auto-generated if None)
            title: Title text for PDF
            remarks: Remarks text for PDF
            open_after_creation: Whether to open PDF after creation

        Returns:
            Tuple of (success: bool, message: str)
        """
        # Validate we have content
        if not self.image_paths and not self.excel_data:
            return (False, "No images or Excel data to generate PDF")

        # Generate output path if not provided
        if output_path is None:
            timestamp = get_timestamp()
            output_path = f"{timestamp}.pdf"

        try:
            # Create document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=AppConfig.PAGE_SIZE,
                topMargin=AppConfig.TOP_MARGIN,
                bottomMargin=AppConfig.BOTTOM_MARGIN,
                leftMargin=AppConfig.LEFT_MARGIN,
                rightMargin=AppConfig.RIGHT_MARGIN,
            )

            content = []

            # Add Excel table if data exists
            if self.excel_headers:
                excel_table = self._create_excel_table()
                if excel_table:
                    content.append(excel_table)
                    content.append(Spacer(1, 0.2 * inch))

            # Process images if they exist
            if self.image_paths:
                content.extend(self._create_image_content())

            # Build PDF with header/footer
            doc.build(
                content,
                onFirstPage=lambda c, d: self._add_header_footer(c, d, title, remarks),
                onLaterPages=lambda c, d: self._add_header_footer(c, d, title, remarks),
            )

            # Open PDF if requested
            if open_after_creation:
                from .utils import open_file

                open_file(output_path)

            return (True, f"PDF created successfully: {output_path}")

        except Exception as e:
            error_msg = format_error_message(e)
            return (False, f"Error creating PDF: {error_msg}")

    def _create_image_content(self) -> List:
        """
        Create content list from images based on layout.

        Returns:
            List of ReportLab flowables
        """
        content = []

        # Calculate dimensions based on layout
        available_width = AppConfig.get_available_width()
        available_height = AppConfig.get_available_height()

        # Account for Excel table space if present
        if self.excel_headers:
            available_height -= 2 * inch

        images_per_row = self.layout.columns
        max_image_width = available_width / images_per_row - AppConfig.IMAGE_SPACING
        max_image_height = available_height / self.layout.rows - AppConfig.IMAGE_SPACING

        # Process images in parallel
        processed_images = []
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(
                    self._process_image_for_pdf,
                    path,
                    max_image_width,
                    max_image_height,
                )
                for path in self.image_paths
            ]
            processed_images = [future.result() for future in as_completed(futures)]

        # Organize images into rows
        image_table_data = []
        filename_table_data = []

        for i, (img, filename) in enumerate(processed_images):
            image_table_data.append(img)
            filename_table_data.append(filename)

            # Create table when we have enough images for a row or at the end
            if (
                len(image_table_data) == images_per_row
                or i == len(processed_images) - 1
            ):
                # Calculate column widths
                col_widths = [max_image_width] * len(image_table_data)

                # Add image row
                content.append(Table([image_table_data], colWidths=col_widths))
                content.append(Spacer(1, 0.1 * inch))

                # Add filename row
                content.append(Table([filename_table_data], colWidths=col_widths))
                content.append(Spacer(1, 0.2 * inch))

                # Reset for next row
                image_table_data = []
                filename_table_data = []

        return content

    def get_image_count(self) -> int:
        """Get number of loaded images"""
        return len(self.image_paths)

    def has_excel_data(self) -> bool:
        """Check if Excel data is loaded"""
        return len(self.excel_headers) > 0

    def get_layout_info(self) -> str:
        """Get layout information string"""
        return f"{self.layout.display_name} - {self.layout.description}"
