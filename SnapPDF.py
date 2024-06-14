# -------------------------------------------------------------
# Reads an Excel file and outputs it as a PDF file along with an image file. If no Excel file is selected, only the image file will be output.
# Select images from multiple folders
# This program "SnapPDF" was developed with the assistance of ChatGPT.
# Copyright (c) 2023 NAGATA Mizuho. Institute of Laser Engineering, Osaka University.
# Created on: 2023-09-29
# Last updated on: 2024-06-14
# -------------------------------------------------------------
from datetime import datetime
from PIL import Image, ImageTk
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Image as PlatypusImage, Table, Paragraph, Spacer, TableStyle
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import tkinter as tk
from tkinter import Tk, Label, Canvas, Frame, filedialog, messagebox
import os
import subprocess
import pandas as pd

# PDF file settings
pdfmetrics.registerFont(TTFont('BIZ-UDGothicR', 'BIZ-UDGothicR.ttc'))
font_name = 'BIZ-UDGothicR'
styles = getSampleStyleSheet()
styles['Normal'].fontName = 'BIZ-UDGothicR'
styles['Normal'].fontSize = 10
styles['Title'].fontName = 'BIZ-UDGothicR'
styles['Title'].fontSize = 16
styles['Title'].alignment = 1  # 1 represents center alignment for the title style.

image_paths = [] # List of image paths
excel_data = [] # List to store data from the Excel file
excel_headers = [] # List to store headers from the Excel file

def select_excel_file():
    global data, excel_data, excel_headers
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")], title="Select Excel File")
    if file_path:
        try:
            # Read data from the Excel file
            df = pd.read_excel(file_path)
            df = df.fillna('')  # Convert missing values to empty strings
            data = df.values.tolist()  # Convert data to a 2D list
            print(data)
            messagebox.showinfo("Excel File Selected", f"Data loading completed. Number of rows: {len(data)}")

            # Add data from the Excel file to `data`
            for row in data:
                excel_data.append(row)

            # Add headers to a separate list
            excel_headers = df.columns.tolist()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to read the Excel file. Error message: {str(e)}")

def select_images():
    global image_paths
    new_image_paths = list(filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]))
    if new_image_paths:
        if not image_paths:
            image_paths = new_image_paths
        else:
            image_paths.extend(new_image_paths)
        messagebox.showinfo("Images Selected", f"Number of selected images: {len(new_image_paths)}")
        # Display thumbnails
        display_thumbnails()

