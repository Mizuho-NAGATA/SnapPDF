# SnapPDF v2.0 - Unified Image to PDF Converter

***DEMO:***  
![SnapPDF demo video](https://github.com/Mizuho-NAGATA/SnapPDF/blob/main/SnapPDF%20demo%20video.gif?raw=true)

「SnapPDF v2.0」は、複数の画像を一つのPDFファイルにまとめるシンプルで強力なツールの統合版です。  
従来の5つの異なるバージョンを1つのアプリケーションに統合し、レイアウトを選択できるようになりました。  

"SnapPDF v2.0" is a unified version of the simple and powerful tool that combines multiple images into a single PDF file. It integrates the previous 5 different versions into one application with selectable layout options.

---

## 📑 目次 / Table of Contents

1. [新機能 / What's New in v2.0](#新機能--whats-new-in-v20)
2. [特徴 / Features](#特徴--features)
3. [インストールガイド / Installation Guide](#インストールガイド--installation-guide)
4. [起動方法 / How to Run](HOW_TO_RUN.md) ⭐
5. [使い方 / Usage](#使い方--usage)
6. [レイアウトオプション / Layout Options](#レイアウトオプション--layout-options)
7. [SnapSearch](#snapsearch)
8. [依存関係 / Dependencies](#依存関係--dependencies)
9. [旧バージョンからの移行 / Migration from Old Versions](#旧バージョンからの移行--migration-from-old-versions)
10. [トラブルシューティング / Troubleshooting](#トラブルシューティング--troubleshooting)
11. [開発者向け情報 / Developer Information](#開発者向け情報--developer-information)
12. [著者 / Author](#著者--author)
13. [ライセンス / License](#ライセンス--license)
14. [謝辞 / Acknowledgments](#謝辞--acknowledgments)

---

## 🎉 新機能 / What's New in v2.0

### 主な改善点 / Major Improvements

✨ **統合アプリケーション / Unified Application**
- 5つの別々のファイル（SnapPDF.py, SnapPDF2.py, SnapPDF4.py, SnapPDF6.py, SnapPDF15.py）を1つのアプリケーションに統合
- Integrated 5 separate files into one application

🎨 **レイアウト選択 / Layout Selection**
- GUIからレイアウトを簡単に選択可能（2, 4, 6, 15枚/ページ）
- Easy layout selection from GUI (2, 4, 6, 15 images per page)

🔧 **改善されたコード品質 / Improved Code Quality**
- クラスベースの設計で保守性が向上
- Better maintainability with class-based design
- エラーハンドリングの強化
- Enhanced error handling
- 並列処理による高速化
- Faster processing with parallel execution

📋 **すべてのバージョンで統一された機能 / Unified Features**
- 画像の並び替え（上下移動、削除）
- Image reordering (move up/down, delete)
- サムネイルプレビュー
- Thumbnail preview
- Excelデータ統合（オプション）
- Excel data integration (optional)

🐛 **バグ修正 / Bug Fixes**
- SnapSearch.pyのインデントエラーを修正
- Fixed indentation error in SnapSearch.py
- フォント読み込みのフォールバック処理を追加
- Added fallback for font loading

---

## 🌟 特徴 / Features

### 基本機能 / Basic Features
- ✅ 複数の画像を一つのPDFに統合 / Combine multiple images into one PDF
- ✅ 複数のフォルダから画像を選択可能 / Select images from multiple folders
- ✅ 5つのレイアウトオプション / 5 layout options (2, 4, 6, 15 images per page, Excel+Images)
- ✅ Excelデータとの統合 / Integration with Excel data
- ✅ 画像の順序変更機能 / Image reordering capability
- ✅ リアルタイムサムネイルプレビュー / Real-time thumbnail preview
- ✅ 日本語フォント対応 / Japanese font support
- ✅ タイトルと備考の追加 / Add title and remarks

### 高度な機能 / Advanced Features
- ⚡ 並列処理による高速PDF生成 / Fast PDF generation with parallel processing
- 🎯 アスペクト比を維持した画像配置 / Image placement maintaining aspect ratio
- 📊 Excelテーブルの自動整形 / Automatic Excel table formatting
- 🖼️ 最適な画像サイズ自動計算 / Automatic optimal image size calculation
- 💾 タイムスタンプ付きファイル名 / Timestamped filename
- 🔄 レイアウトの動的切り替え / Dynamic layout switching

---

## 📦 インストールガイド / Installation Guide

### 1. Pythonのインストール / Python Installation

SnapPDF v2.0はPython 3.7以上を必要とします。  
SnapPDF v2.0 requires Python 3.7 or higher.

1. [Python公式ウェブサイト](https://www.python.org/downloads/)にアクセス
2. お使いのOSに合わせたPython 3.xをダウンロード
3. インストーラーを実行（Windowsの場合は"Add Python to PATH"にチェック）
4. インストール確認：
   ```bash
   python --version
   ```

### 2. 依存パッケージのインストール / Install Dependencies

```bash
# 全ての依存パッケージを一括インストール
pip install -r requirements.txt

# または個別にインストール
pip install Pillow reportlab pandas PyPDF2

# オプション：ドラッグ&ドロップ機能を有効にする場合
pip install tkinterdnd2
```

### 3. フォントファイルの準備 / Font File Preparation

日本語表示のために、システムに`BIZ-UDGothicR.ttc`フォントがあることを確認してください。  
フォントが見つからない場合、自動的にHelveticaにフォールバックします。

For Japanese text display, ensure `BIZ-UDGothicR.ttc` font is available on your system.  
If not found, it will automatically fallback to Helvetica.

---

## 🚀 使い方 / Usage

### 基本的な使い方 / Basic Usage

1. **アプリケーションの起動 / Launch Application**
   
   **方法1: バッチファイルで起動（Windows・推奨）/ Using Batch File (Windows - Recommended)**
   ```bash
   run_snappdf.bat
   ```
   
   **方法2: Pythonコマンドで起動 / Using Python Command**
   ```bash
   python snappdf_unified.py
   ```

2. **レイアウトの選択 / Select Layout**
   - ドロップダウンメニューから希望のレイアウトを選択
   - Select desired layout from dropdown menu

3. **画像の選択 / Select Images**
   - 「Select Images」ボタンをクリック
   - 複数の画像ファイルを選択
   - 画像の順序を変更したい場合は、↑/↓ボタンを使用

4. **タイトルと備考の入力（オプション）/ Enter Title and Remarks (Optional)**
   - PDFに表示したいタイトルと備考を入力

5. **Excelデータの追加（オプション）/ Add Excel Data (Optional)**
   - 「Select Excel File」ボタンをクリック
   - Excelファイルを選択すると、PDFの先頭にテーブルとして追加されます

6. **PDF作成 / Create PDF**
   - 「📄 Create PDF」ボタンをクリック
   - PDFが自動的に生成され、デフォルトのビューアーで開きます

### 画像の管理 / Image Management

- **順序変更 / Reorder**: 画像を選択して↑/↓ボタンで移動
- **削除 / Delete**: 画像を選択して「✖ Delete Selected」ボタン
- **全削除 / Clear All**: 「Clear All Images」ボタンで全ての画像を削除
- **プレビュー / Preview**: 下部のサムネイルエリアで画像をプレビュー

---

## 🎨 レイアウトオプション / Layout Options

### Large (2 per page)
- **1ページあたり**: 2枚の写真
- **配置**: 2列 × 1行
- **用途**: 写真を大きく、詳細に表示したい場合
- **Use case**: Best for detailed viewing of photos

### Medium (4 per page)
- **1ページあたり**: 4枚の写真
- **配置**: 2列 × 2行
- **用途**: バランスの取れたサイズ
- **Use case**: Balanced size for most purposes

### Standard (6 per page)
- **1ページあたり**: 6枚の写真
- **配置**: 3列 × 2行
- **用途**: 標準的なフォトアルバムに最適
- **Use case**: Good balance for photo albums

### Compact (15 per page)
- **1ページあたり**: 15枚の写真
- **配置**: 5列 × 3行
- **用途**: コンパクトなアルバム、多くの写真を1ページに
- **Use case**: Maximum density for compact albums

### Excel + Images (5 per page)
- **1ページあたり**: Excelテーブル + 5枚の写真
- **配置**: テーブル（上部） + 5列 × 1行（下部）
- **用途**: データと写真を組み合わせたレポート
- **Use case**: Reports combining data and photos

**注意**: 縦長の写真を含むと、1ページあたりの出力枚数が少なくなることがあります。  
**Note**: Including portrait-oriented photos may reduce the number of images per page.

---

## 🔍 SnapSearch

SnapSearchは、PDFファイルの中身をキーワードで検索し、一致する内容を持つファイルを見つけ出す強力なツールです。  
SnapSearch is a powerful tool that searches the contents of PDF files by keywords.

### 使い方 / Usage

1. **起動 / Launch**
   
   **方法1: バッチファイルで起動（Windows・推奨）/ Using Batch File (Windows - Recommended)**
   ```bash
   run_snapsearch.bat
   ```
   
   **方法2: Pythonコマンドで起動 / Using Python Command**
   ```bash
   python SnapSearch.py
   ```

2. **検索キーワードの入力 / Enter Keywords**
   - スペースで区切って複数のキーワードを入力
   - 日本語も検索可能

3. **検索タイプの選択 / Select Search Type**
   - ☑ AND検索: すべてのキーワードを含むファイルを検索
   - ☐ OR検索: いずれかのキーワードを含むファイルを検索

4. **ディレクトリの選択 / Select Directory**
   - 「Select directory」ボタンをクリック
   - 検索対象のディレクトリを選択

5. **結果の確認 / View Results**
   - 検索結果がウィンドウに表示されます
   - タイムスタンプ付きCSVファイルとして保存されます

### 特記事項 / Notes

日本語環境の場合、`PdfReadWarning: Advanced encoding /UniJIS-UCS2-H not implemented yet`という警告が表示されることがありますが、検索は正常に実行されます。

In Japanese environments, you may see a warning about advanced encoding, but the search will continue normally.

---

## 📚 依存関係 / Dependencies

### 必須 / Required
- **Python**: 3.7+
- **Pillow**: 画像処理 / Image processing
- **reportlab**: PDF生成 / PDF generation
- **pandas**: Excelデータ読み込み / Excel data reading
- **tkinter**: GUI（Python標準ライブラリ）/ GUI (Python standard library)
- **PyPDF2**: PDF検索（SnapSearch用）/ PDF search (for SnapSearch)

### オプション / Optional
- **tkinterdnd2**: ドラッグ&ドロップ機能 / Drag-and-drop functionality

### インストールコマンド / Installation Commands

```bash
# 必須パッケージ
pip install Pillow reportlab pandas PyPDF2

# オプション
pip install tkinterdnd2
```

---

## 🔄 旧バージョンからの移行 / Migration from Old Versions

### v1.2.2から v2.0への移行 / Migrating from v1.2.2 to v2.0

旧バージョンのファイル（SnapPDF.py, SnapPDF2.py等）は引き続き使用できますが、新しい統合版の使用を推奨します。

The old version files (SnapPDF.py, SnapPDF2.py, etc.) will continue to work, but we recommend using the new unified version.

**移行手順 / Migration Steps:**

1. 依存パッケージをインストール
   ```bash
   pip install -r requirements.txt
   ```

2. 新しい統合版を起動
   ```bash
   python snappdf_unified.py
   ```

3. レイアウトを選択（旧バージョンに対応）
   - SnapPDF2.py → "Large (2 per page)"
   - SnapPDF4.py → "Medium (4 per page)"
   - SnapPDF6.py → "Standard (6 per page)"
   - SnapPDF15.py → "Compact (15 per page)"
   - SnapPDF.py → "Excel + Images (5 per page)"

**互換性 / Compatibility:**
- 生成されるPDFの形式は旧バージョンと互換性があります
- Generated PDFs are compatible with old versions

---

## 🔧 トラブルシューティング / Troubleshooting

### よくある問題 / Common Issues

#### 1. フォントエラー / Font Error
```
Warning: Could not load font BIZ-UDGothicR.ttc
```
**解決方法 / Solution:**
- システムにフォントをインストールするか、Helveticaフォールバックを使用（自動）
- Install the font on your system, or use Helvetica fallback (automatic)

#### 2. tkinterが見つからない / tkinter not found
```
ModuleNotFoundError: No module named 'tkinter'
```
**解決方法 / Solution:**
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **macOS**: Python.orgからインストールしたPythonを使用
- **Windows**: Pythonインストーラーに含まれています

#### 3. 画像が読み込めない / Cannot load images
**解決方法 / Solution:**
- サポートされている形式か確認（JPG, JPEG, PNG, BMP, GIF, TIFF）
- ファイルが破損していないか確認
- ファイルパスに特殊文字が含まれていないか確認

#### 4. PDFが開かない / PDF won't open
**解決方法 / Solution:**
- PDFリーダーがインストールされているか確認
- 出力先ディレクトリの書き込み権限を確認
- 手動でファイルを開いてエラーメッセージを確認

#### 5. Excelファイルが読み込めない / Cannot load Excel file
**解決方法 / Solution:**
- pandasがインストールされているか確認
- ファイル形式が.xlsxまたは.xlsか確認
- Excelファイルが開かれていないか確認

---

## 👨‍💻 開発者向け情報 / Developer Information

### プロジェクト構造 / Project Structure

```
SnapPDF-1.2.2/
├── snappdf/                  # Main package
│   ├── __init__.py          # Package initialization
│   ├── config.py            # Configuration and layout definitions
│   ├── core.py              # PDF generation logic
│   ├── ui.py                # GUI implementation
│   └── utils.py             # Utility functions
├── snappdf_unified.py       # Main entry point (NEW!)
├── SnapSearch.py            # PDF search tool (Fixed)
├── SnapPDF.py               # Legacy version (still works)
├── SnapPDF2.py              # Legacy version
├── SnapPDF4.py              # Legacy version
├── SnapPDF6.py              # Legacy version
├── SnapPDF15.py             # Legacy version
├── requirements.txt         # Dependencies
├── README.md                # Original README
├── README_v2.md             # This file
└── LICENSE                  # MIT License
```

### APIの使用例 / API Usage Example

```python
from snappdf import PDFGenerator, AppConfig

# レイアウトを取得
layout = AppConfig.get_layout("compact")  # 15 images per page

# PDFジェネレーターを作成
generator = PDFGenerator(layout)

# 画像を追加
generator.add_images([
    "path/to/image1.jpg",
    "path/to/image2.jpg",
    "path/to/image3.jpg"
])

# Excelデータを読み込み（オプション）
generator.load_excel_data("path/to/data.xlsx")

# PDFを生成
success, message = generator.generate_pdf(
    output_path="output.pdf",
    title="My Photo Album",
    remarks="Created with SnapPDF v2.0"
)

print(message)
```

### カスタムレイアウトの追加 / Adding Custom Layouts

`snappdf/config.py`を編集して、新しいレイアウトを追加できます：

```python
"custom": LayoutConfig(
    name="custom",
    display_name="Custom (8 per page)",
    images_per_page=8,
    columns=4,
    rows=2,
    description="Custom 4x2 layout"
)
```

### テスト / Testing

```bash
# 統合版のテスト
python snappdf_unified.py

# SnapSearchのテスト
python SnapSearch.py
```

---

## 👤 著者 / Author

**NAGATA Mizuho (永田 みず穂)**  
Institute of Laser Engineering, The University of Osaka

Copyright (c) 2023-2026 NAGATA Mizuho

---

## 📄 ライセンス / License

このプロジェクトはMITライセンスの下で公開されています。  
This project is released under the MIT License.

詳細については、[LICENSE](LICENSE)ファイルをご覧ください。  
For details, see the [LICENSE](LICENSE) file.

---

## 🙏 謝辞 / Acknowledgments

- このプログラムは、ChatGPTの助力によって開発されました。また、ChatGPTを紹介してくれた私の家族に感謝します。
- このREADMEファイルは、Copilotの協力によって作成されました。
- **v2.0のリファクタリングは、Claude (Anthropic)の支援により実現しました。**
- 本開発は文部科学省先端研究基盤共用促進事業（先端研究設備プラットフォームプログラム）JPMXS0450300021である[パワーレーザーDXプラットフォーム](https://powerlaser.jp/)で共用された機器を利用した成果です。
- このプログラムは、第2回身近な研究DXコンテスト2023の受賞作品です。

---

- This program was developed with the assistance of ChatGPT. I would like to express my gratitude to my family for introducing me to ChatGPT.
- This README file was created with the help of Copilot.
- **The v2.0 refactoring was accomplished with assistance from Claude (Anthropic).**
- This work was the result of using research equipment shared by the ["Power Laser DX Platform"](https://powerlaser.jp/), which is MEXT Project for promoting public utilization of advanced research infrastructure (Program for advanced research equipment platforms) Grant Number JPMXS0450300021.
- This program is the winner of the 2nd Familiar Research DX Contest 2023.

---

## 📞 サポート / Support

問題が発生した場合や機能のリクエストがある場合は、GitHubのIssuesページをご利用ください。

For issues or feature requests, please use the GitHub Issues page.

---

**Enjoy using SnapPDF v2.0! 📸 → 📄**