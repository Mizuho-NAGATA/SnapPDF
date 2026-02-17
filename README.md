# SnapPDF

[![CI](https://github.com/Mizuho-NAGATA/SnapPDF/actions/workflows/ci.yml/badge.svg)](https://github.com/Mizuho-NAGATA/SnapPDF/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

複数の写真を選択して高速に PDF 化、Excel の読み込みで画像を結合出力できます。

## Quick install (recommended)

1. Clone or download the repo
2. Create a virtual environment (recommended)
   - python -m venv .venv
   - source .venv/bin/activate  # macOS / Linux
   - .venv\Scripts\activate     # Windows
3. Install dependencies
   - pip install --upgrade pip
   - pip install -r requirements.txt

---

## SnapPDF v3.0.0

### 複数の画像を PDF ファイルにひとまとめ | Combine Multiple Images into One PDF File

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue.svg" alt="Python 3.x">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Multi-platform">
</p>

![Image](https://github.com/user-attachments/assets/3b692d8d-6bf5-4989-85f0-98c94426b4bc)

複数の画像を一つの PDF にまとめます。PDF の生成と PDF 本文検索をひとつの GUI に統合。  
タブ切り替えで両機能を行き来でき、作業を一つのアプリケーションで完結できます。  
たくさんの写真をひとまとめにしたい、特定の単語を含む PDF を検索したい、という思いから作りました。  
SnapPDF is a tool that combines multiple images into a single PDF file. The included PDFSearch allows you to search PDF content.

---

## 主な機能

- **複数画像の PDF 化**  
  画像をまとめて 1 つの PDF に統合できます。

- **複数フォルダの選択に対応**  
  異なるディレクトリからの画像選択が可能です。

- **柔軟なレイアウト設定**  
  2 / 4 / 6 / 15 枚など、用途に応じたレイアウトを選べます。

- **Excel 連携**  
  Excel からのデータ取り込みに対応しています。

- **画像の回転・順番入れ替え・削除**  
  登録する画像を回転させたり、順番を入れ替えることができます。削除もできます。

- **PDF 本文検索機能**  
  PDFSearch により、選択したフォルダ内の PDF 本文を検索できます。

- **マルチプラットフォーム対応**  
  Windows / macOS / Linux で動作します。

---

## インストール

### 必要環境
- Python 3.x

### pip を最新化して一括インストール
macOS / Linux / Windows:  
```bash
python -m pip install --upgrade pip
python -m pip install pandas pillow PyPDF2 reportlab openpyxl xlrd
python SnapPDF.py
```

### Linux での追加設定
```bash
# Ubuntu/Debian
sudo apt-get install xdg-utils

# Fedora/RHEL/CentOS
sudo yum install xdg-utils
```

---

## 使用ライブラリとその役割 / Dependencies and their roles

- **Pillow**  
  画像の読み込み、リサイズ、回転、保存などの基本的な画像処理

- **reportlab**  
  PDF ページの生成、画像の配置、レイアウト描画

- **PyPDF2**  
  既存 PDF の結合、分割、メタデータ操作や簡易なテキスト抽出（PDFSearch の本文読み取りで補助的に利用）

- **pandas**  
  Excel データの取り込みと整形。インポートしたデータをアプリ内で扱いやすく変換。

- **xlrd**  
  古い  .xls ファイルの読み込み（pandas の Excel 読み込みの補助）

- **tkinter**  
  GUI全般（Notebook, Tabs, Dialog など）

- **tkinterdnd2**  
  ファイルのドラッグ＆ドロップ対応

- **xdg-utils (Linux)**  
  Linux 環境で外部プログラムからファイルを開く等のユーティリティ（例: xdg-open）として必要になる場合がある。  

注意: ライブラリのバージョンによっては挙動や互換性が異なるため、特定の環境で問題が発生した場合はバージョン固定や代替ライブラリの検討を推奨します。OCR 機能は本プロジェクトに含まれていないため、PDF 内の画像から直接テキストを抽出したい場合は別途 OCR（Tesseract 等）の導入が必要です。

---

## ドキュメント  
開発者向け情報は [docs/](docs/) フォルダをご覧ください。
For detailed documentation, see the [docs/](docs/) folder.

- [開発者向け / Development](docs/development/) - アーキテクチャと技術詳細

---

## 著者  
**NAGATA Mizuho**  
Institute of Laser Engineering, The University of Osaka

---

## ライセンス  
このプロジェクトは MIT ライセンスで公開されています。詳細は [LICENSE](LICENSE) をご覧ください。  
This project is released under the MIT License. See [LICENSE](LICENSE) for details.

---

## 謝辞  
- このプログラムは ChatGPT と Copilot の助力により開発されました
- 本開発は文部科学省先端研究基盤共用促進事業（JPMXS0450300021）[パワーレーザーDXプラットフォーム](https://powerlaser.jp/)の成果です
