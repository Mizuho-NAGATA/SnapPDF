# coding: shift-jis
# -------------------------------------------------------------
# This program "SnapPDF" was developed with the assistance of ChatGPT. このプログラム「SnapPDF」は、ChatGPTの助力によって開発された。
# Copyright (c) 2023 NAGATA Mizuho, 永田 みず穂. Institute of Laser Engineering, Osaka University.
# 230907 タイトルと画像をpdf出力する。ページ番号表示。
# 複数フォルダから画像選択
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

# PDFファイルの設定
pdfmetrics.registerFont(TTFont('BIZ-UDGothicR', 'BIZ-UDGothicR.ttc'))
font_name = 'BIZ-UDGothicR'
styles = getSampleStyleSheet()
styles['Normal'].fontName = 'BIZ-UDGothicR'
styles['Normal'].fontSize = 10
styles['Title'].fontName = 'BIZ-UDGothicR'
styles['Title'].fontSize = 16

# 画像パスのリスト
image_paths = []

# データリストの作成
data = []

def select_images():
    global image_paths
    new_image_paths = list(filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]))
    if new_image_paths:
        if image_paths is None:
            image_paths = new_image_paths
        else:
            image_paths.extend(new_image_paths)
        messagebox.showinfo("画像選択", f"選択された画像数: {len(new_image_paths)}")

# 最初に呼び出す際に、image_pathsをNoneに設定
image_paths = None
# ボタンなどで select_images 関数を呼び出すことができます

def add_page_number(canvas, doc):
    # 現在のページ番号を取得
    page_num = canvas.getPageNumber()
    # ページ番号を描画
    canvas.setFont("BIZ-UDGothicR", 10)
    canvas.setFillColor(colors.black)
    canvas.drawRightString(A4[0] - inch, inch * 0.5, f"Page {page_num}")

def create_pdf():
    global image_paths

    # データを取得
    data = [entry.get() for entry in entries]

    # 画像を表示
    max_width = 200  # リサイズ後の最大幅
    max_height = 200  # リサイズ後の最大高さ
    images_per_page = 5  # 1ページあたりの画像数
    image_width = 150  # 画像の幅
    image_height = 150  # 画像の高さ
    now = datetime.now()  # 現在の日時を取得
    timestamp = now.strftime("%y%m%d_%H%M%S")  # フォーマットに合わせてファイル名を作成
    pdf_file_path = timestamp + ".pdf"  # ファイル名に日時を追加

    if not image_paths:
        messagebox.showerror("エラー", "画像を選択してください")
        return

    doc = SimpleDocTemplate(pdf_file_path, pagesize=landscape(A4), bottomMargin=0.5 * inch)

    content = []

    # タイトルの追加
    title_text = entries[0].get()  # 最初の入力フィールドのテキストを取得
    title = Paragraph(title_text, styles["Title"])
    content.append(title)

    image_table_data = []
    file_name_table_data = []

    for i, file_path in enumerate(image_paths):
        # 画像を読み込む
        image = Image.open(file_path)

        # 画像のサイズを取得
        original_width, original_height = image.size

        # 画像をリサイズ
        if original_width > max_width or original_height > max_height:
            image.thumbnail((max_width, max_height), Image.LANCZOS)

        # 画像の縦横比を維持しながらサイズを計算
        image_ratio = original_width / original_height
        if image_ratio > 1:
            new_width = image_width
            new_height = int(new_width / image_ratio)
        else:
            new_height = image_height
            new_width = int(new_height * image_ratio)

        # 画像をPDFに追加するためのデータを作成
        image_table_data.append(PlatypusImage(file_path, width=new_width, height=new_height))
        file_name_table_data.append(Paragraph(os.path.basename(file_path), styles['Normal']))

        if len(image_table_data) == images_per_page:
            content.append(Table([image_table_data], colWidths=[image_width] * images_per_page))
            content.append(Table([file_name_table_data], colWidths=[image_width] * images_per_page))
            image_table_data = []
            file_name_table_data = []

    if image_table_data:
        content.append(Table([image_table_data], colWidths=[image_width] * len(image_table_data)))
        content.append(Table([file_name_table_data], colWidths=[image_width] * len(file_name_table_data)))

    # PDFを生成
    doc.build(content, onFirstPage=add_page_number, onLaterPages=add_page_number)

    if os.name == 'nt':
        os.startfile(pdf_file_path)  # PDFファイルを開く（Windowsの場合）
    else:
        subprocess.Popen(["open", pdf_file_path])  # PDFファイルを開く（macOSの場合）

    messagebox.showinfo("完了", "PDFの作成が完了しました")
    image_paths.clear()

root = tk.Tk()
root.title("Snap PDF")

input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=10)

# title_label = tk.Label(input_frame, text="データ入力", font=("Arial", 12, "bold"))
# title_label.pack()

fields = ["Title タイトル"]
entries = []

for field in fields:
    frame = tk.Frame(input_frame)
    frame.pack(pady=5)

    label = tk.Label(frame, text=field, width=15, font=("BIZ-UDGothicR", 14))
    label.pack(side=tk.LEFT)

    entry = tk.Entry(frame, font=("BIZ-UDGothicR", 14))  # テキスト入力フィールドも大きくしたい場合はここにもfontオプションを追加
    entry.pack(side=tk.LEFT)

    entries.append(entry)

select_button = tk.Button(root, text="Select Images\n画像を選択", command=select_images, font=("BIZ-UDGothicR", 14))
select_button.pack(pady=10)

export_button = tk.Button(root, text="Output to pdf\nPDF出力", command=create_pdf, font=("BIZ-UDGothicR", 14))
export_button.pack(pady=10)

root.mainloop()
