# coding: shift-jis
# -------------------------------------------------------------
# This program "SnapPDF" was developed with the assistance of ChatGPT. ���̃v���O�����uSnapPDF�v�́AChatGPT�̏��͂ɂ���ĊJ�����ꂽ�B
# Copyright (c) 2023 NAGATA Mizuho, �i�c �݂���. Institute of Laser Engineering, Osaka University.
# 240606 Excel�t�@�C����ǂݍ��݁A�I�������摜���t�@�C�����Ƌ���pdf�o�͂���v���O�����B�����s�ɔw�i�F�B
# �����̃t�H���_����摜�I��
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

# PDF�t�@�C���̐ݒ�
pdfmetrics.registerFont(TTFont('BIZ-UDGothicR', 'BIZ-UDGothicR.ttc'))
font_name = 'BIZ-UDGothicR'
styles = getSampleStyleSheet()
styles['Normal'].fontName = 'BIZ-UDGothicR'
styles['Normal'].fontSize = 10
styles['Title'].fontName = 'BIZ-UDGothicR'
styles['Title'].fontSize = 16
styles['Title'].alignment = 1  # 1 �͒����񂹂�\���萔�ł��B�^�C�g���̃X�^�C���ɑ΂��Ē����񂹂�ݒ�B

image_paths = [] # �摜�p�X�̃��X�g
excel_data = [] # �G�N�Z���t�@�C������擾�����f�[�^���i�[���郊�X�g
image_paths = None # �ŏ��ɌĂяo���ۂɁAimage_paths��None�ɐݒ�

def select_excel_file():
    global data, excel_data, excel_headers  # ������ excel_headers ���O���[�o���ϐ��Ƃ��Đ錾����
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")], title="Excel�t�@�C����I��") # �_�C�A���O�{�b�N�X�̃^�C�g����ݒ�
    if file_path:
        # Excel�t�@�C������f�[�^��ǂݍ���
        try:
            df = pd.read_excel(file_path)
            df = df.fillna('')  # �����l���󔒕�����ɕϊ�
            data = df.values.tolist()  # �f�[�^��2�������X�g�ɕϊ�
            print(data)
            messagebox.showinfo("Excel�t�@�C���I��", f"�f�[�^�̓ǂݍ��݂��������܂����B�s��: {len(data)}")

            # �G�N�Z���t�@�C������擾�����f�[�^�� `data` �ɒǉ�
            for row in data:
                excel_data.append(row)

            # �w�b�_�[��ʂ̃��X�g�ɒǉ�
            excel_headers = df.columns.tolist()

        except Exception as e:
            messagebox.showerror("�G���[", f"Excel�t�@�C���̓ǂݍ��݂Ɏ��s���܂����B�G���[���b�Z�[�W: {str(e)}")

def select_images():
    global image_paths
    new_image_paths = list(filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]))
    if new_image_paths:
        if image_paths is None:
            image_paths = new_image_paths
        else:
            image_paths.extend(new_image_paths)
        messagebox.showinfo("�摜�I��", f"�I�����ꂽ�摜��: {len(new_image_paths)}")
        # �T���l�C����\��
        display_thumbnails()

