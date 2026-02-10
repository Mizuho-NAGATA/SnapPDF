# -------------------------------------------------------------
# SnapPDF Unified - Universal Image to PDF Converter
# Combines functionality of SnapPDF, SnapPDF2, SnapPDF4, SnapPDF6, and SnapPDF15
# Allows user to select layout (images per page) via GUI
# Copyright (c) 2023 NAGATA Mizuho. Institute of Laser Engineering, The University of Osaka.
# Created on: 2026-02-10
# -------------------------------------------------------------

import os
import platform
import subprocess
import threading
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from functools import lru_cache
from tkinter import Frame, Label, filedialog, messagebox, ttk

import pandas as pd
from PIL import Image, ImageTk
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image as PlatypusImage
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

# PDF font settings
pdfmetrics.registerFont(TTFont("BIZ-UDGothicR", "BIZ-UDGothicR.ttc"))
styles = getSampleStyleSheet()
styles["Normal"].fontName = "BIZ-UDGothicR"
styles["Normal"].fontSize = 10
styles["Title"].fontName = "BIZ-UDGothicR"
styles["Title"].fontSize = 16
styles["Title"].alignment = 1  # center

# Layout presets configuration
LAYOUT_PRESETS = {
    2: {"cols": 1, "rows": 2, "name": "2 images (1x2)"},
    4: {"cols": 2, "rows": 2, "name": "4 images (2x2)"},
    5: {"cols": 5, "rows": 1, "name": "5 images (5x1)"},
    6: {"cols": 3, "rows": 2, "name": "6 images (3x2)"},
    15: {"cols": 5, "rows": 3, "name": "15 images (5x3)"},
}


class LayoutSelectionDialog:
    """Dialog for selecting the layout at startup"""

    def __init__(self, parent):
        self.result = None
        self.excel_support = False

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("SnapPDF Unified - Layout Selection")
        self.dialog.geometry("400x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (400 // 2)
        self.dialog.geometry(f"400x400+{x}+{y}")

        # Title
        title_label = tk.Label(
            self.dialog,
            text="Select Layout",
            font=("BIZ-UDGothicR", 16, "bold"),
        )
        title_label.pack(pady=20)

        # Layout selection frame
        layout_frame = tk.Frame(self.dialog)
        layout_frame.pack(pady=10, padx=20)

        self.layout_var = tk.IntVar(value=4)

        for key, preset in LAYOUT_PRESETS.items():
            rb = tk.Radiobutton(
                layout_frame,
                text=preset["name"],
                variable=self.layout_var,
                value=key,
                font=("BIZ-UDGothicR", 12),
            )
            rb.pack(anchor=tk.W, pady=5)

        # Excel support checkbox
        excel_frame = tk.Frame(self.dialog)
        excel_frame.pack(pady=10, padx=20)

        self.excel_var = tk.BooleanVar(value=False)
        excel_check = tk.Checkbutton(
            excel_frame,
            text="Enable Excel support (5 images layout only)",
            variable=self.excel_var,
            font=("BIZ-UDGothicR", 10),
        )
        excel_check.pack(anchor=tk.W)

        # Buttons
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=20)

        ok_button = tk.Button(
            button_frame,
            text="OK",
            command=self.on_ok,
            font=("BIZ-UDGothicR", 12),
            width=10,
        )
        ok_button.pack(side=tk.LEFT, padx=5)

        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            command=self.on_cancel,
            font=("BIZ-UDGothicR", 12),
            width=10,
        )
        cancel_button.pack(side=tk.LEFT, padx=5)

        # Wait for dialog to close
        parent.wait_window(self.dialog)

    def on_ok(self):
        self.result = self.layout_var.get()
        self.excel_support = self.excel_var.get()
        self.dialog.destroy()

    def on_cancel(self):
        self.result = None
        self.dialog.destroy()


