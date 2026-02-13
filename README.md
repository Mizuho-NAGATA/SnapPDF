# SnapPDF

## 複数の画像を一つのPDFファイルに統合 | Combine Multiple Images into One PDF File

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue.svg" alt="Python 3.x">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Multi-platform">
</p>

![SnapPDF-3 0](https://github.com/user-attachments/assets/158fc541-e4b9-4d77-9bde-990a42a2f883)

複数の画像を一つの PDF にまとめます。PDF の生成と PDF 本文検索をひとつの GUI に統合。日常的な資料作成から研究用途まで幅広く活用できます。  
たくさんの写真をひとまとめにしたい、特定の単語を含む PDF を検索したい、という思いから作りました。  
SnapPDF is a tool that combines multiple images into a single PDF file. The included PDFSearch allows you to search PDF content.

---

## 概要  
SnapPDF は、画像ファイルをまとめて PDF 化する機能と、PDF 内のテキスト検索を行う PDFSearch を備えています。タブ切り替えで両機能を行き来でき、作業を一つのアプリケーションで完結できます。

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

## クイックスタート

### SnapPDF.py  
PDF 作成と検索を統合した GUI 版です。

```bash
pip install Pillow reportlab PyPDF2 pandas tkinterdnd2 xlrd
python SnapPDF.py
```

詳細な手順やガイドは **docs/** フォルダにまとめています。
For detailed guides, see the [docs/](docs/) folder

- [クイックスタートガイド / Quick Start Guide](docs/QUICKSTART.md)
- [タブ版完全ガイド / Tabbed Version Guide](docs/guides/TABBED_VERSION_GUIDE.md)

---

## インストール

### 必要環境
- Python 3.x

### 基本パッケージ
```bash
pip install Pillow reportlab PyPDF2 pandas tkinterdnd2 xlrd
```

### Linux での追加設定
```bash
# Ubuntu/Debian
sudo apt-get install xdg-utils

# Fedora/RHEL/CentOS
sudo yum install xdg-utils
```

---

## ドキュメント  
より詳しい説明や開発者向け情報は [docs/](docs/) フォルダをご覧ください。
For detailed documentation, see the [docs/](docs/) folder.

- [クイックスタート / Quick Start](docs/QUICKSTART.md)
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
- 第2回身近な研究DXコンテスト2023 受賞作品
