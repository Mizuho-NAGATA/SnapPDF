# -------------------------------------------------------------
# 1ページあたり6枚の写真をPDFに出力します。複数のフォルダから画像を選択可能。
# このプログラム「SnapPDF」は ChatGPT と共に開発し、Copilot によって改良されました。
# Copyright (c) 2023 NAGATA Mizuho, Institute of Laser Engineering, The University of Osaka.
# Created on: 2023-09-29
# Last updated on: 2026-02-04 (Class-based refactoring)
# -------------------------------------------------------------

import os
import platform
import subprocess
import threading
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from functools import lru_cache
from tkinter import Frame, Label, filedialog, messagebox

from PIL import Image, ImageTk
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image as PlatypusImage
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table

# -------------------------------------------------------------
# Cross-platform font selection
# -------------------------------------------------------------
def select_font():
    """
    Select appropriate font based on the operating system.
    Returns tuple: (pdf_font_name, gui_font_name)
    """
    system = platform.system()
    
    # Try to register fonts based on OS
    if system == "Windows":
        # Windows: Try BIZ-UDGothicR, then SimHei, then fallback
        font_attempts = [
            ("BIZ-UDGothicR", "BIZ-UDGothicR.ttc"),
            ("BIZ-UDGothicR", "BIZ-UDGothicR.ttf"),
            ("SimHei", "simhei.ttf"),
            ("Arial", None),  # System default, no registration needed
        ]
    elif system == "Darwin":  # macOS
        # macOS: Try Hiragino Sans or fallback to Helvetica
        font_attempts = [
            ("HiraginoSans", "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"),
            ("HiraginoSans", "/System/Library/Fonts/Hiragino Sans GB W3.otf"),
            ("HiraKakuProN-W3", "/System/Library/Fonts/ヒラギノ角ゴ ProN W3.otc"),
            ("Helvetica", None),  # System default, no registration needed
        ]
    else:  # Linux and others
        # Linux: Try DejaVu Sans or other common fonts
        font_attempts = [
            ("DejaVuSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
            ("LiberationSans", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"),
            ("FreeSans", "/usr/share/fonts/truetype/freefont/FreeSans.ttf"),
            ("Helvetica", None),  # Fallback
        ]
    
    # Try each font in order
    for font_name, font_path in font_attempts:
        try:
            if font_path:
                # Try to register the font
                pdfmetrics.registerFont(TTFont(font_name, font_path))
                return (font_name, font_name)
            else:
                # Use system default (Helvetica/Times-Roman are built-in to reportlab)
                return (font_name, font_name)
        except Exception:
            # Font file not found or registration failed, try next
            continue
    
    # Ultimate fallback: use reportlab's built-in Helvetica
    return ("Helvetica", "Helvetica")


# Initialize fonts
PDF_FONT_NAME, GUI_FONT_NAME = select_font()

# PDF font settings
styles = getSampleStyleSheet()
styles["Normal"].fontName = PDF_FONT_NAME
styles["Normal"].fontSize = 10
styles["Title"].fontName = PDF_FONT_NAME
styles["Title"].fontSize = 16


class SnapPDF6App:
    def __init__(self):
        self.image_paths = []  # 選択された画像パス
        self.photo_images = []  # サムネイル保持（GC対策）
        self.entries = []  # Title / Remarks

        self.root = tk.Tk()
        self.root.title("SnapPDF6")

        self.thumbnail_frame = None

        self._build_gui()

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

            label = tk.Label(frame, text=field, width=15, font=(GUI_FONT_NAME, 14))
            label.pack(side=tk.LEFT)

            entry = tk.Entry(frame, font=(GUI_FONT_NAME, 14))
            entry.pack(side=tk.LEFT)

            self.entries.append(entry)

        select_button = tk.Button(
            self.root,
            text="Select Images",
            command=self.select_images,
            font=(GUI_FONT_NAME, 14),
        )
        select_button.pack(pady=10)

        export_button = tk.Button(
            self.root,
            text="Output to PDF",
            command=self.create_pdf,
            font=(GUI_FONT_NAME, 14),
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
                    container, text=filename, wraplength=100, font=(GUI_FONT_NAME, 8)
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
        available_width = A4[1] - 2 * inch
        available_height = A4[0] - 2.5 * inch - 0.5 * inch

        new_width = available_width / 3 - 10
        new_height = new_width / image_ratio

        if new_height > available_height / 2 - 10:
            new_height = available_height / 2 - 10
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

        def add_header(canvas, doc):
            title = Paragraph(title_text, styles["Title"])
            title.wrapOn(canvas, A4[1], A4[0])
            x = (A4[1] - title.width) / 2
            y = A4[0] - inch * 1
            title.drawOn(canvas, x, y)

            page_num = canvas.getPageNumber()
            canvas.setFont(PDF_FONT_NAME, 10)
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

        available_width = A4[1] - 2 * inch
        table_data = []
        row_data = []

        for image, name in results:
            cell_content = [[image], [name]]
            cell_table = Table(cell_content)
            row_data.append(cell_table)

            if len(row_data) == 3:
                table_data.append(row_data)
                row_data = []

            if len(table_data) == 2:
                content.append(Table(table_data, colWidths=[available_width / 3] * 3))
                content.append(Spacer(1, 0.1))
                table_data = []

        if row_data:
            table_data.append(row_data)

        if table_data:
            content.append(
                Table(
                    table_data,
                    colWidths=[available_width / 3]
                    * max(len(row) for row in table_data),
                )
            )

        doc.build(content, onFirstPage=add_header, onLaterPages=add_header)

        if os.name == "nt":
            subprocess.Popen(["start", pdf_file_path], shell=True)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", pdf_file_path])
        else:
            subprocess.Popen(["xdg-open", pdf_file_path])

        messagebox.showinfo("Completed", "PDF creation is complete")

    # -------------------------------------------------------------
    # 実行
    # -------------------------------------------------------------
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    SnapPDF6App().run()