def display_thumbnails():
    if image_paths:
        # �T���l�C���\���p�̃t���[�����쐬
        if thumbnail_frame.winfo_children():
            for widget in thumbnail_frame.winfo_children():
                widget.destroy()

        num_images = len(image_paths)
        num_columns = 10  # �񐔂�������
        num_rows = (num_images + num_columns - 1) // num_columns

        for i, file_path in enumerate(image_paths):
            image = Image.open(file_path)
            image.thumbnail((100, 100))  # �T���l�C���̃T�C�Y��ݒ�
            photo = ImageTk.PhotoImage(image=image)
            label = Label(thumbnail_frame, image=photo)
            label.image = photo
            label.grid(row=i // num_columns, column=i % num_columns, padx=5, pady=5)

def create_pdf():
    global image_paths, data

    # Excel�t�@�C���̃w�b�_�[�� `data` ���X�g�̐擪�ɒǉ�
    data.insert(0, excel_headers)

    # �摜��\��
    max_width = 200  # ���T�C�Y��̍ő啝
    max_height = 200  # ���T�C�Y��̍ő卂��
    images_per_page = 5  # 1�y�[�W������̉摜��
    image_width = 150  # �摜�̕�
    image_height = 150  # �摜�̍���
    image_spacing = 4  # �摜�̍��E�ɒǉ�����X�y�[�X�̕�
    now = datetime.now()  # ���݂̓������擾
    timestamp = now.strftime("%y%m%d_%H%M%S")  # �t�H�[�}�b�g�ɍ��킹�ăt�@�C�������쐬
    pdf_file_path = timestamp + ".pdf"  # �t�@�C�����ɓ�����ǉ�

    if not image_paths:
        messagebox.showerror("�G���[", "�摜��I�����Ă�������")
        return

    doc = SimpleDocTemplate(pdf_file_path, pagesize=landscape(A4), topMargin=1.5 * inch, bottomMargin=0.1 * inch)  # �y�[�W�㉺�̗]��
    content = []

    def add_title_and_page_number(canvas, doc):
        # �^�C�g���̒ǉ�
        title_text = entries[0].get()  # �ŏ��̓��̓t�B�[���h�̃e�L�X�g���擾
        title_style = styles["Title"]
        title = Paragraph(title_text, title_style)
        title.wrapOn(canvas, A4[1], A4[0])  # �^�C�g�����y�[�W�̕��ɍ��킹�ă��b�v���܂�
        # �^�C�g���𒆉��񂹂ŕ`��
        x = (A4[1] - title.width) / 2  # �y�[�W���̒����ɔz�u
        y = A4[0] - inch * 1  # �^�C�g�����y�[�W��[����x�C���`���ɔz�u
        title.wrapOn(canvas, A4[1], A4[0])
        title.drawOn(canvas, x, y)

        # �y�[�W�ԍ��̒ǉ�
        page_num = canvas.getPageNumber()
        canvas.setFont("BIZ-UDGothicR", 10)
        canvas.setFillColor(colors.black)
        page_width, page_height = landscape(A4)
        text = f"Page {page_num}"
        canvas.drawCentredString(page_width / 2, inch * 0.1, text)

        # ���l�̒ǉ�
        remarks_text = entries[1].get()  # ��Ԗڂ̓��̓t�B�[���h�̃e�L�X�g���擾
        remarks = Paragraph(remarks_text, styles["Normal"])
        remarks.wrapOn(canvas, A4[1], A4[0])  # ���l���y�[�W�̕��ɍ��킹�ă��b�v���܂�
        remarks.drawOn(canvas, inch, A4[0] - inch * 1.5)  # ���l���y�[�W��[����x�C���`���ɕ`��B

    # �f�[�^��PDF�ɒǉ����邽�߂̃e�[�u�����쐬
    data_table = Table(data, colWidths=None)  # colWidths��None�ɐݒ肵�ė񕝂���������

    # �e�[�u���̕����y�[�W���ɍ��킹��
    data_table._width = A4[0] - doc.leftMargin - doc.rightMargin

    # �e�[�u���X�^�C�����`
    table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.9, 1.0)),  # 1�s�ڂ̔w�i�F��ݒ� (�������F)
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),      # �O���b�h���̐ݒ�
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),               # ������
        ('FONT', (0, 0), (-1, -1), 'BIZ-UDGothicR', 10),    # �t�H���g�ݒ�
        ('AUTO', (0, 0), (-1, -1), 1),                      # ��������
    ]

    # �����s�ɔw�i�F��ǉ�
    for row in range(2, data_table._nrows, 2):  # �����s�̃C���f�b�N�X�� 2 ����n�܂�
        table_style.append(('BACKGROUND', (0, row), (-1, row), (0.8, 0.9, 1.0)))  # �����s�̔w�i�F��ݒ�

    data_table.setStyle(TableStyle(table_style))

    # �e�[�u����PDF�̃R���e���c�ɒǉ�
    content.append(data_table)

    image_table_data = []
    file_name_table_data = []

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

        if len(image_table_data) == images_per_page:
            # �摜�̍��E�ɃX�y�[�X��ǉ�
            row_data_with_spacing = []
            for image in image_table_data:
                row_data_with_spacing.append(Spacer(1, image_spacing))  # ���̃X�y�[�X
                row_data_with_spacing.append(image)  # �摜
                row_data_with_spacing.append(Spacer(1, image_spacing))  # �E�̃X�y�[�X

            content.append(Table([row_data_with_spacing], colWidths=[image_spacing, image_width, image_spacing] * images_per_page))
            content.append(Table([file_name_table_data], colWidths=[image_width] * images_per_page))
            image_table_data = []
            file_name_table_data = []

    if image_table_data:
        # �摜�̍��E�ɃX�y�[�X��ǉ�
        row_data_with_spacing = []
        for image in image_table_data:
            row_data_with_spacing.append(Spacer(1, image_spacing))  # ���̃X�y�[�X
            row_data_with_spacing.append(image)  # �摜
            row_data_with_spacing.append(Spacer(1, image_spacing))  # �E�̃X�y�[�X

        content.append(Table([row_data_with_spacing], colWidths=[image_spacing, image_width, image_spacing] * len(image_table_data)))
        content.append(Table([file_name_table_data], colWidths=[image_width] * len(file_name_table_data)))

    # �h�L�������g�̃r���h���ɃJ�X�^���R�[���o�b�N�֐����w��
    doc.build(content, onFirstPage=add_title_and_page_number, onLaterPages=add_title_and_page_number)

    if os.name == 'nt':
        os.startfile(pdf_file_path)  # PDF�t�@�C�����J���iWindows�̏ꍇ�j
    else:
        subprocess.Popen(["open", pdf_file_path])  # PDF�t�@�C�����J���imacOS�̏ꍇ�j

    messagebox.showinfo("����", "PDF�̍쐬���������܂���")
    image_paths.clear()

root = tk.Tk()
root.title("Snap PDF")

input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=10)

fields = ["Title �^�C�g��", "Remarks ���l"]  # ���l�t�B�[���h��ǉ�
entries = []

for field in fields:
    frame = tk.Frame(input_frame)
    frame.pack(pady=5)

    label = tk.Label(frame, text=field, width=15, font=("BIZ-UDGothicR", 14))
    label.pack(side=tk.LEFT)

    entry = tk.Entry(frame, font=("BIZ-UDGothicR", 14))
    entry.pack(side=tk.LEFT)

    entries.append(entry)

select_excel_button = tk.Button(root, text="Select Excel File\nExcel�t�@�C����I��", command=select_excel_file, font=("BIZ-UDGothicR", 14))
select_excel_button.pack(pady=10)

select_button = tk.Button(root, text="Select Images\n�摜��I��", command=select_images, font=("BIZ-UDGothicR", 14))
select_button.pack(pady=10)

export_button = tk.Button(root, text="Output to pdf\nPDF�o��", command=create_pdf, font=("BIZ-UDGothicR", 14))
export_button.pack(pady=10)

# �T���l�C���\���p�̃t���[�����쐬
thumbnail_frame = Frame(root)
thumbnail_frame.pack(padx=10, pady=10)

root.mainloop()
