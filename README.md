# 📘 **SnapPDF v2.0.0 – README**

> ** SnapPDF v2.0.0 はメジャーアップデートです**  
> v1 系から内部構造を全面的に再設計しました。  
> 全バージョン（2/4/6/15/Excel版）および PDFSearch をクラス化し、処理速度・安定性・保守性が大幅に向上しました。  
> 見た目や使用方法に大きな変更はありませんが、内部機能は v1.2.2 から大幅に改善されています。

---

# SnapPDF

***DEMO:***  
![SnapPDF demo video](https://github.com/Mizuho-NAGATA/SnapPDF/blob/main/SnapPDF%20demo%20video.gif?raw=true)  
「SnapPDF」は、複数の画像を一つのPDFファイルにまとめるツールです。  
同梱の「PDFSearch」によって、保存したPDF本文を検索することができます。  
v2.0.0 は、見た目や使用方法に大きな変更はありませんが、内部機能は v1.2.2 から大幅に改善されています。  
"SnapPDF" is a simple and powerful tool that combines multiple images into a single PDF file.  
The included "PDFSearch" allows you to search the text inside saved PDF files.

---

# 🆕 **v2.0.0 での主な変更点**

> **v1.2.2 からの大幅アップデート内容**

### ✅ **1. 全コードをクラス化（最大の変更）**
- SnapPDF / SnapPDF2 / 4 / 6 / 15 / PDFSearch をすべてクラスベースに再構築  
- グローバル変数を完全撤廃  
- GUI とロジックを分離し、保守性が大幅向上

### ✅ **2. サムネイル表示の改善**
- サムネイルの下にファイル名を表示  
- 並列処理＋キャッシュで高速化  
- 大量画像でも安定して表示

### ✅ **3. PDF 出力処理の高速化**
- 画像処理を並列化  
- レイアウトを統一し、崩れにくい PDF を生成  
- SnapPDF（Excel版）も構造を整理し安定化

### ✅ **4. PDFSearch の全面リファクタリング**
- クラス化  
- AND/OR 検索のバグ修正（v1 系では最後のページしか検索されない問題）  
- 結果表示ウィンドウを改善

### ✅ **5. プロジェクト全体の品質向上**
- コードの統一  
- 拡張性の向上  
- 長期運用に耐える構造へ進化

---

## 目次 / Table of Contents
1. [SnapPDF](#snappdf)
    1. [特徴 / Features](#特徴--features)
    2. [使い方 / Usage](#使い方--usage)
    3. [各バージョンの説明 / Versions](#各バージョンの説明--versions)
    4. [バージョンの選択 / Version Selection](#バージョンの選択--version-selection)
2. [PDFSearch](#pdfsearch)
    1. [特徴 / Features](#pdfsearch-特徴--features)
    2. [使い方 / Usage](#pdfsearch-使い方--usage)
    3. [特記事項 / Notes](#pdfsearch-特記事項--notes)
3. [インストールガイド / Installation Guide](#インストールガイド--installation-guide)
4. [依存関係 / Dependencies](#依存関係--dependencies)
5. [著者 / Author](#著者--author)
6. [ライセンス / License](#ライセンス--license)
7. [謝辞 / Acknowledgments](#謝辞--acknowledgments)

# SnapPDF

## 特徴 / Features
- 複数の画像を一つのPDFに統合
- 画像は複数のフォルダから選択可能
- 「SnapPDF2, 4, 6, 15」: A4横のページに最大2, 4, 6, 15枚の写真を配置
- 「SnapPDF」：画像＋Excel データを 1 つの PDF に統合  
- クラス化により高速・安定  
- インストール不要で、Pythonスクリプトを直接実行  
- Combine multiple images into one PDF file
- Images can be selected from multiple folders
- SnapPDF2/4/6/15: place 2/4/6/15 photos per A4 landscape page  
- SnapPDF: combine images + Excel data  
- No installation required
  
## 使い方 / Usage
1. GitHubリポジトリから適切な`.py`ファイルをダウンロードしてください。
2. ダウンロードしたファイルを保存したディレクトリに移動します。
3. コマンドプロンプトまたはターミナルを開き、以下のコマンドを実行します：

例: 
```bash
python SnapPDF15.py
```

## 必要条件
- Python 3.x がシステムにインストールされていること

## 各バージョンの説明
- `SnapPDF.py`: A4横1ページにエクセルファイルと小さいサイズの写真をPDF出力。エクセルファイルを選択しない場合は、写真のみを出力。
- `SnapPDF2.py`: A4横1ページに2枚の写真をPDF出力。
- `SnapPDF4.py`: A4横1ページに4枚の写真をPDF出力。
- `SnapPDF6.py`: A4横1ページに6枚の写真をPDF出力。
- `SnapPDF15.py`: A4横1ページに15枚の写真をPDF出力。
  
注意: 縦長の写真を含むと、1ページあたりの出力枚数が少なくなることがあります。その場合はページ数が増えます。  

## バージョンの選択
- `SnapPDF2.py`: 写真を大きく、詳細に表示したい場合に適しています。
- `SnapPDF4.py`と`SnapPDF6.py`: 中間のサイズで写真を表示したいとき。
- `SnapPDF.py`と`SnapPDF15.py`: 多くの写真をコンパクトにまとめます。

# PDFSearch

PDFSearchは、PDFファイルの中身をキーワードで検索し、一致する内容を持つファイルを見つけ出すツールです。指定されたディレクトリ内のPDFファイルを対象に、入力されたキーワードでAND検索を行い、検索結果をCSVファイルに出力します。日本語も検索できます。
PDFSearch is a powerful tool that searches the contents of PDF files by keywords to find files with matching contents. It performs AND searches on PDF files in a specified directory using entered keywords and outputs the search results to a CSV file. Japanese can also be searched.  
v2.0.0 では以下を改善：

- クラス化  
- AND/OR 検索のバグ修正  
- 結果表示ウィンドウの改善  
- コードの可読性向上

## PDFSearch 特徴 / Features
- 複数キーワードによるAND検索機能
- 指定ディレクトリ内のPDFファイルを対象とした検索
- 検索結果のCSV出力機能
- 日本語キーワード検索に対応
- シンプルなGUIによる直感的な操作性

## PDFSearch 使い方 / Usage
1. `PDFSearch.py`をダウンロードし、実行したいディレクトリに配置します。
2. コマンドプロンプトまたはターミナルを開き、以下のコマンドを実行します：
```bash
python PDFSearch.py
```
4. GUIから検索したいディレクトリとキーワードを入力し、検索を開始します。

## PDFSearch 特記事項 / Notes
日本語環境の場合、`PdfReadWarning: Advanced encoding /UniJIS-UCS2-H not implemented yet`という警告メッセージが表示されることがあります。これは、使用しているPDF処理ライブラリが特定の日本語エンコーディングを完全にサポートしていないことを示しています。しかし、この警告はプログラムの実行を停止させるものではなく、検索は引き続き行われます。したがって、このメッセージが表示されても心配する必要はありません。検索が完了するまでしばらくお待ちください。

## PDFSearch  必要条件
- Python 3.x
- PyPDF2ライブラリ

# インストールガイド

SnapPDFとPDFSearchを使用する前に、以下の手順に従って必要なソフトウェアをインストールしてください。

## Pythonのインストール
SnapPDFとPDFSearchはPython 3.xを必要とします。まだインストールしていない場合は、以下の手順に従ってください。

1. Python公式ウェブサイトにアクセスします。
2. お使いのオペレーティングシステムに合わせたPython 3.xのインストーラーをダウンロードします。
3. ダウンロードしたインストーラーを実行し、画面の指示に従ってインストールを完了させます。
4. インストールが完了したら、コマンドプロンプトまたはターミナルを開き、`python --version`を実行して、Pythonが正しくインストールされていることを確認します。

## 📦 **依存関係（v2.0.0）**

SnapPDF v2.0.0 は以下の Python ライブラリを使用しています。

### **共通（SnapPDF / 2 / 4 / 6 / 15）**
- `datetime`：日付・時刻の取得  
- `os`：ファイルパス操作  
- `subprocess`：PDF の自動オープン  
- `tkinter`：GUI  
- `PIL (Pillow)`：画像処理・サムネイル生成  
- `reportlab`：PDF 生成  
- `concurrent.futures`：画像処理の並列化（v2.0.0 で重要）  
- `functools.lru_cache`：サムネイルキャッシュ（v2.0.0 新要素）

### **SnapPDF（Excel版のみ）**
- `pandas`：Excel 読み込み  
- `tkinterdnd2`：ドラッグ＆ドロップ対応  

### **PDFSearch**
- `PyPDF2`：PDF テキスト抽出  

---

## 📥 インストール

```bash
pip install Pillow
pip install reportlab
pip install tk
pip install pandas
pip install tkinterdnd2
pip install PyPDF2
```

---

## 著者

Copyright (c) 2023 NAGATA Mizuho, 永田 みず穂 - Institute of Laser Engineering, The University of Osaka


## ライセンス License
このプロジェクトはMITライセンスの下で公開されています。ライセンスの全文については、[LICENSE](https://github.com/Mizuho-NAGATA/SnapPDF/blob/main/LICENSE) をご覧ください。
This project is released under the MIT License. For the full text of the license, please see the LICENSE file.

## 謝辞 Acknowledgments

- このプログラムは、ChatGPT と Copilot の助力によって開発されました。また、ChatGPTを紹介してくれた私の家族に感謝します。
- 本開発は文部科学省先端研究基盤共用促進事業（先端研究設備プラットフォームプログラム） JPMXS0450300021である[パワーレーザーDXプラットフォーム](https://powerlaser.jp/)で共用された機器を利用した成果です。
- このプログラムは、第2回身近な研究DXコンテスト2023 の受賞作品です。
- This program was developed with the assistance of ChatGPT. I would like to express my gratitude to my family for introducing me to ChatGPT.
- This READEME file was created with the help of Copilot.
- This work was the result of using research equipment shared by the Power Laser DX Platform, which is MEXT Project for promoting public utilization of advanced research infrastructure（Program for advanced research equipment platforms）Grant Number JPMXS0450300021.
- This program is the winner of the 2nd Familiar Research DX Contest 2023.
