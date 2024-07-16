# -------------------------------------------------------------
# 4 photos per page to pdf. You can select images from multiple folders.
# You can rotate the photo. Page size is A4 portrait. You can replace and delete selected photos.
# This program "SnapPDF" was developed with the assistance of ChatGPT.
# Copyright (c) 2023 NAGATA Mizuho, Institute of Laser Engineering, Osaka University.
# Created on: 2023-09-29
# Last updated on: 2024-07-05
# -------------------------------------------------------------

from datetime import datetime
from PIL import Image, ImageTk, ExifTags
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Image as PlatypusImage, Table, Paragraph, Spacer
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from tkinter import Tk, Label, Canvas, Frame, filedialog, messagebox, ttk
from tempfile import NamedTemporaryFile
import tkinter as tk
import os
import subprocess
import tempfile
import threading

# PDF file settings
pdfmetrics.registerFont(TTFont('BIZ-UDGothicR', 'BIZ-UDGothicR.ttc'))
font_name = 'BIZ-UDGothicR'
styles = getSampleStyleSheet()
styles['Normal'].fontName = 'BIZ-UDGothicR'
styles['Normal'].fontSize = 10
styles['Title'].fontName = 'BIZ-UDGothicR'
styles['Title'].fontSize = 16

image_paths = []  # List of image paths
data = []  # Data list creation

def select_images():
    global image_paths
    new_image_paths = list(filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]))
    if new_image_paths:
        image_paths.extend(new_image_paths)
        threading.Thread(target=update_image_list).start()
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
    threading.Thread(target=update_image_list).start()

def move_down():
    selected_items = image_list.selection()
    for item in selected_items:
        index = image_list.index(item)
        if index < len(image_paths) - 1:
            image_paths.insert(index + 1, image_paths.pop(index))
    threading.Thread(target=update_image_list).start()

def delete_selected_images():
    global image_paths
    selected_items = image_list.selection()
    for item in selected_items:
        index = image_list.index(item)
        del image_paths[index]
    threading.Thread(target=update_image_list).start()

def rotate_image(file_path, angle):
    try:
        image = Image.open(file_path)
        rotated_image = image.rotate(angle, expand=True)
        return rotated_image, file_path  # Return rotated image and file path
    except Exception as e:
        print(f"Error rotating image: {e}")
        return None, None

rotated_photos = {}  # Dictionary to store rotated PhotoImage for each thumbnail
rotated_counts = {}  # Dictionary to keep track of rotation counts for each image

def rotate_thumbnail(event, image_label, file_path):
    # Increase rotation count each time thumbnail is clicked
    rotated_counts[file_path] = rotated_counts.get(file_path, 0) + 1
    rotate_angle = 90 * rotated_counts[file_path]  # Rotate by 90 degrees each time

    rotated_image, _ = rotate_image(file_path, rotate_angle)

    if rotated_image:
        # Adjust thumbnail size appropriately
        thumbnail_size = (100, 100)
        rotated_image.thumbnail(thumbnail_size, Image.LANCZOS)

        # Save PIL ImageTk object to global variable
        rotated_photo = ImageTk.PhotoImage(rotated_image)

        # Update thumbnail
        image_label.configure(image=rotated_photo)
        image_label.image = rotated_photo

