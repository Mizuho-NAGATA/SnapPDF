# SnapPDF

## 複数の画像を一つのPDFファイルに統合 | Combine Multiple Images into One PDF File

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue.svg" alt="Python 3.x">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Multi-platform">
</p>

![SnapPDF demo video](https://github.com/Mizuho-NAGATA/SnapPDF/blob/main/SnapPDF%20demo%20video.gif?raw=true)

SnapPDF は複数の画像を一つのPDFファイルに統合するツールです。PDFSearch で PDF 本文を検索できます。  
SnapPDF is a tool that combines multiple images into a single PDF file. The included PDFSearch allows you to search PDF content.

---

## ✨ 主な機能 | Key Features

- 🖼️ **複数画像を PDF に統合** | Combine multiple images into one PDF
- 📁 **複数フォルダ対応** | Select images from multiple folders  
- 🎨 **柔軟なレイアウト** | Flexible layouts (2/4/5/6/15 images per page)
- 📊 **Excel 連携** | Excel import support
- 🚀 **並列処理で高速** | Fast parallel processing
- 🔍 **PDF 検索機能** | Built-in PDF search (PDFSearch)
- 🖥️ **マルチプラットフォーム** | Windows / macOS / Linux support

## 🚀 クイックスタート | Quick Start

### おすすめバージョン | Recommended Versions

#### 🆕 SnapPDF_tabbed.py（最新・推奨）
PDF 作成と検索を1つの GUI で統合。マルチプラットフォーム対応。  
**Unified PDF creation and search in one GUI with multi-platform support.**

```bash
pip install Pillow reportlab PyPDF2
python SnapPDF_tabbed.py
```

📖 **詳細なガイドは [docs/](docs/) フォルダをご覧ください**  
📖 **For detailed guides, see the [docs/](docs/) folder**

- [クイックスタートガイド / Quick Start Guide](docs/QUICKSTART.md)
- [タブ版完全ガイド / Tabbed Version Guide](docs/guides/TABBED_VERSION_GUIDE.md)
- [統合版ガイド / Unified Version Guide](docs/guides/UNIFIED_VERSION_GUIDE.md)

## 📦 インストール | Installation

### 必要な環境 | Requirements
- Python 3.x

### 基本パッケージ | Basic Packages
```bash
pip install Pillow reportlab
```

### タブ版使用時 | For Tabbed Version
```bash
pip install PyPDF2
```

### Excel 連携時 | For Excel Support
```bash
pip install pandas tkinterdnd2
```

### Linux の場合 | For Linux Users
```bash
# Ubuntu/Debian
sudo apt-get install xdg-utils

# Fedora/RHEL/CentOS
sudo yum install xdg-utils
```

## 📖 ドキュメント | Documentation

詳細なドキュメントは [docs/](docs/) フォルダをご覧ください。  
For detailed documentation, see the [docs/](docs/) folder.

- **[クイックスタート / Quick Start](docs/QUICKSTART.md)** - 5分で始める
- **[ユーザーガイド / User Guides](docs/guides/)** - 各バージョンの詳細ガイド
- **[開発者向け / Development](docs/development/)** - アーキテクチャと技術詳細

## 🔧 利用可能なバージョン | Available Versions

### 最新版 | Latest Versions
- **SnapPDF_tabbed.py** - タブ統合版（推奨）/ Tabbed unified version (Recommended)

### 従来版 | Traditional Versions
- SnapPDF.py, SnapPDF2.py, SnapPDF4.py, SnapPDF6.py, SnapPDF15.py
- PDFSearch.py - PDF検索ツール / PDF search tool

*従来版は後方互換性のために保持されています。新規ユーザーには最新版の使用を推奨します。*  
*Traditional versions are kept for backward compatibility. New users should use the latest versions.*

## 👤 著者 | Author

**NAGATA Mizuho** (永田 みず穂)  
Institute of Laser Engineering, The University of Osaka

## 📄 ライセンス | License

このプロジェクトは MIT ライセンスで公開されています。詳細は [LICENSE](LICENSE) をご覧ください。  
This project is released under the MIT License. See [LICENSE](LICENSE) for details.

## 🙏 謝辞 | Acknowledgments

- このプログラムは ChatGPT と Copilot の助力により開発されました
- 本開発は文部科学省先端研究基盤共用促進事業（JPMXS0450300021）[パワーレーザーDXプラットフォーム](https://powerlaser.jp/)の成果です
- 第2回身近な研究DXコンテスト2023 受賞作品

---
