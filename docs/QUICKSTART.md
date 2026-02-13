# SnapPDF.py - Quick Start Guide
# SnapPDF.py - クイックスタートガイド

## 🚀 5分で始める / Get Started in 5 Minutes

### ステップ1: 必要なパッケージをインストール / Step 1: Install Required Packages

```bash
pip install Pillow reportlab PyPDF2 pandas tkinterdnd2
```

### ステップ2: プログラムを起動 / Step 2: Launch the Program

```bash
python SnapPDF.py
```

### ステップ3: タブを選択 / Step 3: Select Tab

プログラムが起動したら、使用する機能のタブを選択します：

Choose the tab for the function you want to use:

- **PDF Creation** - 画像からPDFを作成 / Create PDF from images
- **PDF Search** - PDFファイル内のテキストを検索 / Search text within PDF files

### ステップ4: レイアウトを選択 (PDF作成の場合) / Step 4: Select Layout (For PDF Creation)

PDF Creationタブで、希望するレイアウトを選択します：

In the PDF Creation tab, choose your desired layout:

- **2 images (1×2)** - 最大サイズで2枚 / 2 photos in maximum size
- **4 images (2×2)** - バランスの良い4枚 / 4 photos in balanced size
- **6 images (3×2)** - 推奨・6枚 / 6 photos (recommended)
- **15 images (5×3)** - コンパクトに15枚 / 15 photos compactly

### ステップ5: 画像を選択 / Step 5: Select Images

1. 「Select Images」ボタンをクリック
2. 画像ファイルを選択（複数選択可能）
3. サムネイルが表示されます

Click "Select Images" button, choose image files (multiple selection allowed), and thumbnails will be displayed.

### ステップ6: PDFを出力 / Step 6: Output PDF

「Output to PDF」ボタンをクリックすると、PDFが生成され自動的に開きます。

Click "Output to PDF" button, and the PDF will be generated and automatically opened.

---

## 📖 基本的な使い方 / Basic Usage

### PDF作成タブ / PDF Creation Tab

#### タイトルと備考を追加 / Add Title and Remarks

```
┌─────────────────────────────┐
│ Title:   [Your Title Here]  │
│ Remarks: [Your Notes Here]  │
└─────────────────────────────┘
```

タイトルと備考は各ページのヘッダーに表示されます。

Title and remarks will appear in the header of each page.

#### Excel連携（オプション）/ Excel Integration (Optional)

Excel形式のデータテーブルをPDFに含めることができます：

You can include Excel data tables in the PDF:

1. 「Select Excel File (Optional)」ボタンをクリック
2. Excelファイル（.xlsx または .xls）を選択
3. PDFの最初にテーブルとして表示されます

Click "Select Excel File (Optional)", choose an Excel file (.xlsx or .xls), and it will appear as a table at the beginning of the PDF.

### PDF検索タブ / PDF Search Tab

#### キーワード検索 / Keyword Search

1. 検索キーワードを入力（スペース区切りで複数可能）
2. 検索モードを選択（AND検索 または OR検索）
3. 「Select directory」でディレクトリを選択
4. 検索結果が表示され、CSVファイルも生成されます

Enter search keywords (space-separated for multiple), select search mode (AND or OR), select directory, and view results with auto-generated CSV file.

---

## 💡 便利な使い方 / Useful Tips

### PDF作成のヒント / PDF Creation Tips

#### レイアウトの選び方 / How to Choose Layout

| 用途 / Purpose | 推奨レイアウト / Recommended |
|----------------|----------------------------|
| 詳細な写真記録 / Detailed photo records | 2 images (1×2) |
| 実験結果の比較 / Experiment comparison | 4 images (2×2) |
| イベント記録 / Event documentation | 6 images (3×2)  |
| サムネイル一覧 / Thumbnail overview | 15 images (5×3) |

#### ファイル名のルール / File Naming Rules

生成されるPDFファイル名は自動的に日時で命名されます：

Generated PDF files are automatically named with date and time:

```
YYMMDD_HHMMSS.pdf
例 / Example: 260212_143025.pdf
```

### PDF検索のヒント / PDF Search Tips

#### AND検索 / AND Search
すべてのキーワードを含むPDFを検索します：
```
実験 結果 2026
```

#### OR検索 / OR Search
いずれかのキーワードを含むPDFを検索します：
```
レポート 報告書 ドキュメント
```

---

## ⚠️ トラブルシューティング / Troubleshooting

### エラー: モジュールが見つからない / Error: Module not found

```bash
# 必要なパッケージを再インストール
pip install --upgrade Pillow reportlab pandas PyPDF2
```

### PDFが開かない / PDF doesn't open

PDFは作業ディレクトリに保存されます。手動で開いてください。

The PDF is saved in the working directory. Open it manually.

### 日本語フォントが表示されない / Japanese fonts not displaying

SnapPDF_tabbed.pyは自動的にOS に応じた適切なフォントを選択します。
フォントが見つからない場合は、以下をインストールしてください：

SnapPDF_tabbed.py automatically selects appropriate fonts based on your OS.
If fonts are not found, install the following:

