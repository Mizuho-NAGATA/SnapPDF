# -------------------------------------------------------------
# SnapPDF Unified - Select layout to output multiple photos per page to PDF
# Images can be selected from multiple folders
# This program "SnapPDF" was developed with ChatGPT and Copilot
# Copyright (c) 2023-2026 NAGATA Mizuho
# Institute of Laser Engineering, Osaka University
# Created on: 2023-09-29
# Last updated on: 2026-02-12 (Unified version with layout selection)
# -------------------------------------------------------------

import os
import platform
import subprocess
import threading
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from functools import lru_cache
from tkinter import Frame, Label, filedialog, messagebox

import pandas as pd
from PIL import Image, ImageTk
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image as PlatypusImage,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# PDF font settings
pdfmetrics.registerFont(TTFont("BIZ-UDGothicR", "BIZ-UDGothicR.ttc"))
styles = getSampleStyleSheet()
styles["Normal"].fontName = "BIZ-UDGothicR"
styles["Normal"].fontSize = 10
styles["Title"].fontName = "BIZ-UDGothicR"
styles["Title"].fontSize = 16
styles["Title"].alignment = 1  # center


# Layout configurations: (columns, rows, description)
LAYOUT_PRESETS = {
    "2": {"cols": 1, "rows": 2, "total": 2, "name": "2 images (1×2)"},
    "4": {"cols": 2, "rows": 2, "total": 4, "name": "4 images (2×2)"},
    "5": {"cols": 5, "rows": 1, "total": 5, "name": "5 images (5×1)"},
    "6": {"cols": 3, "rows": 2, "total": 6, "name": "6 images (3×2)"},
    "15": {"cols": 5, "rows": 3, "total": 15, "name": "15 images (5×3)"},
}


class SnapPDFUnifiedApp:
    def __init__(self):
        self.image_paths = []
        self.photo_images = []
        self.entries = []
        self.excel_data = []
        self.excel_headers = []
        self.selected_layout = tk.StringVar(value="6")  # Default to 6 images

        self.root = tk.Tk()
        self.root.title("SnapPDF Unified")

        self.thumbnail_frame = None

        self._build_gui()

    # -------------------------------------------------------------
    # GUI構築
    # -------------------------------------------------------------
    def _build_gui(self):
        # Title and Remarks input
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

        # Layout selection frame
        layout_frame = tk.LabelFrame(
            self.root, text="Select Layout (Images per Page)", font=("BIZ-UDGothicR", 12)
        )
        layout_frame.pack(padx=10, pady=10, fill=tk.X)

        # Create radio buttons for each layout preset
        button_frame = tk.Frame(layout_frame)
        button_frame.pack(pady=5)

        for key in ["2", "4", "5", "6", "15"]:
            preset = LAYOUT_PRESETS[key]
            rb = tk.Radiobutton(
                button_frame,
                text=preset["name"],
                variable=self.selected_layout,
                value=key,
                font=("BIZ-UDGothicR", 12),
            )
            rb.pack(side=tk.LEFT, padx=10)

        # Excel file selection button
        select_excel_button = tk.Button(
            self.root,
            text="Select Excel File (Optional)",
            command=self.select_excel_file,
            font=("BIZ-UDGothicR", 14),
        )
        select_excel_button.pack(pady=10)

        # Image selection button
        select_button = tk.Button(
            self.root,
            text="Select Images",
            command=self.select_images,
            font=("BIZ-UDGothicR", 14),
        )
        select_button.pack(pady=10)

        # PDF export button
        export_button = tk.Button(
            self.root,
            text="Output to PDF",
            command=self.create_pdf,
            font=("BIZ-UDGothicR", 14),
        )
        export_button.pack(pady=10)

        # Thumbnail display frame
        self.thumbnail_frame = Frame(self.root)
        self.thumbnail_frame.pack(padx=10, pady=10)

    # -------------------------------------------------------------
    # Excel file selection
    # -------------------------------------------------------------
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

    # -------------------------------------------------------------
    # Image selection
    # -------------------------------------------------------------
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

    # -------------------------------------------------------------
    # Thumbnail generation (with cache)
    # -------------------------------------------------------------
    @lru_cache(maxsize=None)
    def generate_thumbnail(self, file_path):
        image = Image.open(file_path)
        image.thumbnail((100, 100))
        return ImageTk.PhotoImage(image=image)

    # -------------------------------------------------------------
    # Thumbnail display
    # -------------------------------------------------------------
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

    # -------------------------------------------------------------
    # Process image for PDF based on layout
    # -------------------------------------------------------------
    def process_image_for_pdf(self, file_path, layout_config):
        image = Image.open(file_path)
        original_width, original_height = image.size

        available_width = A4[1] - 2 * inch
        available_height = A4[0] - 2.5 * inch - 0.5 * inch

        cols = layout_config["cols"]
        rows = layout_config["rows"]

        # Calculate target dimensions
        target_width = available_width / cols - 10
        target_height = available_height / rows - 10

        image_ratio = original_width / original_height

        # Fit image within target dimensions
        new_width = target_width
        new_height = new_width / image_ratio

        if new_height > target_height:
            new_height = target_height
            new_width = new_height * image_ratio

        return (
            PlatypusImage(file_path, width=new_width, height=new_height),
            Paragraph(os.path.basename(file_path), styles["Normal"]),
        )

    # -------------------------------------------------------------
    # PDF generation
    # -------------------------------------------------------------
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
            canvas.drawCentredString(
                landscape(A4)[0] / 2, inch * 0.1, f"Page {page_num}"
            )

            remarks = Paragraph(remarks_text, styles["Normal"])
            remarks.wrapOn(canvas, A4[1], A4[0])
            remarks.drawOn(canvas, inch, A4[0] - inch * 1.5)

        # Add Excel data if available
        if self.excel_headers:
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

        # Get layout configuration
        layout_key = self.selected_layout.get()
        layout_config = LAYOUT_PRESETS[layout_key]
        cols = layout_config["cols"]
        rows = layout_config["rows"]
        images_per_page = layout_config["total"]

        # Process images in parallel (preserve order)
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.process_image_for_pdf, path, layout_config)
                for path in self.image_paths
            ]
            results = [f.result() for f in futures]

        available_width = A4[1] - 2 * inch

        # Build page layout
        table_data = []
        row_data = []

        for image, name in results:
            cell_content = [[image], [name]]
            cell_table = Table(cell_content)
            row_data.append(cell_table)

            # When a row is complete
            if len(row_data) == cols:
                table_data.append(row_data)
                row_data = []

            # When a page is complete
            if len(table_data) == rows:
                content.append(
                    Table(table_data, colWidths=[available_width / cols] * cols)
                )
                content.append(Spacer(1, 0.1))
                table_data = []

        # Add remaining images
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

        # Build PDF
        doc.build(content, onFirstPage=add_header, onLaterPages=add_header)

        # Open PDF
        if os.name == "nt":
            subprocess.Popen(["start", pdf_file_path], shell=True)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", pdf_file_path])
        else:
            subprocess.Popen(["xdg-open", pdf_file_path])

        messagebox.showinfo("Completed", "PDF creation is complete")

    # -------------------------------------------------------------
    # Run application
    # -------------------------------------------------------------
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    SnapPDFUnifiedApp().run()
