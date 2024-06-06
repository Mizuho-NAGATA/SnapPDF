# coding: shift-jis
# -------------------------------------------------------------
# This program "SnapPDF" was developed with the assistance of ChatGPT. このプログラム「SnapPDF」は、ChatGPTの助力によって開発された。
# Copyright (c) 2023 NAGATA Mizuho, 永田 みず穂. Institute of Laser Engineering, Osaka University.
# 240606 Excelファイルを読み込み、選択した画像をファイル名と共にpdf出力するプログラム。偶数行に背景色。
# 複数のフォルダから画像選択
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

# PDFファイルの設定
pdfmetrics.registerFont(TTFont('BIZ-UDGothicR', 'BIZ-UDGothicR.ttc'))
font_name = 'BIZ-UDGothicR'
styles = getSampleStyleSheet()
styles['Normal'].fontName = 'BIZ-UDGothicR'
styles['Normal'].fontSize = 10
styles['Title'].fontName = 'BIZ-UDGothicR'
styles['Title'].fontSize = 16
styles['Title'].alignment = 1  # 1 は中央寄せを表す定数です。タイトルのスタイルに対して中央寄せを設定。

image_paths = [] # 画像パスのリスト
excel_data = [] # エクセルファイルから取得したデータを格納するリスト
image_paths = None # 最初に呼び出す際に、image_pathsをNoneに設定

def select_excel_file():
    global data, excel_data, excel_headers  # ここで excel_headers をグローバル変数として宣言する
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")], title="Excelファイルを選択") # ダイアログボックスのタイトルを設定
    if file_path:
        # Excelファイルからデータを読み込む
        try:
            df = pd.read_excel(file_path)
            df = df.fillna('')  # 欠損値を空白文字列に変換
            data = df.values.tolist()  # データを2次元リストに変換
            print(data)
            messagebox.showinfo("Excelファイル選択", f"データの読み込みが完了しました。行数: {len(data)}")

            # エクセルファイルから取得したデータを `data` に追加
            for row in data:
                excel_data.append(row)

            # ヘッダーを別のリストに追加
            excel_headers = df.columns.tolist()

        except Exception as e:
            messagebox.showerror("エラー", f"Excelファイルの読み込みに失敗しました。エラーメッセージ: {str(e)}")

def select_images():
    global image_paths
    new_image_paths = list(filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]))
    if new_image_paths:
        if image_paths is None:
            image_paths = new_image_paths
        else:
            image_paths.extend(new_image_paths)
        messagebox.showinfo("画像選択", f"選択された画像数: {len(new_image_paths)}")
        # サムネイルを表示
        display_thumbnails()

