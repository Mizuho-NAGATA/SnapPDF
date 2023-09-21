# coding: shift-jis
# -------------------------------------------------------------
# This program "SnapPDF" was developed with the assistance of ChatGPT. ���̃v���O�����uSnapPDF�v�́AChatGPT�̏��͂ɂ���ĊJ�����ꂽ�B
# Copyright (c) 2023 NAGATA Mizuho, �i�c �݂���. Institute of Laser Engineering, Osaka University.
# 230921 �^�C�g���Ɖ摜��pdf�o�͂���B�y�[�W�ԍ��\���B
# �����t�H���_����摜�I��
# -------------------------------------------------------------
from datetime import datetime
from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Image as PlatypusImage, Table, Paragraph, Spacer
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess

# PDF�t�@�C���̐ݒ�
pdfmetrics.registerFont(TTFont('BIZ-UDGothicR', 'BIZ-UDGothicR.ttc'))
font_name = 'BIZ-UDGothicR'
styles = getSampleStyleSheet()
styles['Normal'].fontName = 'BIZ-UDGothicR'
styles['Normal'].fontSize = 10
styles['Title'].fontName = 'BIZ-UDGothicR'
styles['Title'].fontSize = 16

# �摜�p�X�̃��X�g
image_paths = []

# �f�[�^���X�g�̍쐬
data = []

def select_images():
    global image_paths
    new_image_paths = list(filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]))
    if new_image_paths:
        if image_paths is None:
            image_paths = new_image_paths
        else:
            image_paths.extend(new_image_paths)
        messagebox.showinfo("�摜�I��", f"�I�����ꂽ�摜��: {len(new_image_paths)}")

# �ŏ��ɌĂяo���ۂɁAimage_paths��None�ɐݒ�
image_paths = None
# �{�^���Ȃǂ� select_images �֐����Ăяo�����Ƃ��ł��܂�

def add_page_number(canvas, doc):
    # ���݂̃y�[�W�ԍ����擾
    page_num = canvas.getPageNumber()
    # �y�[�W�ԍ���`��
    canvas.setFont("BIZ-UDGothicR", 10)
    canvas.setFillColor(colors.black)
    canvas.drawRightString(A4[0] - inch, inch * 0.5, f"Page {page_num}")

def create_pdf():
    global image_paths

    # �f�[�^���擾
    data = [entry.get() for entry in entries]

    # �摜��\��
    max_width = 530  # ���T�C�Y��̍ő啝�ipx�j
    max_height = 300  # ���T�C�Y��̍ő卂���ipx�j
    images_per_page = 2  # 1�y�[�W������̉摜����4�ɕύX
    cells_per_row = 2    # 2��̃Z�����쐬
    image_width = 265  # �摜�̕�
    image_height = 300  # �摜�̍���
    now = datetime.now()  # ���݂̓������擾
    timestamp = now.strftime("%y%m%d_%H%M%S")  # �t�H�[�}�b�g�ɍ��킹�ăt�@�C�������쐬
    pdf_file_path = timestamp + ".pdf"  # �t�@�C�����ɓ�����ǉ�

    if not image_paths:
        messagebox.showerror("�G���[", "�摜��I�����Ă�������")
        return

    doc = SimpleDocTemplate(pdf_file_path, pagesize=landscape(A4), bottomMargin=0.5 * inch)

    content = []

    # �^�C�g���̒ǉ�
    title_text = entries[0].get()  # �ŏ��̓��̓t�B�[���h�̃e�L�X�g���擾
    title = Paragraph(title_text, styles["Title"])
    content.append(title)

    image_table_data = []
    file_name_table_data = []
    combined_table_data = []

    for i, file_path in enumerate(image_paths):
        # �摜��ǂݍ���
        image = Image.open(file_path)

        # �摜�̃T�C�Y���擾
        original_width, original_height = image.size

        # �摜�����T�C�Y
        if original_width > max_width or original_height > max_height:
            image.thumbnail((max_width, max_height), Image.LANCZOS)

        # �摜�̏c������ێ����Ȃ���T�C�Y���v�Z
        image_ratio = original_width / original_height
        if image_ratio > 1:
            new_width = image_width
            new_height = int(new_width / image_ratio)
        else:
            new_height = image_height
            new_width = int(new_height * image_ratio)

        # �摜��PDF�ɒǉ����邽�߂̃f�[�^���쐬
        image_table_data.append(PlatypusImage(file_path, width=new_width, height=new_height))
        file_name_table_data.append(Paragraph(os.path.basename(file_path), styles['Normal']))

        # �摜�ƃt�@�C�����̃y�A���쐬
        image_cell = PlatypusImage(file_path, width=new_width, height=new_height)
        file_name_cell = Paragraph(os.path.basename(file_path), styles['Normal'])

        # �摜�ƃt�@�C�����̃y�A���e�[�u���̍s�ɒǉ�
        combined_table_data.append([image_cell, file_name_cell])

        if len(combined_table_data) == images_per_page:
            # �Z����2x2�̃e�[�u���ɔz�u
            table_data = [combined_table_data[i:i+cells_per_row] for i in range(0, len(combined_table_data), cells_per_row)]
            content.append(Table(table_data, colWidths=[image_width] * cells_per_row))
            combined_table_data = []

    if combined_table_data:
        # �c�����Z����ǉ�
        table_data = [combined_table_data[i:i+cells_per_row] for i in range(0, len(combined_table_data), cells_per_row)]
        content.append(Table(table_data, colWidths=[image_width] * cells_per_row))


    # PDF�𐶐�
    doc.build(content, onFirstPage=add_page_number, onLaterPages=add_page_number)

    if os.name == 'nt':
        os.startfile(pdf_file_path)  # PDF�t�@�C�����J���iWindows�̏ꍇ�j
    else:
        subprocess.Popen(["open", pdf_file_path])  # PDF�t�@�C�����J���imacOS�̏ꍇ�j

    messagebox.showinfo("����", "PDF�̍쐬���������܂���")
    image_paths.clear()

root = tk.Tk()
root.title("Snap PDF �ʐ^4��")

input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=10)

# title_label = tk.Label(input_frame, text="�f�[�^����", font=("Arial", 12, "bold"))
# title_label.pack()

fields = ["Title �^�C�g��"]
entries = []

for field in fields:
    frame = tk.Frame(input_frame)
    frame.pack(pady=5)

    label = tk.Label(frame, text=field, width=15, font=("BIZ-UDGothicR", 14))
    label.pack(side=tk.LEFT)

    entry = tk.Entry(frame, font=("BIZ-UDGothicR", 14))  # �e�L�X�g���̓t�B�[���h���傫���������ꍇ�͂����ɂ�font�I�v�V������ǉ�
    entry.pack(side=tk.LEFT)

    entries.append(entry)

select_button = tk.Button(root, text="Select Images\n�摜��I��", command=select_images, font=("BIZ-UDGothicR", 14))
select_button.pack(pady=10)

export_button = tk.Button(root, text="Output to pdf\nPDF�o��", command=create_pdf, font=("BIZ-UDGothicR", 14))
export_button.pack(pady=10)

root.mainloop()
