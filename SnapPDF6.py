# -------------------------------------------------------------
# 6 photos per page to pdf. You can select images from multiple folders.
# This program "SnapPDF" was developed with the assistance of ChatGPT.
# Copyright (c) 2023 NAGATA Mizuho, Institute of Laser Engineering, Osaka University.
# Created on: 2023-09-29
# Last updated on: 2024-06-20
# -------------------------------------------------------------
from datetime import datetime
from PIL import Image, ImageTk
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Image as PlatypusImage, Table, Paragraph, Spacer
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import tkinter as tk
from tkinter import Tk, Label, Frame, filedialog, messagebox
import os
import subprocess
import threading

# PDF file settings
pdfmetrics.registerFont(TTFont('BIZ-UDGothicR', 'BIZ-UDGothicR.ttc'))
font_name = 'BIZ-UDGothicR'
styles = getSampleStyleSheet()
styles['Normal'].fontName = font_name
styles['Normal'].fontSize = 10
styles['Title'].fontName = font_name
styles['Title'].fontSize = 16

image_paths = []  # List of image paths

def select_images():
    new_image_paths = list(filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]))
    if new_image_paths:
        image_paths.extend(new_image_paths)
        messagebox.showinfo("Image Selection", f"Number of selected images: {len(new_image_paths)}")
        threading.Thread(target=display_thumbnails).start()  # Start thumbnail generation in a separate thread

# Create a list to store the PhotoImage objects
photo_images = []

def display_thumbnails():
    global photo_images  # Declare the list as global
    if image_paths:
        if thumbnail_frame.winfo_children():
            for widget in thumbnail_frame.winfo_children():
                widget.destroy()

        num_images = len(image_paths)
        num_columns = 10
        num_rows = (num_images + num_columns - 1) // num_columns

        for i, file_path in enumerate(image_paths):
            image = Image.open(file_path)
            image.thumbnail((100, 100))
            photo = ImageTk.PhotoImage(image=image)
            photo_images.append(photo)  # Add the PhotoImage object to the list
            label = Label(thumbnail_frame, image=photo_images[-1])  # Use the last added PhotoImage object
            label.grid(row=i // num_columns, column=i % num_columns, padx=5, pady=5)

def create_pdf():
    now = datetime.now()
    timestamp = now.strftime("%y%m%d_%H%M%S")
    pdf_file_path = timestamp + ".pdf"

    if not image_paths:
        messagebox.showerror("Error", "Please select an image")
        return

    doc = SimpleDocTemplate(pdf_file_path, pagesize=landscape(A4), topMargin=1.5 * inch, bottomMargin=0.1 * inch)

    content = []

    def add_title_and_page_number(canvas, doc, title_text, remarks_text):
        title_style = styles["Title"]
        title = Paragraph(title_text, title_style)
        title.wrapOn(canvas, A4[1], A4[0])
        x = (A4[1] - title.width) / 2
        y = A4[0] - inch * 1
        title.drawOn(canvas, x, y)

        page_num = canvas.getPageNumber()
        canvas.setFont(font_name, 10)
        canvas.setFillColor(colors.black)
        page_width, page_height = landscape(A4)
        text = f"Page {page_num}"
        canvas.drawCentredString(page_width / 2, inch * 0.1, text)

        remarks = Paragraph(remarks_text, styles["Normal"])
        remarks.wrapOn(canvas, A4[1], A4[0])
        remarks.drawOn(canvas, inch, A4[0] - inch * 1.5)

    # Calculate to maximize the size of the image
    available_width = A4[1] - 2 * inch
    available_height = A4[0] - 2.5 * inch - 0.5 * inch  # Consider the space for title, remarks, and page number

    image_table_data = []
    file_name_table_data = []

    for i, file_path in enumerate(image_paths):
        image = Image.open(file_path)
        original_width, original_height = image.size

        image_ratio = original_width / original_height
        new_width = available_width / 3 - 10  # Display in 3 columns, with space in between
        new_height = new_width / image_ratio

        # Check if the image fits on the page
        if new_height > available_height / 2 - 10:  # Display in 2 rows, with space in between
            new_height = available_height / 2 - 10  # Display in 2 rows, with space in between
            new_width = new_height * image_ratio

        image_table_data.append(PlatypusImage(file_path, width=new_width, height=new_height))
        file_name_table_data.append(Paragraph(os.path.basename(file_path), styles['Normal']))

        # When 3 images are gathered or it's the last image, create a table and add it to content
        if len(image_table_data) == 3 or i == len(image_paths) - 1:
            content.append(Table([image_table_data], colWidths=[available_width / 3] * len(image_table_data)))  # Add image table
            content.append(Spacer(1, 0.1))  # Add minimal space between image and file name
            content.append(Table([file_name_table_data], colWidths=[available_width / 3] * len(file_name_table_data)))  # Add file name table
            content.append(Spacer(1, 0.1))  # Add space between lines
            # Clear the lists
            image_table_data = []
            file_name_table_data = []

    title_text = entries[0].get()
    remarks_text = entries[1].get()

    doc.build(content, onFirstPage=lambda canvas, doc: add_title_and_page_number(canvas, doc, title_text, remarks_text),
              onLaterPages=lambda canvas, doc: add_title_and_page_number(canvas, doc, title_text, remarks_text))

    if os.name == 'nt':
        subprocess.Popen(["start", pdf_file_path], shell=True)
    else:
        subprocess.Popen(["open", pdf_file_path])

    messagebox.showinfo("Completed", "PDF creation is complete")

root = tk.Tk()
root.title("Snap PDF6")

input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=10)

fields = ["Title", "Remarks"]
entries = []

for field in fields:
    frame = tk.Frame(input_frame)
    frame.pack(pady=5)

    label = tk.Label(frame, text=field, width=15, font=("BIZ-UDGothicR", 14))
    label.pack(side=tk.LEFT)

    entry = tk.Entry(frame, font=("BIZ-UDGothicR", 14))
    entry.pack(side=tk.LEFT)

    entries.append(entry)

select_button = tk.Button(root, text="Select Images", command=select_images, font=("BIZ-UDGothicR", 14))
select_button.pack(pady=10)

export_button = tk.Button(root, text="Output to pdf", command=create_pdf, font=("BIZ-UDGothicR", 14))
export_button.pack(pady=10)

thumbnail_frame = Frame(root)
thumbnail_frame.pack(padx=10, pady=10)

root.mainloop()
