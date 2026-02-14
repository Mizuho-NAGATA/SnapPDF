# -------------------------------------------------------------
# Excelファイルと画像ファイルを読み込み、PDFファイルとして出力します。
# Excelファイルが選択されない場合は、画像ファイルのみが出力されます。
# 複数のフォルダから画像を選択可能
# このプログラム「SnapPDF」は ChatGPT と共に開発され、Copilot によって改良されました。
# Copyright (c) 2023 NAGATA Mizuho. Institute of Laser Engineering, The University of Osaka .
# Created on: 2023-09-29
# Last updated on: 2026-02-04 (Class-based refactoring)
# -------------------------------------------------------------
import os
import subprocess
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, ttk

import pandas as pd
from PIL import Image, ImageTk
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image as PlatypusImage,
)
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from tkinterdnd2 import DND_FILES, TkinterDnD

# PDF file settings (globalな設定だが状態は持たないのでこのままでOK)
pdfmetrics.registerFont(TTFont("BIZ-UDGothicR", "BIZ-UDGothicR.ttc"))
styles = getSampleStyleSheet()
styles["Normal"].fontName = "BIZ-UDGothicR"
styles["Normal"].fontSize = 10
styles["Title"].fontName = "BIZ-UDGothicR"
styles["Title"].fontSize = 16
styles["Title"].alignment = 1  # center


