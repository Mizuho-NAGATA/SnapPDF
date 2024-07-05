# -------------------------------------------------------------
# This program "SnapPDF4_kaiten_tate" was developed with the assistance of ChatGPT.
# Copyright (c) 2023 NAGATA Mizuho. Institute of Laser Engineering, Osaka University.
# 240110 Outputs titles and images to PDF, displaying page numbers.
# Photos can be rotated.
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
from tkinter import Tk, Label, Canvas, Frame, filedialog, messagebox
import os
import subprocess
import tempfile
import tkinter as tk

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
image_paths = None  # Set image_paths to None when first called

def select_images():
    global image_paths
    new_image_paths = list(filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tif")]))
    if new_image_paths:
        if image_paths is None:
            image_paths = new_image_paths
        else:
            image_paths.extend(new_image_paths)
        messagebox.showinfo("Select Images", f"Number of selected images: {len(new_image_paths)}")
        # Display thumbnails
        display_thumbnails()

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
            temp_filename = tempfile.mktemp(suffix='.png')
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
root.title("SnapPDF4_kaiten_tate")

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

export_button = tk.Button(root, text="Output to PDF", command=create_pdf, font=("BIZ-UDGothicR", 14))
export_button.pack(pady=10)

root.mainloop()
