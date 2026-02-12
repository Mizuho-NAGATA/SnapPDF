# SnapPDF Unified - Quick Start Guide
# SnapPDF統合版 - クイックスタートガイド

## 🚀 5分で始める / Get Started in 5 Minutes

### ステップ1: 必要なパッケージをインストール / Step 1: Install Required Packages

```bash
pip install Pillow reportlab pandas
```

### ステップ2: プログラムを起動 / Step 2: Launch the Program

```bash
python SnapPDF_unified.py
```

### ステップ3: レイアウトを選択 / Step 3: Select Layout

プログラムが起動したら、希望するレイアウトを選択します：

Choose your desired layout when the program starts:

- **2 images (1×2)** - 最大サイズで2枚 / 2 photos in maximum size
- **4 images (2×2)** - バランスの良い4枚 / 4 photos in balanced size
- **5 images (5×1)** - 横並びで5枚 / 5 photos in horizontal strip
- **6 images (3×2)** - 推奨・6枚 / 6 photos (recommended)
- **15 images (5×3)** - コンパクトに15枚 / 15 photos compactly

### ステップ4: 画像を選択 / Step 4: Select Images

1. 「Select Images」ボタンをクリック
2. 画像ファイルを選択（複数選択可能）
3. サムネイルが表示されます

Click "Select Images" button, choose image files (multiple selection allowed), and thumbnails will be displayed.

### ステップ5: PDFを出力 / Step 5: Output PDF

「Output to PDF」ボタンをクリックすると、PDFが生成され自動的に開きます。

Click "Output to PDF" button, and the PDF will be generated and automatically opened.

---

## 📖 基本的な使い方 / Basic Usage

### タイトルと備考を追加 / Add Title and Remarks

```
┌─────────────────────────────┐
│ Title:   [Your Title Here]  │
│ Remarks: [Your Notes Here]  │
└─────────────────────────────┘
```

タイトルと備考は各ページのヘッダーに表示されます。

Title and remarks will appear in the header of each page.

### Excel連携（オプション）/ Excel Integration (Optional)

Excel形式のデータテーブルをPDFに含めることができます：

You can include Excel data tables in the PDF:

1. 「Select Excel File (Optional)」ボタンをクリック
2. Excelファイル（.xlsx または .xls）を選択
3. PDFの最初にテーブルとして表示されます

Click "Select Excel File (Optional)", choose an Excel file (.xlsx or .xls), and it will appear as a table at the beginning of the PDF.

---

## 💡 便利な使い方 / Useful Tips

### レイアウトの選び方 / How to Choose Layout

| 用途 / Purpose | 推奨レイアウト / Recommended |
|----------------|----------------------------|
| 詳細な写真記録 / Detailed photo records | 2 images (1×2) |
| 実験結果の比較 / Experiment comparison | 4 images (2×2) |
| イベント記録 / Event documentation | 6 images (3×2) ⭐ |
| サムネイル一覧 / Thumbnail overview | 15 images (5×3) |

### ファイル名のルール / File Naming Rules

生成されるPDFファイル名は自動的に日時で命名されます：

Generated PDF files are automatically named with date and time:

```
YYMMDD_HHMMSS.pdf
例 / Example: 260212_143025.pdf
```

---

## ⚠️ トラブルシューティング / Troubleshooting

### エラー: モジュールが見つからない / Error: Module not found

```bash
# 必要なパッケージを再インストール
pip install --upgrade Pillow reportlab pandas
```

### PDFが開かない / PDF doesn't open

PDFは作業ディレクトリに保存されます。手動で開いてください。

The PDF is saved in the working directory. Open it manually.

### 日本語フォントが表示されない / Japanese fonts not displaying

BIZ-UDGothicR.ttcフォントがシステムにインストールされていることを確認してください。

Ensure BIZ-UDGothicR.ttc font is installed on your system.

---

## 🎯 よくある質問 / FAQ

### Q: 統合版は従来版と何が違いますか？

A: 統合版では5つの異なるレイアウトを1つのプログラムで切り替えられます。従来版では各レイアウトごとに別のプログラムを起動する必要がありました。

### Q: How is the unified version different from traditional versions?

A: The unified version allows you to switch between 5 different layouts in one program. Traditional versions required launching separate programs for each layout.

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

---

## 📱 実行例 / Usage Example

### 例1: 実験記録をPDFにまとめる / Example 1: Create PDF of Experiment Records

```bash
python SnapPDF_unified.py
```

1. レイアウト「6 images (3×2)」を選択
2. Title: "Experiment 2026-02-12"
3. Remarks: "Temperature: 25°C, Humidity: 45%"
4. Excelファイルで実験パラメータを選択
5. 実験写真を選択
6. 「Output to PDF」をクリック

### 例2: イベント写真アルバム / Example 2: Event Photo Album

```bash
python SnapPDF_unified.py
```

1. レイアウト「15 images (5×3)」を選択
2. Title: "Lab Meeting 2026-02-12"
3. イベント写真を選択（多数）
4. 「Output to PDF」をクリック

---

## 🔧 詳細設定 / Advanced Settings

### カスタムレイアウトの追加 / Adding Custom Layouts

将来のアップデートで、カスタムレイアウトの定義が可能になる予定です。

Future updates will allow custom layout definitions.

### バッチ処理 / Batch Processing

複数のPDFを一度に生成する機能は、将来のアップデートで追加予定です。

Batch processing to generate multiple PDFs at once is planned for future updates.

---

## 📞 サポート / Support

### ヘルプが必要ですか？ / Need Help?

- **GitHub Issues**: https://github.com/Mizuho-NAGATA/SnapPDF/issues
- **Documentation**: README.md, UNIFIED_VERSION_GUIDE.md
- **Technical Details**: ARCHITECTURE.md

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

- **UNIFIED_VERSION_GUIDE.md** - 詳細な使用方法と移行ガイド
- **REFACTORING_SUMMARY.md** - 統合版の技術的な詳細
- **ARCHITECTURE.md** - システムアーキテクチャ

### フィードバックをお願いします / We Want Your Feedback

このツールを改善するため、ぜひフィードバックをお寄せください！

Help us improve this tool by providing feedback!

---

**Last Updated**: 2026-02-12  
**Version**: 1.0  
**Ready to Use**: ✅

---

## 🎉 さあ、始めましょう！ / Let's Get Started!

```bash
python SnapPDF_unified.py
```

簡単、高速、パワフル - SnapPDF Unified

Easy, Fast, Powerful - SnapPDF Unified