def display_thumbnails():
    if image_paths:
        # サムネイル表示用のフレームを作成
        if thumbnail_frame.winfo_children():
            for widget in thumbnail_frame.winfo_children():
                widget.destroy()

        num_images = len(image_paths)
        num_columns = 10  # 列数を初期化
        num_rows = (num_images + num_columns - 1) // num_columns

        for i, file_path in enumerate(image_paths):
            image = Image.open(file_path)
            image.thumbnail((100, 100))  # サムネイルのサイズを設定
            photo = ImageTk.PhotoImage(image=image)
            label = Label(thumbnail_frame, image=photo)
            label.image = photo
            label.grid(row=i // num_columns, column=i % num_columns, padx=5, pady=5)

def create_pdf():
    global image_paths, data

    # Excelファイルのヘッダーを `data` リストの先頭に追加
    data.insert(0, excel_headers)

    # 画像を表示
    max_width = 200  # リサイズ後の最大幅
    max_height = 200  # リサイズ後の最大高さ
    images_per_page = 5  # 1ページあたりの画像数
    image_width = 150  # 画像の幅
    image_height = 150  # 画像の高さ
    image_spacing = 4  # 画像の左右に追加するスペースの幅
    now = datetime.now()  # 現在の日時を取得
    timestamp = now.strftime("%y%m%d_%H%M%S")  # フォーマットに合わせてファイル名を作成
    pdf_file_path = timestamp + ".pdf"  # ファイル名に日時を追加

    if not image_paths:
        messagebox.showerror("エラー", "画像を選択してください")
        return

    doc = SimpleDocTemplate(pdf_file_path, pagesize=landscape(A4), topMargin=1.5 * inch, bottomMargin=0.1 * inch)  # ページ上下の余白
    content = []

    def add_title_and_page_number(canvas, doc):
        # タイトルの追加
        title_text = entries[0].get()  # 最初の入力フィールドのテキストを取得
        title_style = styles["Title"]
        title = Paragraph(title_text, title_style)
        title.wrapOn(canvas, A4[1], A4[0])  # タイトルをページの幅に合わせてラップします
        # タイトルを中央寄せで描画
        x = (A4[1] - title.width) / 2  # ページ幅の中央に配置
        y = A4[0] - inch * 1  # タイトルをページ上端からxインチ下に配置
        title.wrapOn(canvas, A4[1], A4[0])
        title.drawOn(canvas, x, y)

        # ページ番号の追加
        page_num = canvas.getPageNumber()
        canvas.setFont("BIZ-UDGothicR", 10)
        canvas.setFillColor(colors.black)
        page_width, page_height = landscape(A4)
        text = f"Page {page_num}"
        canvas.drawCentredString(page_width / 2, inch * 0.1, text)

        # 備考の追加
        remarks_text = entries[1].get()  # 二番目の入力フィールドのテキストを取得
        remarks = Paragraph(remarks_text, styles["Normal"])
        remarks.wrapOn(canvas, A4[1], A4[0])  # 備考をページの幅に合わせてラップします
        remarks.drawOn(canvas, inch, A4[0] - inch * 1.5)  # 備考をページ上端からxインチ下に描画。

    # データをPDFに追加するためのテーブルを作成
    data_table = Table(data, colWidths=None)  # colWidthsをNoneに設定して列幅を自動調整

    # テーブルの幅をページ幅に合わせる
    data_table._width = A4[0] - doc.leftMargin - doc.rightMargin

    # テーブルスタイルを定義
    table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.9, 1.0)),  # 1行目の背景色を設定 (薄い水色)
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),      # グリッド線の設定
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),               # 中央寄せ
        ('FONT', (0, 0), (-1, -1), 'BIZ-UDGothicR', 10),    # フォント設定
        ('AUTO', (0, 0), (-1, -1), 1),                      # 自動調整
    ]

    # 偶数行に背景色を追加
    for row in range(2, data_table._nrows, 2):  # 偶数行のインデックスは 2 から始まる
        table_style.append(('BACKGROUND', (0, row), (-1, row), (0.8, 0.9, 1.0)))  # 偶数行の背景色を設定

    data_table.setStyle(TableStyle(table_style))

    # テーブルをPDFのコンテンツに追加
    content.append(data_table)

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
            # 画像の左右にスペースを追加
            row_data_with_spacing = []
            for image in image_table_data:
                row_data_with_spacing.append(Spacer(1, image_spacing))  # 左のスペース
                row_data_with_spacing.append(image)  # 画像
                row_data_with_spacing.append(Spacer(1, image_spacing))  # 右のスペース

            content.append(Table([row_data_with_spacing], colWidths=[image_spacing, image_width, image_spacing] * images_per_page))
            content.append(Table([file_name_table_data], colWidths=[image_width] * images_per_page))
            image_table_data = []
            file_name_table_data = []

    if image_table_data:
        # 画像の左右にスペースを追加
        row_data_with_spacing = []
        for image in image_table_data:
            row_data_with_spacing.append(Spacer(1, image_spacing))  # 左のスペース
            row_data_with_spacing.append(image)  # 画像
            row_data_with_spacing.append(Spacer(1, image_spacing))  # 右のスペース

        content.append(Table([row_data_with_spacing], colWidths=[image_spacing, image_width, image_spacing] * len(image_table_data)))
        content.append(Table([file_name_table_data], colWidths=[image_width] * len(file_name_table_data)))

    # ドキュメントのビルド時にカスタムコールバック関数を指定
    doc.build(content, onFirstPage=add_title_and_page_number, onLaterPages=add_title_and_page_number)

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

fields = ["Title タイトル", "Remarks 備考"]  # 備考フィールドを追加
entries = []

for field in fields:
    frame = tk.Frame(input_frame)
    frame.pack(pady=5)

    label = tk.Label(frame, text=field, width=15, font=("BIZ-UDGothicR", 14))
    label.pack(side=tk.LEFT)

    entry = tk.Entry(frame, font=("BIZ-UDGothicR", 14))
    entry.pack(side=tk.LEFT)

    entries.append(entry)

select_excel_button = tk.Button(root, text="Select Excel File\nExcelファイルを選択", command=select_excel_file, font=("BIZ-UDGothicR", 14))
select_excel_button.pack(pady=10)

select_button = tk.Button(root, text="Select Images\n画像を選択", command=select_images, font=("BIZ-UDGothicR", 14))
select_button.pack(pady=10)

export_button = tk.Button(root, text="Output to pdf\nPDF出力", command=create_pdf, font=("BIZ-UDGothicR", 14))
export_button.pack(pady=10)

# サムネイル表示用のフレームを作成
thumbnail_frame = Frame(root)
thumbnail_frame.pack(padx=10, pady=10)

root.mainloop()
