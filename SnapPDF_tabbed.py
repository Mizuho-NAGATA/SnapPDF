# -*- coding: utf-8 -*-
# -------------------------------------------------------------
# SnapPDF Tabbed - Unified interface with PDF creation and search
# Multi-platform font support with automatic OS detection
# This program "SnapPDF" was developed with ChatGPT and Copilot
# Copyright (c) 2023-2026 NAGATA Mizuho
# Institute of Laser Engineering, Osaka University
# Created on: 2023-09-29
# Last updated on: 2026-02-12 (Tabbed interface with multi-platform fonts)
# -------------------------------------------------------------

import csv
import os
import platform
import subprocess
import threading
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from functools import lru_cache
from tkinter import Frame, Label, filedialog, messagebox, ttk

import pandas as pd
from PIL import Image, ImageTk
from PyPDF2 import PdfReader
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


# =============================================================================
# Multi-platform font configuration
# =============================================================================
def select_font_for_pdf():
    """
    Select appropriate font for PDF generation based on OS.
    Returns (font_name, font_file_path) tuple.
    """
    system = platform.system()
    
    if system == "Windows":
        # Windows: Try Japanese fonts
        font_candidates = [
            ("MS-Gothic", "msgothic.ttc"),
            ("Yu-Gothic", "YuGothR.ttc"),
            ("BIZ-UDGothicR", "BIZ-UDGothicR.ttc"),
        ]
    elif system == "Darwin":  # macOS
        font_candidates = [
            ("Hiragino-Sans", "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"),
            ("Hiragino-Kaku", "/System/Library/Fonts/Hiragino Sans GB.ttc"),
            ("Arial-Unicode", "/Library/Fonts/Arial Unicode.ttf"),
        ]
    else:  # Linux
        font_candidates = [
            ("NotoSansCJK", "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
            ("TakaoPGothic", "/usr/share/fonts/truetype/takao-gothic/TakaoPGothic.ttf"),
            ("IPAGothic", "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"),
            ("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        ]
    
    # Try to register the first available font
    for font_name, font_path in font_candidates:
        try:
            # Try with absolute path first
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont(font_name, font_path))
                return font_name
            # Try without path (system fonts)
            pdfmetrics.registerFont(TTFont(font_name, font_path.split("/")[-1]))
            return font_name
        except Exception:
            continue
    
    # Fallback to Helvetica (built-in)
    return "Helvetica"


def select_font_for_gui():
    """
    Select appropriate font for GUI based on OS.
    Returns (font_family, size) tuple.
    """
    system = platform.system()
    
    if system == "Windows":
        return ("Yu Gothic UI", 11)
    elif system == "Darwin":  # macOS
        return ("Hiragino Sans", 13)
    else:  # Linux
        return ("Noto Sans CJK JP", 11)


# Initialize PDF font
PDF_FONT_NAME = select_font_for_pdf()
styles = getSampleStyleSheet()
styles["Normal"].fontName = PDF_FONT_NAME
styles["Normal"].fontSize = 10
styles["Title"].fontName = PDF_FONT_NAME
styles["Title"].fontSize = 16
styles["Title"].alignment = 1  # center

# Initialize GUI font
GUI_FONT_FAMILY, GUI_FONT_SIZE = select_font_for_gui()


# Layout configurations: (columns, rows, description)
# Using Unicode multiplication sign (U+00D7) instead of ASCII 'x'
LAYOUT_PRESETS = {
    "2": {"cols": 2, "rows": 1, "total": 2, "name": "2 images (2\u00D71)"},
    "4": {"cols": 2, "rows": 2, "total": 4, "name": "4 images (2\u00D72)"},
    "6": {"cols": 3, "rows": 2, "total": 6, "name": "6 images (3\u00D72)"},
    "15": {"cols": 5, "rows": 3, "total": 15, "name": "15 images (5\u00D73)"},
}


# =============================================================================
# SnapPDF Tab - PDF Creation
# =============================================================================
class SnapPDFTab:
    def __init__(self, parent):
        self.parent = parent
        self.image_paths = []
        self.photo_images = []
        self.entries = []
        self.excel_data = []
        self.excel_headers = []
        self.selected_layout = tk.StringVar(value="6")  # Default to 6 images
        self.thumbnail_canvas = None
        self.thumbnail_inner_frame = None
        self.thumbnail_vscroll = None
        
        self._build_gui()
    
    def _build_gui(self):
        # Main frame with scrollbar
        main_frame = Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title and Remarks input
        input_frame = tk.Frame(main_frame)
        input_frame.pack(padx=10, pady=10)
        
        fields = ["Title", "Remarks"]
        for field in fields:
            frame = tk.Frame(input_frame)
            frame.pack(pady=5)
            
            label = tk.Label(frame, text=field, width=15, 
                           font=(GUI_FONT_FAMILY, GUI_FONT_SIZE))
            label.pack(side=tk.LEFT)
            
            entry = tk.Entry(frame, font=(GUI_FONT_FAMILY, GUI_FONT_SIZE))
            entry.pack(side=tk.LEFT)
            
            self.entries.append(entry)
        
        # Layout selection frame
        layout_frame = tk.LabelFrame(
            main_frame, text="Select Layout (Images per Page)", 
            font=(GUI_FONT_FAMILY, GUI_FONT_SIZE)
        )
        layout_frame.pack(padx=10, pady=10, fill=tk.X)
        
        # Create radio buttons for each layout preset
        button_frame = tk.Frame(layout_frame)
        button_frame.pack(pady=5)
        
        # Note: removed the 5 images option as requested
        for key in ["2", "4", "6", "15"]:
            preset = LAYOUT_PRESETS[key]
            rb = tk.Radiobutton(
                button_frame,
                text=preset["name"],
                variable=self.selected_layout,
                value=key,
                font=(GUI_FONT_FAMILY, GUI_FONT_SIZE),
            )
            rb.pack(side=tk.LEFT, padx=10)
        
        # Excel file selection button
        select_excel_button = tk.Button(
            main_frame,
            text="Select Excel File (Optional)",
            command=self.select_excel_file,
            font=(GUI_FONT_FAMILY, GUI_FONT_SIZE),
        )
        select_excel_button.pack(pady=10)
        
        # Image selection button
        select_button = tk.Button(
            main_frame,
            text="Select Images",
            command=self.select_images,
            font=(GUI_FONT_FAMILY, GUI_FONT_SIZE),
        )
        select_button.pack(pady=10)
        
        # PDF export button
        export_button = tk.Button(
            main_frame,
            text="Output to PDF",
            command=self.create_pdf,
            font=(GUI_FONT_FAMILY, GUI_FONT_SIZE),
        )
        export_button.pack(pady=10)
        
        # Thumbnail display frame with scrollbar (canvas + inner frame)
        thumb_container = Frame(main_frame)
        thumb_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas for scrolling
        canvas = tk.Canvas(thumb_container, height=260)
        vscroll = tk.Scrollbar(thumb_container, orient=tk.VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=vscroll.set)
        
        vscroll.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        inner_frame = Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        
        # Update scroll region when inner_frame changes
        def _on_frame_config(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        inner_frame.bind("<Configure>", _on_frame_config)
        
        # Mousewheel support when hovering thumbnails
        def _on_enter(event):
            # bind to the canvas so wheel works when pointer is over the thumbnails area
            canvas.bind_all("<MouseWheel>", self._on_mousewheel)
            canvas.bind_all("<Button-4>", self._on_mousewheel)  # Linux
            canvas.bind_all("<Button-5>", self._on_mousewheel)
        
        def _on_leave(event):
            canvas.unbind_all("<MouseWheel>")
            canvas.unbind_all("<Button-4>")
            canvas.unbind_all("<Button-5>")
        
        inner_frame.bind("<Enter>", _on_enter)
        inner_frame.bind("<Leave>", _on_leave)
        
        self.thumbnail_canvas = canvas
        self.thumbnail_inner_frame = inner_frame
        self.thumbnail_vscroll = vscroll
    
    def _on_mousewheel(self, event):
        # Cross-platform mousewheel handling
        system = platform.system()
        if system == "Darwin":
            delta = int(-1 * (event.delta))
        else:
            # On Windows event.delta is multiple of 120; on many Linux setups Button-4/5 used instead
            if hasattr(event, "num"):
                # Button-4 (up) or Button-5 (down)
                if event.num == 4:
                    self.thumbnail_canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    self.thumbnail_canvas.yview_scroll(1, "units")
                return
            else:
                delta = int(-1 * (event.delta / 120))
        self.thumbnail_canvas.yview_scroll(delta, "units")
    
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
            # Ensure thumbnail generation and GUI updates happen in main thread
            # (creating ImageTk.PhotoImage from other threads can be unsafe)
            self.display_thumbnails()
    
    @lru_cache(maxsize=None)
    def generate_thumbnail(self, file_path):
        image = Image.open(file_path)
        image.thumbnail((100, 100))
        return ImageTk.PhotoImage(image=image)
    
    def display_thumbnails(self):
        if not self.image_paths:
            return
        
        # Clear previous thumbnails
        for widget in self.thumbnail_inner_frame.winfo_children():
            widget.destroy()
        
        num_images = len(self.image_paths)
        num_columns = 10
        self.photo_images.clear()
        
        # Build thumbnails sequentially (safe for Tkinter)
        for i in range(num_images):
            photo = self.generate_thumbnail(self.image_paths[i])
            # Keep reference to prevent GC
            self.photo_images.append(photo)
            
            container = Frame(self.thumbnail_inner_frame)
            container.grid(
                row=(i // num_columns) * 2, column=i % num_columns, padx=5, pady=5
            )
            
            label = Label(container, image=photo)
            label.pack()
            
            filename = os.path.basename(self.image_paths[i])
            name_label = Label(
                container, text=filename, wraplength=100, 
                font=(GUI_FONT_FAMILY, 8)
            )
            name_label.pack()
            
            # Force redraw occasionally
            if i % 20 == 0:
                self.thumbnail_inner_frame.update_idletasks()
        
        # Update scrollregion explicitly
        self.thumbnail_canvas.configure(scrollregion=self.thumbnail_canvas.bbox("all"))
    
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
            canvas.setFont(PDF_FONT_NAME, 10)
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
                ("FONT", (0, 0), (-1, -1), PDF_FONT_NAME, 10),
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


# =============================================================================
# PDF Search Tab
# =============================================================================
class PDFSearchTab:
    def __init__(self, parent):
        self.parent = parent
        self.keyword_entry = None
        self.and_checkbox_var = tk.BooleanVar(value=True)
        
        self._build_gui()
    
    def _build_gui(self):
        main_frame = Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        label = tk.Label(
            main_frame,
            text="Search keywords\n(separate with space, supports Japanese):",
            font=(GUI_FONT_FAMILY, GUI_FONT_SIZE),
        )
        label.pack(pady=10)
        
        self.keyword_entry = tk.Entry(main_frame, font=(GUI_FONT_FAMILY, GUI_FONT_SIZE))
        self.keyword_entry.pack(pady=5)
        
        and_checkbox = tk.Checkbutton(
            main_frame,
            text="AND search",
            font=(GUI_FONT_FAMILY, GUI_FONT_SIZE),
            variable=self.and_checkbox_var,
        )
        and_checkbox.pack(pady=5)
        
        search_button = tk.Button(
            main_frame,
            text="Select directory\nOutput search results to CSV",
            font=(GUI_FONT_FAMILY, GUI_FONT_SIZE),
            command=self.search_pdf,
        )
        search_button.pack(pady=10)
    
    def search_pdf(self):
        directory = filedialog.askdirectory(title="Select directory to search")
        if not directory:
            return
        
        keywords = self.keyword_entry.get().split()
        if not keywords:
            messagebox.showerror("Error", "Please enter at least one keyword")
            return
        
        and_search = self.and_checkbox_var.get()
        results = []
        
        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.lower().endswith(".pdf"):
                    pdf_path = os.path.join(root, filename)
                    
                    try:
                        reader = PdfReader(pdf_path)
                    except Exception:
                        continue
                    
                    found = False
                    
                    for page in reader.pages:
                        text = page.extract_text() or ""
                        
                        if and_search:
                            if all(k in text for k in keywords):
                                found = True
                                break
                        else:
                            if any(k in text for k in keywords):
                                found = True
                                break
                    
                    if found:
                        results.append((filename, pdf_path, keywords))
        
        self.export_csv(results)
        self.show_results(results)
    
    def export_csv(self, results):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = f"search_results_{timestamp}.csv"
        
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["File name", "Location", "Keywords"])
            
            for filename, location, keywords in results:
                writer.writerow([filename, location, ", ".join(keywords)])
    
    def show_results(self, results):
        win = tk.Toplevel(self.parent)
        win.title("PDF Search Results")
        
        if not results:
            label = tk.Label(win, text="No keywords were found", 
                           font=(GUI_FONT_FAMILY, GUI_FONT_SIZE))
            label.pack()
            return
        
        header = tk.Label(
            win, text="PDF files where keywords were found:", 
            font=(GUI_FONT_FAMILY, GUI_FONT_SIZE)
        )
        header.pack()
        
        # Add scrollbar for results
        frame = Frame(win)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set,
                            font=(GUI_FONT_FAMILY, 10))
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)
        
        for filename, location, keywords in results:
            text_widget.insert(tk.END, f"File: {filename}\n")
            text_widget.insert(tk.END, f"Path: {location}\n")
            text_widget.insert(tk.END, f"Keywords: {', '.join(keywords)}\n")
            text_widget.insert(tk.END, "-" * 50 + "\n\n")
        
        text_widget.config(state=tk.DISABLED)


# =============================================================================
# Main Application with Tabs
# =============================================================================
class SnapPDFTabbedApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SnapPDF - Unified PDF Tools")
        self.root.geometry("800x700")
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs
        pdf_creation_tab = Frame(self.notebook)
        pdf_search_tab = Frame(self.notebook)
        
        self.notebook.add(pdf_creation_tab, text="  PDF Creation  ")
        self.notebook.add(pdf_search_tab, text="  PDF Search  ")
        
        # Initialize tab contents
        self.snap_pdf = SnapPDFTab(pdf_creation_tab)
        self.pdf_search = PDFSearchTab(pdf_search_tab)
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = SnapPDFTabbedApp()
    app.run()
