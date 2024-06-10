# coding: shift-jis
# ------------------------------------------------------------
# PDFファイルの中身をand検索するプログラム Snap Search
# 2023-OCT-04 Wed.
# This program "Snap Search" was developed with the assistance of ChatGPT. このプログラム「Snap Search」は、ChatGPTの助力によって開発された。
# Copyright (c) 2023 NAGATA Mizuho, 永田 みず穂. Institute of Laser Engineering, Osaka University.
# ------------------------------------------------------------
import os
from PyPDF2 import PdfReader
import tkinter as tk
from tkinter import filedialog
import csv
from datetime import datetime  # datetimeモジュールをインポート

def search_pdf():
    # ダイアログボックスを表示してディレクトリを選択
    selected_directory = filedialog.askdirectory(title="検索したいディレクトリを選択") # ダイアログボックスのタイトルを設定

    # 入力されたキーワードを取得
    search_keywords = keyword_entry.get().split()  # スペースでキーワードを分割

    # and検索チェックボックスの状態を取得
    and_search = and_checkbox_var.get()

    # 検索結果を保存するリスト
    search_results = []

    # ディレクトリ内のPDFファイルを検索
    for root, _, files in os.walk(selected_directory):
        for filename in files:
            if filename.endswith('.pdf'):
                pdf_file_path = os.path.join(root, filename)

                # PDFファイルを開く
                pdf_reader = PdfReader(pdf_file_path)

                # 各ページを検索
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()

                    # and検索: すべてのキーワードが含まれているかチェック
                if and_search:
                    if all(keyword in page_text for keyword in search_keywords):
                        # 検索結果にキーワードも追加
                        search_results.append((filename, pdf_file_path, search_keywords))
                        continue  # 他のページはチェック不要
                # or検索: どれか一つのキーワードが含まれているかチェック
                else:
                    if any(keyword in page_text for keyword in search_keywords):
                        # 検索結果にキーワードも追加
                        search_results.append((filename, pdf_file_path, search_keywords))


    # 現在の日付と時刻を取得
    current_datetime = datetime.now()

    # 現在の日付と時刻をフォーマット
    date_time_str = current_datetime.strftime("%Y%m%d_%H%M%S")

    # 検索結果CSVファイルへのパス（現在時刻を含む）
    csv_file_path = f'search_results_{date_time_str}.csv'

    # CSVファイルに検索結果を書き込む
    with open(csv_file_path, 'w', newline='', encoding='shift-jis') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['ファイル名', '場所', 'キーワード'])

        for filename, location, keywords in search_results:
            csv_writer.writerow([filename, location, ', '.join(keywords)])

    # 検索結果表示用のウィンドウを作成
    result_window = tk.Toplevel(window)
    result_window.title('PDF本文検索結果')

    if not search_results:
        # 検索結果がない場合のラベル
        result_label = tk.Label(result_window, text='キーワードが見つかりませんでした')
        result_label.pack()
    else:
        # 検索結果を表示
        result_label = tk.Label(result_window, text='キーワードが見つかったPDFファイル:')
        result_label.pack()

    # 検索結果のファイル名、場所、およびキーワードを表示
    for filename, location, keywords in search_results:
        keyword_str = ', '.join(keywords)
        result_text = f'ファイル名: {filename}, 場所: {location}, キーワード: {keyword_str}'
        result_label = tk.Label(result_window, text=result_text, font=("Helvetica", 14))
        result_label.pack()

# GUIウィンドウを作成
window = tk.Tk()
window.title('PDF本文検索 Snap Search')

# ウィンドウのサイズを変更する
window.geometry("400x200")  # 幅400ピクセル、高さ200ピクセル

# キーワード入力欄
keyword_label = tk.Label(window, text='検索キーワード (スペースで区切って入力):', font=("Helvetica", 14))
keyword_label.pack()
keyword_entry = tk.Entry(window, font=("Helvetica", 14))
keyword_entry.pack()

# and検索チェックボックス (最初からチェックされた状態)
and_checkbox_var = tk.BooleanVar(value=True)
and_checkbox = tk.Checkbutton(window, text='and検索', font=("Helvetica", 14), variable=and_checkbox_var)
and_checkbox.pack()

# ディレクトリ選択とCSV出力ボタン
export_csv_button = tk.Button(window, text='ディレクトリを選択 \n 検索結果をCSV出力', font=("Helvetica", 14), command=search_pdf)
export_csv_button.pack()

window.mainloop()
