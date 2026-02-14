# -------------------------------------------------------------
# Outputs 2 photos per page to PDF. Images can be selected from
# multiple folders. This program "SnapPDF2" was developed with
# the assistance of ChatGPT and Copilot.
# Copyright (c) 2023 NAGATA Mizuho
# Institute of Laser Engineering, Osaka University.
# Created on: 2023-09-29
# Last updated on: 2026-02-04 (Class-based refactoring)
# -------------------------------------------------------------

import os
import subprocess
import threading
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from tkinter import Frame, Label, filedialog, messagebox

from PIL import Image, ImageTk
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image as PlatypusImage
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table

# PDF font settings
pdfmetrics.registerFont(TTFont("BIZ-UDGothicR", "BIZ-UDGothicR.ttc"))
styles = getSampleStyleSheet()
styles["Normal"].fontName = "BIZ-UDGothicR"
styles["Normal"].fontSize = 10
styles["Title"].fontName = "BIZ-UDGothicR"
styles["Title"].fontSize = 16


class SnapPDF2App:
    def __init__(self):
        self.image_paths = []  # 選択された画像パス
        self.photo_images = []  # サムネイル保持（GC対策）
        self.entries = []  # Title / Remarks

        self.root = tk.Tk()
        self.root.title("SnapPDF2")

        self.thumbnail_frame = None

        self._build_gui()

    def _get_safe_pdf_path(self, base_name):
        """
        Get a safe path for PDF file with collision detection.
        Tries Desktop first, then Documents, then Home directory.
        """
        home_dir = Path.home()
        
        # Try Desktop first
        possible_dirs = [
            home_dir / "Desktop",
            home_dir / "Documents", 
            home_dir
        ]
        
        save_dir = None
        for directory in possible_dirs:
            if directory.exists() and os.access(directory, os.W_OK):
                save_dir = directory
                break
        
        if save_dir is None:
            raise PermissionError("No writable directory found for saving PDF")
        
        # Generate unique filename with counter if file exists or is locked
        counter = 0
        while True:
            if counter == 0:
                filename = f"{base_name}.pdf"
            else:
                filename = f"{base_name}_{counter}.pdf"
            
            pdf_path = save_dir / filename
            
            # Check if file exists and can be written
            if not pdf_path.exists():
                return str(pdf_path)
            
            # Try next counter if file exists (might be locked)
            counter += 1
            
            # Safety limit
            if counter > 100:
                raise RuntimeError("Could not find available filename for PDF")

    # -------------------------------------------------------------
    # GUI構築
    # -------------------------------------------------------------
    def _build_gui(self):
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

        select_button = tk.Button(
            self.root,
            text="Select Images",
            command=self.select_images,
            font=("BIZ-UDGothicR", 14),
        )
        select_button.pack(pady=10)

        export_button = tk.Button(
            self.root,
            text="Output to PDF",
            command=self.create_pdf,
            font=("BIZ-UDGothicR", 14),
        )
        export_button.pack(pady=10)

        self.thumbnail_frame = Frame(self.root)
        self.thumbnail_frame.pack(padx=10, pady=10)

    # -------------------------------------------------------------
    # 画像選択
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
    # サムネイル生成（キャッシュ付き）
    # -------------------------------------------------------------
    @lru_cache(maxsize=None)
    def generate_thumbnail(self, file_path):
        image = Image.open(file_path)
        image.thumbnail((100, 100))
        return ImageTk.PhotoImage(image=image)

    # -------------------------------------------------------------
    # サムネイル表示
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
    # PDF用画像処理
    # -------------------------------------------------------------
    def process_image_for_pdf(self, file_path):
        image = Image.open(file_path)
        original_width, original_height = image.size

        image_ratio = original_width / original_height
        new_width = (A4[1] - 2 * inch) / 2 - 10
        new_height = new_width / image_ratio

        if new_height > (A4[0] - 2.5 * inch - 0.5 * inch - 10):
            new_height = A4[0] - 2.5 * inch - 0.5 * inch - 10
            new_width = new_height * image_ratio

        return (
            PlatypusImage(file_path, width=new_width, height=new_height),
            Paragraph(os.path.basename(file_path), styles["Normal"]),
        )

    # -------------------------------------------------------------
    # PDF生成
    # -------------------------------------------------------------
    def create_pdf(self):
        if not self.image_paths:
            messagebox.showerror("Error", "Please select images")
            return

        try:
            now = datetime.now()
            timestamp = now.strftime("%y%m%d_%H%M%S")
            
            # Get safe path for PDF file
            pdf_file_path = self._get_safe_pdf_path(timestamp)

            doc = SimpleDocTemplate(
                pdf_file_path,
                pagesize=landscape(A4),
                topMargin=1.5 * inch,
                bottomMargin=0.1 * inch,
            )
            content = []

            title_text = self.entries[0].get()
            remarks_text = self.entries[1].get()

            def add_header(canvas, doc):
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

            # 並列で画像処理
            with ThreadPoolExecutor() as executor:
                futures = [
                    executor.submit(self.process_image_for_pdf, path)
                    for path in self.image_paths
                ]
                results = [f.result() for f in as_completed(futures)]

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

            doc.build(content, onFirstPage=add_header, onLaterPages=add_header)

            if os.name == "nt":
                subprocess.Popen(["start", pdf_file_path], shell=True)
            else:
                subprocess.Popen(["open", pdf_file_path])

            # Show success message with file location
            messagebox.showinfo(
                "Completed", 
                f"PDF creation is complete\nSaved to: {pdf_file_path}"
            )
            
        except PermissionError as e:
            messagebox.showerror(
                "Permission Error",
                f"Could not save PDF file: {str(e)}\n\n"
                "Please ensure you have write permissions to your Desktop or Documents folder."
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"An error occurred while creating PDF: {str(e)}"
            )

    # -------------------------------------------------------------
    # 実行
    # -------------------------------------------------------------
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    SnapPDF2App().run()
