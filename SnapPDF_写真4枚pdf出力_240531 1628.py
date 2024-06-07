# coding: shift-jis
# -------------------------------------------------------------
# This program "SnapPDF" was developed with the assistance of ChatGPT. このプログラム「SnapPDF」は、ChatGPTの助力によって開発された。
# Copyright (c) 2023 NAGATA Mizuho, 永田 みず穂. Institute of Laser Engineering, Osaka University.
# 240531 写真4枚表示。タイトルと画像をpdf出力する。ページ番号表示。複数フォルダから画像選択。
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

# PDFファイルの設定
pdfmetrics.registerFont(TTFont('BIZ-UDGothicR', 'BIZ-UDGothicR.ttc'))
font_name = 'BIZ-UDGothicR'
styles = getSampleStyleSheet()
styles['Normal'].fontName = font_name
styles['Normal'].fontSize = 10
styles['Title'].fontName = font_name
styles['Title'].fontSize = 16

image_paths = []  # 画像パスのリスト

def select_images():
    new_image_paths = list(filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]))
    if new_image_paths:
        image_paths.extend(new_image_paths)
        messagebox.showinfo("画像選択", f"選択された画像数: {len(new_image_paths)}")
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
        messagebox.showerror("エラー", "画像を選択してください")
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

    # 画像のサイズを最大化するための計算
    available_width = A4[1] - 2 * inch
    available_height = A4[0] - 2.5 * inch - 0.5 * inch  # タイトル、備考、ページ番号のスペースを考慮

    image_table_data = []
    file_name_table_data = []

    for i, file_path in enumerate(image_paths):
        image = Image.open(file_path)
        original_width, original_height = image.size

        image_ratio = original_width / original_height
        new_width = available_width / 2 - 10  # 2列で表示、間にスペース
        new_height = new_width / image_ratio

        # 画像がページに収まるかどうかを確認
        if new_height > available_height / 2 - 10:  # 2行で表示、間にスペース
            new_height = available_height / 2 - 10  # 2行で表示、間にスペース
            new_width = new_height * image_ratio

        image_table_data.append(PlatypusImage(file_path, width=new_width, height=new_height))
        file_name_table_data.append(Paragraph(os.path.basename(file_path), styles['Normal']))

        # 2枚の画像が集まったら、テーブルを作成してcontentに追加
        if len(image_table_data) == 2:
            content.append(Table([image_table_data], colWidths=[available_width / 2] * 2))  # 画像テーブルを追加
            content.append(Spacer(1, 0.1))  # 画像とファイル名の間に最小限のスペースを追加
            content.append(Table([file_name_table_data], colWidths=[available_width / 2] * 2))  # ファイル名テーブルを追加
            content.append(Spacer(1, 0.1))  # 行間にスペースを追加
            # リストをクリア
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

    messagebox.showinfo("完了", "PDFの作成が完了しました")

root = tk.Tk()
root.title("Snap PDF")

input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=10)

fields = ["Title タイトル", "Remarks 備考"]
entries = []

for field in fields:
    frame = tk.Frame(input_frame)
    frame.pack(pady=5)

    label = tk.Label(frame, text=field, width=15, font=("BIZ-UDGothicR", 14))
    label.pack(side=tk.LEFT)

    entry = tk.Entry(frame, font=("BIZ-UDGothicR", 14))
    entry.pack(side=tk.LEFT)

    entries.append(entry)

select_button = tk.Button(root, text="Select Images\n画像を選択", command=select_images, font=("BIZ-UDGothicR", 14))
select_button.pack(pady=10)

export_button = tk.Button(root, text="Output to pdf\nPDF出力", command=create_pdf, font=("BIZ-UDGothicR", 14))
export_button.pack(pady=10)

thumbnail_frame = Frame(root)
thumbnail_frame.pack(padx=10, pady=10)

root.mainloop()
