# SnapPDF Tabbed Version Guide
# SnapPDF タブ付き統合版ガイド

## 🆕 概要 / Overview

SnapPDF (`SnapPDF.py`) は、PDF作成とPDF検索を1つのGUIで統合し、マルチプラットフォーム対応を実現した最新バージョンです。

SnapPDF (`SnapPDF.py`) is the latest version that integrates PDF creation and search in one GUI with multi-platform support.

---

## 🌟 主な特徴 / Key Features

### 1. タブインターフェース / Tabbed Interface
- **PDF作成タブ**: 画像からPDFを作成
- **PDF検索タブ**: PDFファイル内のテキストを検索
- 1つのウィンドウで両機能を簡単に切り替え

**PDF Creation Tab**: Create PDF from images
**PDF Search Tab**: Search text within PDF files
Easily switch between functions in one window

### 2. マルチプラットフォーム対応 / Multi-platform Support

自動的にOSに応じた最適なフォントを選択します：

Automatically selects optimal fonts based on OS:

#### Windows
- MS-Gothic (MS ゴシック)
- Yu Gothic (游ゴシック)
- BIZ-UDGothicR

#### macOS
- Hiragino Sans (ヒラギノ角ゴシック)
- Arial Unicode

#### Linux
- Noto Sans CJK JP
- Takao Gothic (TakaoPGothic)
- IPA Gothic (IPAゴシック)
- DejaVu Sans (フォールバック)

### 3. 文字エンコーディング修正 / Fixed Character Encoding

レイアウト表示で「×」記号が正しく表示されます：
- ❌ 従来: `3x5` (ASCII 'x'で文字化け)
- ✅ 新版: `3×5` (Unicode U+00D7)

Layout displays now show "×" symbol correctly:
- ❌ Old: `3x5` (garbled with ASCII 'x')
- ✅ New: `3×5` (proper Unicode U+00D7)

---

## 📦 インストール / Installation

### 必要なパッケージ / Required Packages

```bash
pip install Pillow reportlab pandas PyPDF2
```

### システム要件 / System Requirements

- Python 3.x
- Windows 10/11, macOS, または Linux
- 日本語フォント（自動検出・フォールバック機能付き）

---

## 🚀 使い方 / How to Use

### 起動 / Launch

```bash
python SnapPDF.py
```

---

## 📑 PDF作成タブ / PDF Creation Tab

### 基本的な使い方 / Basic Usage

1. **レイアウトを選択**
   - 2 images (1×2)
   - 4 images (2×2)
   - 5 images (5×1)
   - 6 images (3×2) ← デフォルト
   - 15 images (5×3)

2. **Excelファイルを選択（オプション）**
   - データテーブルをPDFに含めたい場合

3. **画像を選択**
   - 複数の画像ファイルを選択可能
   - サムネイルが自動的に表示されます

4. **「Output to PDF」をクリック**
   - PDFが生成され、自動的に開きます

### タイトルと備考 / Title and Remarks

```
Title: [実験記録 2026-02-12]
Remarks: [温度: 25°C, 湿度: 45%]
```

これらの情報は各PDFページのヘッダーに表示されます。

This information appears in the header of each PDF page.

### Excelデータ統合 / Excel Data Integration

Excelファイルを選択すると、データテーブルがPDFの最初に配置されます。

When you select an Excel file, the data table appears at the beginning of the PDF.

**対応形式 / Supported Formats:**
- `.xlsx` (Excel 2007以降)
- `.xls` (Excel 97-2003)

---

## 🔍 PDF検索タブ / PDF Search Tab

### 基本的な使い方 / Basic Usage

1. **検索キーワードを入力**
   - スペースで区切って複数のキーワードを入力
   - 日本語検索に対応

2. **検索モードを選択**
   - ✓ **AND検索**: すべてのキーワードを含むPDFを検索
   - ☐ **OR検索**: いずれかのキーワードを含むPDFを検索

3. **「Select directory」をクリック**
   - 検索対象のディレクトリを選択
   - サブディレクトリも自動的に検索されます

4. **結果を確認**
   - 検索結果がウィンドウに表示されます
   - CSVファイルも自動生成されます

### 検索結果 / Search Results

検索結果は以下の形式でCSVファイルに保存されます：

Search results are saved in CSV format:

```
File name,Location,Keywords
report.pdf,/path/to/report.pdf,"keyword1, keyword2"
```

**ファイル名 / Filename:**
```
search_results_20260212_143025.csv
```

---

## 🎨 GUIフォント設定 / GUI Font Configuration

### 自動選択されるフォント / Auto-selected Fonts

| OS | フォント / Font | サイズ / Size |
|----|----------------|---------------|
| Windows | Yu Gothic UI | 11 |
| macOS | Hiragino Sans | 13 |
| Linux | Noto Sans CJK JP | 11 |

---

## 💡 便利な使い方 / Tips & Tricks

### 1. 大量の画像を扱う場合 / Handling Many Images

サムネイル表示は自動的に並列処理されます。大量の画像でも高速に表示できます。

Thumbnail display is automatically parallelized. Even with many images, display is fast.

### 2. PDF検索のコツ / PDF Search Tips

**AND検索の例 / AND Search Example:**
```
実験 結果 2026
→ これら3つのキーワードすべてを含むPDFを検索
```

