# ---------
# Outputs 15 photos per page to pdf. You can select images from multiple folders.
# This program "SnapPDF" was developed with the assistance of ChatGPT.
# Copyright (c) 2023 NAGATA Mizuho, Institute of Laser Engineering, Osaka University.
# Created on: 2023-09-29
# Last updated on: 2024-07-04
# ---------
from datetime import datetime
from PIL import Image, ImageTk, ImageOps
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Image as PlatypusImage, Table, Paragraph, Spacer
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import tkinter as tk
from tkinter import Tk, Label, Frame, filedialog, messagebox, ttk
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from functools import lru_cache

# PDF file settings
pdfmetrics.registerFont(TTFont('BIZ-UDGothicR', 'BIZ-UDGothicR.ttc'))
font_name = 'BIZ-UDGothicR'
styles = getSampleStyleSheet()
styles['Normal'].fontName = font_name
styles['Normal'].fontSize = 10
styles['Title'].fontName = font_name
styles['Title'].fontSize = 16

image_paths = []  # List of image paths
photo_images = []  # List to store the PhotoImage objects

def select_images():
    global image_paths
    new_image_paths = list(filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]))
    if new_image_paths:
        image_paths.extend(new_image_paths)
        update_image_list()
        messagebox.showinfo("Images Selected", f"Number of selected images: {len(new_image_paths)}")

def update_image_list():
    global image_paths
    for item in image_list.get_children():
        image_list.delete(item)
    for path in image_paths:
        thumbnail = generate_thumbnail(path)
        filename = os.path.basename(path)
        image_list.insert("", "end", values=(filename, path), image=thumbnail)

    # Display thumbnails after updating the list
    display_thumbnails()

def move_up():
    selected_items = image_list.selection()
    for item in selected_items:
        index = image_list.index(item)
        if index > 0:
            image_paths.insert(index - 1, image_paths.pop(index))
    update_image_list()

def move_down():
    selected_items = image_list.selection()
    for item in selected_items:
        index = image_list.index(item)
        if index < len(image_paths) - 1:
            image_paths.insert(index + 1, image_paths.pop(index))
    update_image_list()

def delete_selected_images():
    global image_paths
    selected_items = image_list.selection()
    for item in selected_items:
        index = image_list.index(item)
        del image_paths[index]
    update_image_list()

def display_thumbnails():
    global image_paths

    # Create or get the thumbnail_frame if it's not already defined globally
    if 'thumbnail_frame' not in globals():
        # Define thumbnail_frame globally if it doesn't exist
        global thumbnail_frame
        thumbnail_frame = tk.Frame(root)  # Replace `root` with your parent widget if necessary
        thumbnail_frame.pack(padx=10, pady=10)

    # Clear existing thumbnails
    for widget in thumbnail_frame.winfo_children():
        widget.destroy()

    # Display thumbnails
    thumbnails = []
    for path in image_paths:
        thumbnail = generate_thumbnail(path)
        if thumbnail:
            thumbnails.append(thumbnail)

    num_columns = 10  # Number of columns
    for i, photo in enumerate(thumbnails):
        label = tk.Label(thumbnail_frame, image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection
        label.grid(row=i // num_columns, column=i % num_columns, padx=5, pady=5)

    # Update the GUI
    root.update_idletasks()

def generate_thumbnail(image_path):
    try:
        image = Image.open(image_path)
        image.thumbnail((100, 100))  # Thumbnail size
        thumbnail = ImageTk.PhotoImage(image)
        return thumbnail
    except Exception as e:
        print(f"Error generating thumbnail for {image_path}: {str(e)}")
        return None

def process_image_for_pdf(file_path):
    image = Image.open(file_path)
    original_width, original_height = image.size
    image.thumbnail((200, 200), Image.LANCZOS)

    image_ratio = original_width / original_height
    if image_ratio > 1:
        new_width = 150
        new_height = int(new_width / image_ratio)
    else:
        new_height = 150
        new_width = int(new_height * image_ratio)

    return (PlatypusImage(file_path, width=new_width, height=new_height), Paragraph(os.path.basename(file_path), styles['Normal']))

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

    image_spacing = 10
    col_widths = [150 + image_spacing] * 5

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_image_for_pdf, file_path) for file_path in image_paths]
        results = [future.result() for future in as_completed(futures)]

    image_table_data = []
    file_name_table_data = []

    for image, name in results:
        image_table_data.append(image)
        file_name_table_data.append(name)

        if len(image_table_data) == 5:
            content.append(Table([image_table_data], colWidths=col_widths))
            content.append(Spacer(1, 0.1))
            content.append(Table([file_name_table_data], colWidths=col_widths))
            content.append(Spacer(1, 0.1))
            image_table_data = []
            file_name_table_data = []

    if image_table_data:
        last_row_col_widths = [150 + image_spacing] * len(image_table_data)
        content.append(Table([image_table_data], colWidths=last_row_col_widths))
        content.append(Spacer(1, 12))
        content.append(Table([file_name_table_data], colWidths=last_row_col_widths))
        content.append(Spacer(1, 20))

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
root.title("Snap PDF15")

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

move_up_button = tk.Button(root, text="Move Up", command=move_up, font=("BIZ-UDGothicR", 14))
move_up_button.pack(pady=10)

move_down_button = tk.Button(root, text="Move Down", command=move_down, font=("BIZ-UDGothicR", 14))
move_down_button.pack(pady=10)

delete_button = tk.Button(root, text="Delete Selected", command=delete_selected_images, font=("BIZ-UDGothicR", 14))
delete_button.pack(pady=10)

export_button = tk.Button(root, text="Output to PDF", command=create_pdf, font=("BIZ-UDGothicR", 14))
export_button.pack(pady=10)

# Create frame for image list
image_list_frame = tk.Frame(root)
image_list_frame.pack(padx=10, pady=10)

# Create and pack the image list view
image_list = ttk.Treeview(image_list_frame, columns=("File Name", "Path"), show='headings')
image_list.heading("File Name", text="File Name")
image_list.heading("Path", text="Path")
image_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Add a scrollbar to the list view
scrollbar = tk.Scrollbar(image_list_frame, orient="vertical", command=image_list.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
image_list.configure(yscrollcommand=scrollbar.set)

root.mainloop()