**Windows**: MS Gothic または Yu Gothic（通常はプリインストール済み）
**macOS**: Hiragino Sans（通常はプリインストール済み）
**Linux**:
```bash
sudo apt-get install fonts-noto-cjk fonts-takao-gothic
```

---

## 🎯 よくある質問 / FAQ

### Q: SnapPDF_tabbed.pyは他のバージョンと何が違いますか？

A: SnapPDF_tabbed.pyはPDF作成とPDF検索を1つのGUIで統合し、タブで簡単に切り替えられます。また、Windows、macOS、Linuxの各プラットフォームで適切なフォントを自動的に選択します。

### Q: How is SnapPDF_tabbed.py different from other versions?

A: SnapPDF_tabbed.py integrates PDF creation and search in one GUI with easy tab switching. It also automatically selects appropriate fonts for Windows, macOS, and Linux platforms.

### Q: 画像の順序は保持されますか？

A: はい、選択した順序通りにPDFに配置されます。

### Q: Is the image order preserved?

A: Yes, images are arranged in the PDF in the order they were selected.

### Q: 画像形式は何がサポートされていますか？

A: JPEG (.jpg, .jpeg), PNG (.png), BMP (.bmp) がサポートされています。

### Q: What image formats are supported?

A: JPEG (.jpg, .jpeg), PNG (.png), and BMP (.bmp) are supported.

### Q: PDFのサイズは？

A: A4横向き（landscape）で出力されます。

### Q: What is the PDF size?

A: Output is A4 landscape orientation.

### Q: PDF検索で日本語は使えますか？

A: はい、日本語のキーワードで検索できます。

### Q: Can I use Japanese for PDF search?

A: Yes, you can search using Japanese keywords.

---

## 📱 実行例 / Usage Example

### 例1: 実験記録をPDFにまとめる / Example 1: Create PDF of Experiment Records

```bash
python SnapPDF_tabbed.py
```

1. 「PDF Creation」タブを選択
2. レイアウト「6 images (3×2)」を選択
3. Title: "Experiment 2026-02-12"
4. Remarks: "Temperature: 25°C, Humidity: 45%"
5. Excelファイルで実験パラメータを選択（オプション）
6. 実験写真を選択
7. 「Output to PDF」をクリック

### 例2: PDF内のキーワード検索 / Example 2: Search for Keywords in PDFs

```bash
python SnapPDF_tabbed.py
```

1. 「PDF Search」タブを選択
2. キーワード入力: "実験 結果"
3. AND検索を選択
4. 「Select directory」でフォルダを選択
5. 検索結果が表示され、CSVファイルが生成されます

---

## 🌟 主な特徴 / Key Features

### マルチプラットフォーム対応 / Multi-platform Support

SnapPDF_tabbed.pyは、Windows、macOS、Linuxで動作し、各OSに最適なフォントを自動的に選択します。

SnapPDF_tabbed.py works on Windows, macOS, and Linux, automatically selecting optimal fonts for each OS.

### タブインターフェース / Tabbed Interface

PDF作成とPDF検索を1つのウィンドウで切り替えられる直感的なインターフェース。

Intuitive interface allowing you to switch between PDF creation and search in one window.

---

## 📞 サポート / Support

### ヘルプが必要ですか？ / Need Help?

- **GitHub Issues**: https://github.com/Mizuho-NAGATA/SnapPDF/issues
- **詳細ガイド / Detailed Guide**: [TABBED_VERSION_GUIDE.md](guides/TABBED_VERSION_GUIDE.md)
- **技術詳細 / Technical Details**: [ARCHITECTURE.md](development/ARCHITECTURE.md)

### バグを見つけた場合 / Found a Bug?

GitHub Issuesでバグ報告をお願いします。以下の情報を含めてください：

Please report bugs on GitHub Issues with the following information:

1. 使用しているOS / Operating system
2. Pythonバージョン / Python version
3. エラーメッセージ / Error message
4. 再現手順 / Steps to reproduce

---

## 🎓 次のステップ / Next Steps

### もっと詳しく知りたい方へ / For More Information

- **[TABBED_VERSION_GUIDE.md](guides/TABBED_VERSION_GUIDE.md)** - 詳細な使用方法とトラブルシューティング
- **[ARCHITECTURE.md](development/ARCHITECTURE.md)** - システムアーキテクチャ
- **[TABBED_IMPLEMENTATION.md](development/TABBED_IMPLEMENTATION.md)** - タブ版の実装詳細

### フィードバックをお願いします / We Want Your Feedback

このツールを改善するため、ぜひフィードバックをお寄せください！

Help us improve this tool by providing feedback!

---

**Last Updated**: 2026-02-13  
**Version**: Tabbed 1.0  
**Ready to Use**: ✅

---

## 🎉 さあ、始めましょう！ / Let's Get Started!

```bash
python SnapPDF_tabbed.py
```

簡単、高速、パワフル - SnapPDF_tabbed.py

Easy, Fast, Powerful - SnapPDF_tabbed.py