def display_thumbnails():
    if image_paths:
        if thumbnail_frame.winfo_children():
            for widget in thumbnail_frame.winfo_children():
                widget.destroy()

        num_images = len(image_paths)
        num_columns = 10  # Initialize the number of columns
        num_rows = (num_images + num_columns - 1) // num_columns

        for i, file_path in enumerate(image_paths):
            image = Image.open(file_path)
            image.thumbnail((100, 100))  # Set the thumbnail size
            photo = ImageTk.PhotoImage(image=image)
            label = Label(thumbnail_frame, image=photo)
            label.image = photo
            label.grid(row=i // num_columns, column=i % num_columns, padx=5, pady=5)

def create_pdf():
    global image_paths, data

    now = datetime.now()  # Get the current date and time
    timestamp = now.strftime("%y%m%d_%H%M%S")  # Create a file name based on the format
    pdf_file_path = timestamp + ".pdf"  # Add the date and time to the file name

    if not image_paths:
        messagebox.showerror("Error", "Please select images")
        return

    doc = SimpleDocTemplate(pdf_file_path, pagesize=landscape(A4), topMargin=1.5 * inch, bottomMargin=0.1 * inch)  # Page margins
    content = []

    def add_title_and_page_number(canvas, doc):
        # Add title
        title_text = entries[0].get()  # Get text from the first input field
        title_style = styles["Title"]
        title = Paragraph(title_text, title_style)
        title.wrapOn(canvas, A4[1], A4[0])  # Wrap the title to the width of the page
        # Draw the title centered
        x = (A4[1] - title.width) / 2  # Center on the page width
        y = A4[0] - inch * 1  # Place the title 1 inch below the top edge of the page
        title.wrapOn(canvas, A4[1], A4[0])
        title.drawOn(canvas, x, y)

        # Add page number
        page_num = canvas.getPageNumber()
        canvas.setFont("BIZ-UDGothicR", 10)
        canvas.setFillColor(colors.black)
        page_width, page_height = landscape(A4)
        text = f"Page {page_num}"
        canvas.drawCentredString(page_width / 2, inch * 0.1, text)

        # Add remarks
        remarks_text = entries[1].get()  # Get text from the second input field
        remarks = Paragraph(remarks_text, styles["Normal"])
        remarks.wrapOn(canvas, A4[1], A4[0])  # Wrap the remarks to the width of the page
        remarks.drawOn(canvas, inch, A4[0] - inch * 1.5)  # Draw the remarks 1.5 inches below the top edge of the page

    # Add Excel file data to the PDF if headers are present
    if excel_headers:
        # Add headers from the Excel file to the top of the `data` list
        data.insert(0, excel_headers)

        # Create a table to add data to the PDF
        data_table = Table(data, colWidths=None)  # Set colWidths to None for auto-adjustment

        # Adjust table width to fit the page
        data_table._width = A4[0] - doc.leftMargin - doc.rightMargin

        # Define table style
        table_style = [
            ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.9, 1.0)),  # Set background color for the first row (light blue)
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),      # Set grid lines
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),               # Center alignment
            ('FONT', (0, 0), (-1, -1), 'BIZ-UDGothicR', 10),    # Font settings
            ('AUTO', (0, 0), (-1, -1), 1),                      # Auto-adjust
        ]

        # Add background color to even rows
        for row in range(2, data_table._nrows, 2):  # Even row indices start from 2
            table_style.append(('BACKGROUND', (0, row), (-1, row), (0.8, 0.9, 1.0)))  # Set background color for even rows

        data_table.setStyle(TableStyle(table_style))

        # Add the table to the PDF content
        content.append(data_table)

    image_table_data = []
    file_name_table_data = []

    max_width = 200  # Maximum width after resizing
    max_height = 200  # Maximum height after resizing
    images_per_page = 5  # Number of images per page
    image_width = 150  # Image width
    image_height = 150  # Image height
    image_spacing = 4  # Width of space added to the left and right of images

    for i, file_path in enumerate(image_paths):
        # Load the image
        image = Image.open(file_path)

        # Get the size of the image
        original_width, original_height = image.size

        # Resize the image
        if original_width > max_width or original_height > max_height:
            image.thumbnail((max_width, max_height), Image.LANCZOS)

        # Calculate size while maintaining aspect ratio
        image_ratio = original_width / original_height
        if image_ratio > 1:
            new_width = image_width
            new_height = int(new_width / image_ratio)
        else:
            new_height = image_height
            new_width = int(new_height * image_ratio)

        # Create data to add the image to the PDF
        image_table_data.append(PlatypusImage(file_path, width=new_width, height=new_height))
        file_name_table_data.append(Paragraph(os.path.basename(file_path), styles['Normal']))

        if len(image_table_data) == images_per_page:
            # Add space to the left and right of images
            row_data_with_spacing = []
            for image in image_table_data:
                row_data_with_spacing.append(Spacer(1, image_spacing))  # Left space
                row_data_with_spacing.append(image)  # Image
                row_data_with_spacing.append(Spacer(1, image_spacing))  # Right space

            content.append(Table([row_data_with_spacing], colWidths=[image_spacing, image_width, image_spacing] * images_per_page))
            content.append(Table([file_name_table_data], colWidths=[image_width] * images_per_page))
            image_table_data = []
            file_name_table_data = []

    if image_table_data:
        # Add space to the left and right of images
        row_data_with_spacing = []
        for image in image_table_data:
            row_data_with_spacing.append(Spacer(1, image_spacing))  # Left space
            row_data_with_spacing.append(image)  # Image
            row_data_with_spacing.append(Spacer(1, image_spacing))  # Right space

        content.append(Table([row_data_with_spacing], colWidths=[image_spacing, image_width, image_spacing] * len(image_table_data)))
        content.append(Table([file_name_table_data], colWidths=[image_width] * len(file_name_table_data)))

    # Specify custom callback function when building the document
    doc.build(content, onFirstPage=add_title_and_page_number, onLaterPages=add_title_and_page_number)

    if os.name == 'nt':
        os.startfile(pdf_file_path)  # Open the PDF file (Windows)
    else:
        subprocess.Popen(["open", pdf_file_path])  # Open the PDF file (macOS)

    messagebox.showinfo("Completed", "PDF creation is complete")
    image_paths.clear()

root = tk.Tk()
root.title("Snap PDF")

input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=10)

fields = ["Title", "Remarks"]  # Added remarks field
entries = []

for field in fields:
    frame = tk.Frame(input_frame)
    frame.pack(pady=5)

    label = tk.Label(frame, text=field, width=15, font=("BIZ-UDGothicR", 14))
    label.pack(side=tk.LEFT)

    entry = tk.Entry(frame, font=("BIZ-UDGothicR", 14))
    entry.pack(side=tk.LEFT)

    entries.append(entry)

select_excel_button = tk.Button(root, text="Select Excel File", command=select_excel_file, font=("BIZ-UDGothicR", 14))
select_excel_button.pack(pady=10)

select_button = tk.Button(root, text="Select Images", command=select_images, font=("BIZ-UDGothicR", 14))
select_button.pack(pady=10)

export_button = tk.Button(root, text="Output to PDF", command=create_pdf, font=("BIZ-UDGothicR", 14))
export_button.pack(pady=10)

# Create frame for thumbnail display
thumbnail_frame = Frame(root)
thumbnail_frame.pack(padx=10, pady=10)

root.mainloop()