def display_thumbnails():
    global rotated_counts  # Initialize dictionary on screen refresh

    if image_paths:
        # Create frame for displaying thumbnails
        if thumbnail_frame.winfo_children():
            for widget in thumbnail_frame.winfo_children():
                widget.destroy()

        num_images = len(image_paths)
        num_columns = 10  # Initialize number of columns
        num_rows = (num_images + num_columns - 1) // num_columns

        for i, file_path in enumerate(image_paths):
            image = Image.open(file_path)
            image.thumbnail((100, 100))  # Set thumbnail size
            photo = ImageTk.PhotoImage(image=image)

            label = tk.Label(thumbnail_frame, image=photo)
            label.image = photo
            label.grid(row=i // num_columns, column=i % num_columns, padx=5, pady=5)

            # Bind rotation event to clicking thumbnail
            label.bind("<Button-1>", lambda event, path=file_path, label=label: rotate_thumbnail(event, label, path))

def generate_thumbnail(image_path):
    try:
        image = Image.open(image_path)
        image.thumbnail((100, 100))  # Thumbnail size
        thumbnail = ImageTk.PhotoImage(image)
        return thumbnail
    except Exception as e:
        print(f"Error generating thumbnail for {image_path}: {str(e)}")
        return None

def create_pdf():
    global image_paths, rotated_counts

    now = datetime.now()
    timestamp = now.strftime("%y%m%d_%H%M%S")
    pdf_file_path = timestamp + ".pdf"

    if not image_paths:
        messagebox.showerror("Error", "Please select an image")
        return

    doc = SimpleDocTemplate(pdf_file_path, pagesize=A4, topMargin=1.5 * inch, bottomMargin=0.1 * inch)

    content = []

    def add_title_and_page_number(canvas, doc, title_text, remarks_text):
        title_style = styles["Title"]
        title = Paragraph(title_text, title_style)
        title.wrapOn(canvas, A4[0], A4[1])
        x = (A4[0] - title.width) / 2
        y = A4[1] - inch * 1
        title.drawOn(canvas, x, y)

        page_num = canvas.getPageNumber()
        canvas.setFont(font_name, 10)
        canvas.setFillColor(colors.black)
        page_width, page_height = A4
        text = f"Page {page_num}"
        canvas.drawCentredString(page_width / 2, inch * 0.1, text)

        remarks = Paragraph(remarks_text, styles["Normal"])
        remarks.wrapOn(canvas, A4[0], A4[1])
        remarks.drawOn(canvas, inch, A4[1] - inch * 1.5)

    # Calculate to maximize the size of the image
    available_width = A4[0] - 2 * inch - 10  # Consider the space for margins and the gap between images
    available_height = A4[1] - 2.5 * inch - 0.5 * inch  # Consider the space for title, remarks, and page number

    image_table_data = []
    file_name_table_data = []

    for i, file_path in enumerate(image_paths):
        # Load the image
        rotated_image, rotated_file_path = rotate_image(file_path, 90 * rotated_counts.get(file_path, 0))

    if rotated_image:
        # Save rotated image to a temporary folder
        with NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            temp_filename = temp_file.name
            rotated_image.save(temp_filename)

        # Calculate image dimensions while maintaining aspect ratio
        image_ratio = rotated_image.width / rotated_image.height
        new_width = available_width / 2 - 10  # Display in 2 columns, with space in between
        new_height = new_width / image_ratio

        # Check if the image fits on the page
        if new_height > available_height / 2 - 10:  # Display in 2 rows, with space in between
            new_height = available_height / 2 - 10  # Display in 2 rows, with space in between
            new_width = new_height * image_ratio

        image_table_data.append(PlatypusImage(temp_filename, width=new_width, height=new_height))
        file_name_table_data.append(Paragraph(os.path.basename(rotated_file_path), styles['Normal']))

        # When 2 images are gathered or it's the last image, create a table and add it to content
        if len(image_table_data) == 2 or i == len(image_paths) - 1:
            content.append(Table([image_table_data], colWidths=[available_width / 2] * len(image_table_data)))  # Add image table
            content.append(Spacer(1, 0.1 * inch))  # Add minimal space between image and file name
            content.append(Table([file_name_table_data], colWidths=[available_width / 2] * len(file_name_table_data)))  # Add file name table
            content.append(Spacer(1, 0.1 * inch))  # Add space between lines
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
root.title("SnapPDF4_irekae")

input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=10)

fields = ["Title", "Remarks"]  # Add Remarks field
entries = []

for field in fields:
    frame = tk.Frame(input_frame)
    frame.pack(pady=5)

    label = tk.Label(frame, text=field, width=15, font=("BIZ-UDGothicR", 14))
    label.pack(side=tk.LEFT)

    entry = tk.Entry(frame, font=("BIZ-UDGothicR", 14))  # You can also increase the font size for text input fields here
    entry.pack(side=tk.LEFT)

    entries.append(entry)

# Create frame for displaying thumbnails
thumbnail_frame = Frame(root)
thumbnail_frame.pack(padx=10, pady=10)

# Add "Select Images" button
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
