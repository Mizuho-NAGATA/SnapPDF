# coding: shift-jis
# This program "SnapPDF" was developed with the assistance of ChatGPT. ���̃v���O�����uSnapPDF�v�́AChatGPT�̏��͂ɂ���ĊJ�����ꂽ�B
# Copyright (c) 2023 NAGATA Mizuho, �i�c �݂���. Institute of Laser Engineering, Osaka University.
# 2406 �ʐ^15���B�^�C�g���Ɖ摜��pdf�o�͂���B�y�[�W�ԍ��\���B�����t�H���_����摜�I���B

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
from tkinter import Tk, Label, Canvas, Frame, filedialog, messagebox
import os
import subprocess

# PDF�t�@�C���̐ݒ�
pdfmetrics.registerFont(TTFont('BIZ-UDGothicR', 'BIZ-UDGothicR.ttc'))
font_name = 'BIZ-UDGothicR'
styles = getSampleStyleSheet()
styles['Normal'].fontName = font_name
styles['Normal'].fontSize = 10
styles['Title'].fontName = font_name
styles['Title'].fontSize = 16

image_paths = []  # �摜�p�X�̃��X�g

def select_images():
    new_image_paths = list(filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]))
    if new_image_paths:
        image_paths.extend(new_image_paths)
        messagebox.showinfo("�摜�I��", f"�I�����ꂽ�摜��: {len(new_image_paths)}")
        display_thumbnails()

def display_thumbnails():
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
            label = Label(thumbnail_frame, image=photo)
            label.image = photo
            label.grid(row=i // num_columns, column=i % num_columns, padx=5, pady=5)

def create_pdf():
    now = datetime.now()
    timestamp = now.strftime("%y%m%d_%H%M%S")
    pdf_file_path = timestamp + ".pdf"

    if not image_paths:
        messagebox.showerror("�G���[", "�摜��I�����Ă�������")
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

    # �摜�e�[�u���̗񕝂�ݒ肷�邽�߂̃X�y�[�X�̃T�C�Y���`
    image_spacing = 10  # 10�|�C���g�̃X�y�[�X
    # �摜�e�[�u���̗񕝂��v�Z�i�摜�̕� + �X�y�[�X�j
    col_widths = [150 + image_spacing] * 5  # ������ '5' ��1�y�[�W������̉摜���ł�

    image_table_data = []
    file_name_table_data = []

    for i, file_path in enumerate(image_paths):
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

        image_table_data.append(PlatypusImage(file_path, width=new_width, height=new_height))
        file_name_table_data.append(Paragraph(os.path.basename(file_path), styles['Normal']))

        # 5���̉摜���W�܂�����A�e�[�u�����쐬����content�ɒǉ�
        if len(image_table_data) == 5:
            content.append(Table([image_table_data], colWidths=col_widths)) # �摜�e�[�u����ǉ�
            content.append(Spacer(1, 0.1)) # �摜�ƃt�@�C�����̊Ԃɍŏ����̃X�y�[�X��ǉ�
            content.append(Table([file_name_table_data], colWidths=col_widths))  # �t�@�C�����e�[�u����ǉ�
            content.append(Spacer(1, 0.1)) # �s�ԂɃX�y�[�X��ǉ�
            # ���X�g���N���A
            image_table_data = []
            file_name_table_data = []

    # �c��̉摜������΁A�������e�[�u���ɒǉ�
    if image_table_data:
        # �Ō�̍s�̉摜���ɉ����ė񕝂𒲐�
        last_row_col_widths = [150 + image_spacing] * len(image_table_data)
        content.append(Table([image_table_data], colWidths=last_row_col_widths))
        content.append(Spacer(1, 12))  # �摜�ƃt�@�C�����̊ԂɃX�y�[�X��ǉ�
        content.append(Table([file_name_table_data], colWidths=last_row_col_widths))
        content.append(Spacer(1, 20))  # �s�ԂɃX�y�[�X��ǉ�

    title_text = entries[0].get()
    remarks_text = entries[1].get()

    doc.build(content, onFirstPage=lambda canvas, doc: add_title_and_page_number(canvas, doc, title_text, remarks_text),
              onLaterPages=lambda canvas, doc: add_title_and_page_number(canvas, doc, title_text, remarks_text))

    if os.name == 'nt':
        subprocess.Popen(["start", pdf_file_path], shell=True)
    else:
        subprocess.Popen(["open", pdf_file_path])

    messagebox.showinfo("����", "PDF�̍쐬���������܂���")

root = tk.Tk()
root.title("Snap PDF")

input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=10)

fields = ["Title �^�C�g��", "Remarks ���l"]
entries = []

for field in fields:
    frame = tk.Frame(input_frame)
    frame.pack(pady=5)

    label = tk.Label(frame, text=field, width=15, font=("BIZ-UDGothicR", 14))
    label.pack(side=tk.LEFT)

    entry = tk.Entry(frame, font=("BIZ-UDGothicR", 14))
    entry.pack(side=tk.LEFT)

    entries.append(entry)

select_button = tk.Button(root, text="Select Images\n�摜��I��", command=select_images, font=("BIZ-UDGothicR", 14))
select_button.pack(pady=10)

export_button = tk.Button(root, text="Output to pdf\nPDF�o��", command=create_pdf, font=("BIZ-UDGothicR", 14))
export_button.pack(pady=10)

thumbnail_frame = Frame(root)
thumbnail_frame.pack(padx=10, pady=10)

root.mainloop()