class SnapPDFApp:
    def __init__(self):
        # 状態（元グローバル変数）
        self.image_paths = []  # 画像パス一覧
        self.excel_data = []  # Excelデータ本体
        self.excel_headers = []  # Excelヘッダ
        self.entries = []  # Title / Remarks の Entry

        # GUI要素
        self.root = TkinterDnD.Tk()
        self.root.title("Snap PDF")

        self.thumbnail_frame = None
        self.image_list = None

        # GUI構築
        self._build_gui()

    # =========================
    # GUI 構築
    # =========================
    def _build_gui(self):
        # 入力欄（Title / Remarks）
        input_frame = tk.Frame(self.root)
        input_frame.pack(padx=10, pady=10)

        fields = ["Title", "Remarks"]
        for field in fields:
            frame = tk.Frame(input_frame)
            frame.pack(pady=5)

            label = tk.Label(frame, text=field, width=15, font=("BIZ-UDGothicR", 14))
            label.pack(side=tk.LEFT)

            entry = tk.Entry(frame, font=("BIZ-UDGothicR", 14))
            entry.pack(side=tk.LEFT)

            self.entries.append(entry)

        # ボタン群
        select_excel_button = tk.Button(
            self.root,
            text="Select Excel File",
            command=self.select_excel_file,
            font=("BIZ-UDGothicR", 14),
        )
        select_excel_button.pack(pady=10)

        select_button = tk.Button(
            self.root,
            text="Select Images",
            command=self.select_images,
            font=("BIZ-UDGothicR", 14),
        )
        select_button.pack(pady=10)

        move_up_button = tk.Button(
            self.root,
            text="Move Up",
            command=self.move_up,
            font=("BIZ-UDGothicR", 14),
        )
        move_up_button.pack(pady=10)

        move_down_button = tk.Button(
            self.root,
            text="Move Down",
            command=self.move_down,
            font=("BIZ-UDGothicR", 14),
        )
        move_down_button.pack(pady=10)

        delete_button = tk.Button(
            self.root,
            text="Delete Selected",
            command=self.delete_selected_images,
            font=("BIZ-UDGothicR", 14),
        )
        delete_button.pack(pady=10)

        export_button = tk.Button(
            self.root,
            text="Output to PDF",
            command=self.create_pdf,
            font=("BIZ-UDGothicR", 14),
        )
        export_button.pack(pady=10)

        # 画像リスト（Treeview）
        image_list_frame = tk.Frame(self.root)
        image_list_frame.pack(padx=10, pady=10)

        self.image_list = ttk.Treeview(
            image_list_frame, columns=("File Name", "Path"), show="headings"
        )
        self.image_list.heading("File Name", text="File Name")
        self.image_list.heading("Path", text="Path")
        self.image_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(
            image_list_frame, orient="vertical", command=self.image_list.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.image_list.configure(yscrollcommand=scrollbar.set)

        # サムネイル表示用フレーム（必要になったときに作る）
        self.thumbnail_frame = tk.Frame(self.root)
        self.thumbnail_frame.pack(padx=10, pady=10)

        # （必要なら）Drag & Dropの登録もここで可能
        # self.root.drop_target_register(DND_FILES)
        # self.root.dnd_bind("<<Drop>>", self.on_drop_files)

    # =========================
    # イベントハンドラ / ロジック
    # =========================
    def select_excel_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx *.xls")],
            title="Select Excel File",
        )
        if file_path:
            try:
                df = pd.read_excel(file_path)
                df = df.fillna("")  # NaN を空文字に
                data = df.values.tolist()

                messagebox.showinfo(
                    "Excel File Selected",
                    f"Data loading completed. Number of rows: {len(data)}",
                )

                self.excel_data = data
                self.excel_headers = df.columns.tolist()

            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"Failed to read the Excel file. Error message: {str(e)}",
                )

    def select_images(self):
        new_image_paths = list(
            filedialog.askopenfilenames(
                filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
            )
        )
        if new_image_paths:
            self.image_paths.extend(new_image_paths)
            self.update_image_list()
            messagebox.showinfo(
                "Images Selected",
                f"Number of selected images: {len(new_image_paths)}",
            )

    def update_image_list(self):
        # Treeview をクリア
        for item in self.image_list.get_children():
            self.image_list.delete(item)

        # 画像リストを再構築
        for path in self.image_paths:
            thumbnail = self.generate_thumbnail(path)
            filename = os.path.basename(path)
            # Treeview自体はサムネイルを保持しないが、image引数は指定可能
            self.image_list.insert("", "end", values=(filename, path), image=thumbnail)

        # サムネイル一覧も更新
        self.display_thumbnails()

    def move_up(self):
        selected_items = self.image_list.selection()
        for item in selected_items:
            index = self.image_list.index(item)
            if index > 0:
                self.image_paths.insert(index - 1, self.image_paths.pop(index))
        self.update_image_list()

    def move_down(self):
        selected_items = self.image_list.selection()
        for item in selected_items:
            index = self.image_list.index(item)
            if index < len(self.image_paths) - 1:
                self.image_paths.insert(index + 1, self.image_paths.pop(index))
        self.update_image_list()

    def delete_selected_images(self):
        selected_items = self.image_list.selection()
        # index がずれないように後ろから消す方が安全だが、
        # selection() の順序はTreeview依存なので、ここでは元コードに合わせる
        for item in selected_items:
            index = self.image_list.index(item)
            del self.image_paths[index]
        self.update_image_list()

    def display_thumbnails(self):
        # 既存サムネイルをクリア
        for widget in self.thumbnail_frame.winfo_children():
            widget.destroy()

        num_columns = 5  # 列数

        for i, path in enumerate(self.image_paths):
            thumbnail = self.generate_thumbnail(path)
            if thumbnail:
                # 画像＋ファイル名をまとめるコンテナ
                container = tk.Frame(self.thumbnail_frame)
                container.grid(
                    row=(i // num_columns) * 2,
                    column=i % num_columns,
                    padx=5,
                    pady=5,
                )

                # サムネイル画像
                img_label = tk.Label(container, image=thumbnail)
                img_label.image = thumbnail  # 参照保持
                img_label.pack()

                # ファイル名
                filename = os.path.basename(path)
                name_label = tk.Label(
                    container,
                    text=filename,
                    wraplength=100,
                    font=("BIZ-UDGothicR", 8),
                )
                name_label.pack()

        self.root.update_idletasks()

    def generate_thumbnail(self, image_path):
        try:
            image = Image.open(image_path)
            image.thumbnail((100, 100))
            thumbnail = ImageTk.PhotoImage(image)
            return thumbnail
        except Exception as e:
            print(f"Error generating thumbnail for {image_path}: {str(e)}")
            return None

    def create_pdf(self):
        if not self.image_paths:
            messagebox.showerror("Error", "Please select images")
            return

        now = datetime.now()
        timestamp = now.strftime("%y%m%d_%H%M%S")
        pdf_file_path = timestamp + ".pdf"

        doc = SimpleDocTemplate(
            pdf_file_path,
            pagesize=landscape(A4),
            topMargin=1.5 * inch,
            bottomMargin=0.1 * inch,
        )
        content = []

        # タイトル・ページ番号・備考の描画関数
        def add_title_and_page_number(c, doc_obj):
            # Title
            title_text = self.entries[0].get()
            title_style = styles["Title"]
            title = Paragraph(title_text, title_style)
            title.wrapOn(c, A4[1], A4[0])
            x = (A4[1] - title.width) / 2
            y = A4[0] - inch * 1
            title.wrapOn(c, A4[1], A4[0])
            title.drawOn(c, x, y)

            # Page number
            page_num = c.getPageNumber()
            c.setFont("BIZ-UDGothicR", 10)
            c.setFillColor(colors.black)
            page_width, page_height = landscape(A4)
            text = f"Page {page_num}"
            c.drawCentredString(page_width / 2, inch * 0.1, text)

            # Remarks
            remarks_text = self.entries[1].get()
            remarks = Paragraph(remarks_text, styles["Normal"])
            remarks.wrapOn(c, A4[1], A4[0])
            remarks.drawOn(c, inch, A4[0] - inch * 1.5)

        # Excelデータがあれば先頭に表として追加
        if self.excel_headers:
            # 先頭行にヘッダを追加
            data_with_header = [self.excel_headers] + self.excel_data

            data_table = Table(data_with_header, colWidths=None)
            data_table._width = A4[0] - doc.leftMargin - doc.rightMargin

            table_style = [
                ("BACKGROUND", (0, 0), (-1, 0), (0.8, 0.9, 1.0)),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONT", (0, 0), (-1, -1), "BIZ-UDGothicR", 10),
            ]

            for row in range(2, data_table._nrows, 2):
                table_style.append(("BACKGROUND", (0, row), (-1, row), (0.8, 0.9, 1.0)))

            data_table.setStyle(TableStyle(table_style))
            content.append(data_table)

        # 画像配置
        image_table_data = []
        file_name_table_data = []

        max_width = 200
        max_height = 200
        images_per_page = 5
        image_width = 150
        image_height = 150
        image_spacing = 10  # Spacing between images

        for file_path in self.image_paths:
            image = Image.open(file_path)
            original_width, original_height = image.size

            if original_width > max_width or original_height > max_height:
                image.thumbnail((max_width, max_height), Image.LANCZOS)

            image_ratio = original_width / original_height
            if image_ratio > 1:
                new_width = image_width
                new_height = int(new_width / image_ratio)
            else:
                new_height = image_height
                new_width = int(new_height * image_ratio)

            image_table_data.append(
                PlatypusImage(file_path, width=new_width, height=new_height)
            )
            file_name_table_data.append(
                Paragraph(os.path.basename(file_path), styles["Normal"])
            )

            if len(image_table_data) == images_per_page:
                # Build row with images separated by empty cells for spacing
                row_data_with_spacing = []
                for i, img in enumerate(image_table_data):
                    if i > 0:
                        row_data_with_spacing.append('')  # Empty cell for spacing
                    row_data_with_spacing.append(img)

                # Calculate column widths: alternating image and spacing widths
                colWidths = []
                for i in range(len(image_table_data)):
                    if i > 0:
                        colWidths.append(image_spacing)
                    colWidths.append(image_width)

                content.append(
                    Table(
                        [row_data_with_spacing],
                        colWidths=colWidths,
                    )
                )
                
                # Build filename row with same structure
                filename_row = []
                for i, name in enumerate(file_name_table_data):
                    if i > 0:
                        filename_row.append('')  # Empty cell for spacing
                    filename_row.append(name)
                
                content.append(
                    Table(
                        [filename_row],
                        colWidths=colWidths,
                    )
                )
                image_table_data = []
                file_name_table_data = []

        if image_table_data:
            # Build row with images separated by empty cells for spacing
            row_data_with_spacing = []
            for i, img in enumerate(image_table_data):
                if i > 0:
                    row_data_with_spacing.append('')  # Empty cell for spacing
                row_data_with_spacing.append(img)

            # Calculate column widths: alternating image and spacing widths
            colWidths = []
            for i in range(len(image_table_data)):
                if i > 0:
                    colWidths.append(image_spacing)
                colWidths.append(image_width)

            content.append(
                Table(
                    [row_data_with_spacing],
                    colWidths=colWidths,
                )
            )
            
            # Build filename row with same structure
            filename_row = []
            for i, name in enumerate(file_name_table_data):
                if i > 0:
                    filename_row.append('')  # Empty cell for spacing
                filename_row.append(name)
            
            content.append(
                Table(
                    [filename_row],
                    colWidths=colWidths,
                )
            )

        # PDF生成
        doc.build(
            content,
            onFirstPage=add_title_and_page_number,
            onLaterPages=add_title_and_page_number,
        )

        # PDFを開く
        if os.name == "nt":
            os.startfile(pdf_file_path)
        else:
            subprocess.Popen(["open", pdf_file_path])

        messagebox.showinfo("Completed", "PDF creation is complete")

        # 状態リセット
        self.image_paths.clear()
        self.update_image_list()

    # =========================
    # アプリ起動
    # =========================
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = SnapPDFApp()
    app.run()