class SnapPDFUnifiedApp:
    def __init__(self, layout_key, excel_support=False):
        self.layout_key = layout_key
        self.layout_config = LAYOUT_PRESETS[layout_key]
        self.excel_support = excel_support

        # State
        self.image_paths = []
        self.photo_images = []
        self.entries = []
        self.excel_data = []
        self.excel_headers = []

        # GUI
        self.root = tk.Tk()
        self.root.title(f"SnapPDF Unified - {self.layout_config['name']}")
        self.thumbnail_frame = None
        self.image_list = None

        self._build_gui()

    # =========================
    # GUI Construction
    # =========================
    def _build_gui(self):
        # Input fields (Title / Remarks)
        input_frame = tk.Frame(self.root)
        input_frame.pack(padx=10, pady=10)

        fields = ["Title", "Remarks"]
        for field in fields:
            frame = tk.Frame(input_frame)
            frame.pack(pady=5)

            label = tk.Label(frame, text=field, width=15, font=("BIZ-UDGothicR", 14))
            label.pack(side=tk.LEFT)

            entry = tk.Entry(frame, font=("BIZ-UDGothicR", 14))
            entry.pack(side=tk.LEFT)

            self.entries.append(entry)

        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        if self.excel_support and self.layout_key == 5:
            select_excel_button = tk.Button(
                button_frame,
                text="Select Excel File",
                command=self.select_excel_file,
                font=("BIZ-UDGothicR", 14),
            )
            select_excel_button.pack(side=tk.LEFT, padx=5)

        select_button = tk.Button(
            button_frame,
            text="Select Images",
            command=self.select_images,
            font=("BIZ-UDGothicR", 14),
        )
        select_button.pack(side=tk.LEFT, padx=5)

        export_button = tk.Button(
            button_frame,
            text="Output to PDF",
            command=self.create_pdf,
            font=("BIZ-UDGothicR", 14),
        )
        export_button.pack(side=tk.LEFT, padx=5)

        # Thumbnail frame
        self.thumbnail_frame = Frame(self.root)
        self.thumbnail_frame.pack(padx=10, pady=10)

    # =========================
    # Event Handlers
    # =========================
    def select_excel_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx *.xls")],
            title="Select Excel File",
        )
        if file_path:
            try:
                df = pd.read_excel(file_path)
                df = df.fillna("")
                data = df.values.tolist()

                messagebox.showinfo(
                    "Excel File Selected",
                    f"Data loading completed. Number of rows: {len(data)}",
                )

                self.excel_data = data
                self.excel_headers = df.columns.tolist()

            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"Failed to read the Excel file. Error message: {str(e)}",
                )

    def select_images(self):
        new_paths = list(
            filedialog.askopenfilenames(
                filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
            )
        )
        if new_paths:
            self.image_paths.extend(new_paths)
            messagebox.showinfo(
                "Image Selection", f"Number of selected images: {len(new_paths)}"
            )
            threading.Thread(target=self.display_thumbnails).start()

    # =========================
    # Thumbnail Generation
    # =========================
    @lru_cache(maxsize=None)
    def generate_thumbnail(self, file_path):
        image = Image.open(file_path)
        image.thumbnail((100, 100))
        return ImageTk.PhotoImage(image=image)

    def display_thumbnails(self):
        if not self.image_paths:
            return

        for widget in self.thumbnail_frame.winfo_children():
            widget.destroy()

        num_images = len(self.image_paths)
        num_columns = 10
        self.photo_images.clear()

        def update_thumbnails(start, end):
            for i in range(start, end):
                if i >= num_images:
                    return

                photo = self.generate_thumbnail(self.image_paths[i])
                self.photo_images.append(photo)

                container = Frame(self.thumbnail_frame)
                container.grid(
                    row=(i // num_columns) * 2, column=i % num_columns, padx=5, pady=5
                )

                label = Label(container, image=photo)
                label.pack()

                filename = os.path.basename(self.image_paths[i])
                name_label = Label(
                    container, text=filename, wraplength=100, font=("BIZ-UDGothicR", 8)
                )
                name_label.pack()

                self.thumbnail_frame.update_idletasks()

        with ThreadPoolExecutor() as executor:
            batch_size = 10
            for start in range(0, num_images, batch_size):
                executor.submit(update_thumbnails, start, start + batch_size)

    # =========================
    # PDF Generation
    # =========================
    def calculate_image_size(self, original_width, original_height):
        """Calculate image size based on layout configuration"""
        cols = self.layout_config["cols"]
        rows = self.layout_config["rows"]

        available_width = A4[1] - 2 * inch
        available_height = A4[0] - 2.5 * inch - 0.5 * inch

        image_ratio = original_width / original_height

        # Calculate based on columns
        if self.layout_key == 5:
            # Special handling for 5-image horizontal layout
            max_width = 150
            max_height = 150
            if image_ratio > 1:
                new_width = max_width
                new_height = int(new_width / image_ratio)
            else:
                new_height = max_height
                new_width = int(new_height * image_ratio)
        else:
            # General layout calculation
            new_width = available_width / cols - 10
            new_height = new_width / image_ratio

            if new_height > available_height / rows - 10:
                new_height = available_height / rows - 10
                new_width = new_height * image_ratio

        return new_width, new_height

    def process_image_for_pdf(self, file_path):
        """Process image for PDF with layout-specific sizing"""
        image = Image.open(file_path)
        original_width, original_height = image.size

        new_width, new_height = self.calculate_image_size(
            original_width, original_height
        )

        return (
            PlatypusImage(file_path, width=new_width, height=new_height),
            Paragraph(os.path.basename(file_path), styles["Normal"]),
        )

    def create_pdf(self):
        if not self.image_paths:
            messagebox.showerror("Error", "Please select images")
            return

        now = datetime.now()
        pdf_file_path = now.strftime("%y%m%d_%H%M%S") + ".pdf"

        doc = SimpleDocTemplate(
            pdf_file_path,
            pagesize=landscape(A4),
            topMargin=1.5 * inch,
            bottomMargin=0.1 * inch,
        )
        content = []

        title_text = self.entries[0].get()
        remarks_text = self.entries[1].get()

        def add_header(canvas, doc_obj):
            title = Paragraph(title_text, styles["Title"])
            title.wrapOn(canvas, A4[1], A4[0])
            x = (A4[1] - title.width) / 2
            y = A4[0] - inch * 1
            title.drawOn(canvas, x, y)

            page_num = canvas.getPageNumber()
            canvas.setFont("BIZ-UDGothicR", 10)
            canvas.setFillColor(colors.black)
            canvas.drawCentredString(
                landscape(A4)[0] / 2, inch * 0.1, f"Page {page_num}"
            )

            remarks = Paragraph(remarks_text, styles["Normal"])
            remarks.wrapOn(canvas, A4[1], A4[0])
            remarks.drawOn(canvas, inch, A4[0] - inch * 1.5)

        # Add Excel data if available (for layout 5 only)
        if self.excel_headers and self.excel_support and self.layout_key == 5:
            data_with_header = [self.excel_headers] + self.excel_data
            data_table = Table(data_with_header, colWidths=None)
            data_table._width = A4[0] - doc.leftMargin - doc.rightMargin

            table_style = [
                ("BACKGROUND", (0, 0), (-1, 0), (0.8, 0.9, 1.0)),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONT", (0, 0), (-1, -1), "BIZ-UDGothicR", 10),
            ]

            for row in range(2, len(data_with_header), 2):
                table_style.append(("BACKGROUND", (0, row), (-1, row), (0.8, 0.9, 1.0)))

            data_table.setStyle(TableStyle(table_style))
            content.append(data_table)

        # Process images in parallel
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.process_image_for_pdf, path)
                for path in self.image_paths
            ]
            results = [f.result() for f in as_completed(futures)]

        # Build PDF content based on layout
        self._build_pdf_content(content, results)

        # Generate PDF
        doc.build(content, onFirstPage=add_header, onLaterPages=add_header)

        # Open PDF
        if os.name == "nt":
            subprocess.Popen(["start", pdf_file_path], shell=True)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", pdf_file_path])
        else:
            subprocess.Popen(["xdg-open", pdf_file_path])

        messagebox.showinfo("Completed", "PDF creation is complete")

    def _build_pdf_content(self, content, results):
        """Build PDF content based on selected layout"""
        cols = self.layout_config["cols"]
        rows = self.layout_config["rows"]
        images_per_page = cols * rows
        available_width = A4[1] - 2 * inch

        if self.layout_key == 2:
            # 2 images per page (1 column x 2 rows)
            image_row = []
            name_row = []

            for img, name in results:
                image_row.append(img)
                name_row.append(name)

                if len(image_row) == 2:
                    content.append(Table([image_row, name_row]))
                    content.append(Spacer(1, 0.1))
                    image_row, name_row = [], []

            if image_row:
                content.append(Table([image_row, name_row]))

        elif self.layout_key in [4, 6]:
            # 4 images (2x2) or 6 images (3x2)
            table_data = []
            row_data = []

            for image, name in results:
                cell_content = [[image], [name]]
                cell_table = Table(cell_content)
                row_data.append(cell_table)

                if len(row_data) == cols:
                    table_data.append(row_data)
                    row_data = []

                if len(table_data) == rows:
                    content.append(Table(table_data, colWidths=[available_width / cols] * cols))
                    content.append(Spacer(1, 0.1))
                    table_data = []

            if row_data:
                table_data.append(row_data)

            if table_data:
                content.append(
                    Table(
                        table_data,
                        colWidths=[available_width / cols]
                        * max(len(row) for row in table_data),
                    )
                )

        elif self.layout_key == 5:
            # 5 images per row (horizontal layout like original SnapPDF)
            image_table_data = []
            file_name_table_data = []
            image_spacing = 4
            image_width = 150

            for image, name in results:
                image_table_data.append(image)
                file_name_table_data.append(name)

                if len(image_table_data) == 5:
                    row_data_with_spacing = []
                    for img in image_table_data:
                        row_data_with_spacing.append(Spacer(1, image_spacing))
                        row_data_with_spacing.append(img)
                        row_data_with_spacing.append(Spacer(1, image_spacing))

                    content.append(
                        Table(
                            [row_data_with_spacing],
                            colWidths=[image_spacing, image_width, image_spacing] * 5,
                        )
                    )
                    content.append(
                        Table([file_name_table_data], colWidths=[image_width] * 5)
                    )
                    image_table_data = []
                    file_name_table_data = []

            if image_table_data:
                row_data_with_spacing = []
                for img in image_table_data:
                    row_data_with_spacing.append(Spacer(1, image_spacing))
                    row_data_with_spacing.append(img)
                    row_data_with_spacing.append(Spacer(1, image_spacing))

                content.append(
                    Table(
                        [row_data_with_spacing],
                        colWidths=[image_spacing, image_width, image_spacing]
                        * len(image_table_data),
                    )
                )
                content.append(
                    Table(
                        [file_name_table_data],
                        colWidths=[image_width] * len(file_name_table_data),
                    )
                )

        elif self.layout_key == 15:
            # 15 images (5x3)
            image_spacing = 10
            col_widths = [150 + image_spacing] * 5
            image_row = []
            name_row = []

            for image, name in results:
                image_row.append(image)
                name_row.append(name)

                if len(image_row) == 5:
                    content.append(Table([image_row], colWidths=col_widths))
                    content.append(Spacer(1, 0.1))
                    content.append(Table([name_row], colWidths=col_widths))
                    content.append(Spacer(1, 0.1))
                    image_row, name_row = [], []

            if image_row:
                last_col_widths = [150 + image_spacing] * len(image_row)
                content.append(Table([image_row], colWidths=last_col_widths))
                content.append(Spacer(1, 12))
                content.append(Table([name_row], colWidths=last_col_widths))
                content.append(Spacer(1, 20))

    # =========================
    # Run Application
    # =========================
    def run(self):
        self.root.mainloop()


def main():
    """Main entry point with layout selection"""
    # Create a temporary root for the dialog
    temp_root = tk.Tk()
    temp_root.withdraw()

    # Show layout selection dialog
    dialog = LayoutSelectionDialog(temp_root)

    if dialog.result is None:
        temp_root.destroy()
        return

    layout_key = dialog.result
    excel_support = dialog.excel_support

    temp_root.destroy()

    # Create and run the main application
    app = SnapPDFUnifiedApp(layout_key, excel_support)
    app.run()


if __name__ == "__main__":
    main()