**OR検索の例 / OR Search Example:**
```
レポート 報告書 ドキュメント
→ これらのいずれかを含むPDFを検索
```

### 3. フォントが見つからない場合 / If Fonts Not Found

システムにフォントがインストールされていない場合、自動的にフォールバックフォントが使用されます。

If fonts are not installed on the system, fallback fonts are automatically used.

**追加フォントのインストール / Installing Additional Fonts:**

**Windows:**
- [BIZ UDゴシック](https://github.com/googlefonts/morisawa-biz-ud-gothic)

**macOS:**
- システムフォントが自動的に使用されます

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install fonts-noto-cjk fonts-takao-gothic
```

---

## 🔧 トラブルシューティング / Troubleshooting

### フォントエラー / Font Errors

**問題 / Problem:**
```
reportlab.lib.utils.TTFError: Can't find font file
```

**解決策 / Solution:**
1. 必要なフォントをインストール
2. プログラムを再起動
3. フォールバックフォント（DejaVu、Helvetica）が自動的に使用されます

### 文字化けが発生する / Garbled Characters

**問題 / Problem:**
PDFまたはGUIで文字が正しく表示されない

**解決策 / Solution:**
1. システムに日本語フォントがインストールされているか確認
2. ファイルの文字エンコーディングがUTF-8であることを確認
3. 最新版のPythonとライブラリを使用

### CSV出力が文字化けする / CSV Output Garbled

**解決策 / Solution:**
新バージョンではUTF-8エンコーディングを使用しています。ExcelでCSVを開く際は：

1. Excelで「データ」→「テキストまたはCSVから」を選択
2. ファイルの元のエンコーディングで「UTF-8」を選択

---

## 🆚 バージョン比較 / Version Comparison

| 機能 / Feature | Tabbed | Unified | Individual Files |
|---------------|--------|---------|------------------|
| PDF作成 / PDF Creation | ✓ | ✓ | ✓ |
| PDF検索 / PDF Search | ✓ | ✗ | ✗ (separate app) |
| タブインターフェース / Tabs | ✓ | ✗ | ✗ |
| マルチプラットフォーム / Multi-platform | ✓ | ✗ | ✗ |
| 文字エンコーディング修正 / Fixed encoding | ✓ | ✗ | ✗ |
| レイアウト選択 / Layout selection | ✓ | ✓ | 固定 / Fixed |

---

## 📊 技術詳細 / Technical Details

### アーキテクチャ / Architecture

```
SnapPDFTabbedApp (Main)
├── ttk.Notebook (Tab Container)
│   ├── SnapPDFTab (PDF Creation)
│   │   ├── Layout Selection
│   │   ├── Excel Import
│   │   ├── Image Selection
│   │   └── PDF Generation
│   └── PDFSearchTab (PDF Search)
│       ├── Keyword Input
│       ├── Search Mode
│       ├── Directory Search
│       └── Results Display
```

### フォント選択ロジック / Font Selection Logic

```python
def select_font_for_pdf():
    system = platform.system()
    
    if system == "Windows":
        font_candidates = [...]
    elif system == "Darwin":  # macOS
        font_candidates = [...]
    else:  # Linux
        font_candidates = [...]
    
    # Try each font candidate
    for font_name, font_path in font_candidates:
        try:
            pdfmetrics.registerFont(TTFont(font_name, font_path))
            return font_name
        except:
            continue
    
    # Fallback
    return "Helvetica"
```

---

## 🎯 今後の予定 / Future Plans

- [ ] ドラッグ＆ドロップでの画像並び替え
- [ ] PDFプレビュー機能
- [ ] カスタムレイアウトの設定保存
- [ ] バッチ処理（複数PDF一括生成）
- [ ] PDFのマージ・分割機能

---

## 📞 サポート / Support

### 問題報告 / Issue Reporting

GitHubのIssuesページでバグ報告や機能要望をお寄せください：

Please report bugs and feature requests on GitHub Issues:

**GitHub Repository:** https://github.com/Mizuho-NAGATA/SnapPDF

### よくある質問 / FAQ

**Q: 従来版との互換性は？**
A: 従来版のファイルは引き続き利用可能です。データ形式は同じです。

**Q: Compatibility with previous versions?**
A: Previous version files remain usable. Data formats are the same.

**Q: どのバージョンを使うべきですか？**
A: 新規ユーザーには `SnapPDF.py` を推奨します。

**Q: Which version should I use?**
A: We recommend `SnapPDF.py` for new users.

---

**Last Updated**: 2026-02-12  
**Version**: Tabbed 1.0  
**Status**: ✅ Production Ready

---

## 🎉 まとめ / Summary

SnapPDF Tabbed は、PDF作成とPDF検索を1つの便利なインターフェースで提供し、Windows、macOS、Linuxの各プラットフォームで適切に動作する最新バージョンです。

SnapPDF Tabbed is the latest version that provides PDF creation and search in one convenient interface, working properly on Windows, macOS, and Linux platforms.

**主な利点 / Key Benefits:**
- ✅ 統合されたインターフェース
- ✅ マルチプラットフォーム対応
- ✅ 文字化けなし
- ✅ 使いやすいタブ切り替え

ぜひお試しください！

Please give it a try!
