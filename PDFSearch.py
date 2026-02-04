# -------------------------------------------------------------
# PDFキーワード検索とCSV出力プログラム（クラス化リファクタリング版）
# このプログラム「PDFSearch」は ChatGPT と共に開発し、Copilotによって改良されました。
# Copyright (c) 2023
# NAGATA Mizuho, Institute of Laser Engineering, The University of Osaka.
# Created on: 2023-09-15
# Last updated on: 2026-02-04 (Class-based refactoring)
# -------------------------------------------------------------

import csv
import os
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox

from PyPDF2 import PdfReader


class PDFSearchApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PDF Text Search - PDFSearch")
        self.root.geometry("420x230")

        self.keyword_entry = None
        self.and_checkbox_var = tk.BooleanVar(value=True)

        self._build_gui()

    # -------------------------------------------------------------
    # GUI構築
    # -------------------------------------------------------------
    def _build_gui(self):
        label = tk.Label(
            self.root,
            text="Search keywords\n(separate with space, supports Japanese):",
            font=("Helvetica", 14),
        )
        label.pack()

        self.keyword_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.keyword_entry.pack()

        and_checkbox = tk.Checkbutton(
            self.root,
            text="AND search",
            font=("Helvetica", 14),
            variable=self.and_checkbox_var,
        )
        and_checkbox.pack()

        search_button = tk.Button(
            self.root,
            text="Select directory\nOutput search results to CSV",
            font=("Helvetica", 14),
            command=self.search_pdf,
        )
        search_button.pack(pady=10)

    # -------------------------------------------------------------
    # PDF検索処理
    # -------------------------------------------------------------
    def search_pdf(self):
        directory = filedialog.askdirectory(title="Select directory to search")
        if not directory:
            return

        keywords = self.keyword_entry.get().split()
        if not keywords:
            messagebox.showerror("Error", "Please enter at least one keyword")
            return

        and_search = self.and_checkbox_var.get()
        results = []

        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.lower().endswith(".pdf"):
                    pdf_path = os.path.join(root, filename)

                    try:
                        reader = PdfReader(pdf_path)
                    except Exception:
                        continue

                    found = False

                    for page in reader.pages:
                        text = page.extract_text() or ""

                        if and_search:
                            if all(k in text for k in keywords):
                                found = True
                                break
                        else:
                            if any(k in text for k in keywords):
                                found = True
                                break

                    if found:
                        results.append((filename, pdf_path, keywords))

        self.export_csv(results)
        self.show_results(results)

    # -------------------------------------------------------------
    # CSV出力
    # -------------------------------------------------------------
    def export_csv(self, results):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = f"search_results_{timestamp}.csv"

        with open(csv_path, "w", newline="", encoding="shift-jis") as f:
            writer = csv.writer(f)
            writer.writerow(["File name", "Location", "Keywords"])

            for filename, location, keywords in results:
                writer.writerow([filename, location, ", ".join(keywords)])

    # -------------------------------------------------------------
    # 結果表示ウィンドウ
    # -------------------------------------------------------------
    def show_results(self, results):
        win = tk.Toplevel(self.root)
        win.title("PDF Search Results")

        if not results:
            label = tk.Label(win, text="No keywords were found", font=("Helvetica", 14))
            label.pack()
            return

        header = tk.Label(
            win, text="PDF files where keywords were found:", font=("Helvetica", 14)
        )
        header.pack()

        for filename, location, keywords in results:
            text = (
                f"File: {filename}\nPath: {location}\nKeywords: {', '.join(keywords)}"
            )
            label = tk.Label(win, text=text, font=("Helvetica", 12), justify="left")
            label.pack(pady=5)

    # -------------------------------------------------------------
    # 実行
    # -------------------------------------------------------------
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    PDFSearchApp().run()
