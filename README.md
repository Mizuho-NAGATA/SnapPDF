# SnapPDF

***DEMO:***  
![SnapPDF demo video](https://github.com/Mizuho-NAGATA/SnapPDF/blob/main/SnapPDF%20demo%20video.gif?raw=true)

「SnapPDF」は、複数の画像を一つのPDFファイルにまとめるシンプルで強力なツールです。  
同梱の「SnapSearch」によって、保存したPDF本文を検索することができます。   
"SnapPDF" is a simple and powerful tool that combines multiple images into a single PDF file. The program places a specific number of photos on an A4 horizontal page and instantly creates a PDF for presentation or archival purposes.  
 The included "SnapSearch" also allows you to search the saved PDF text.  
## 目次 / Table of Contents
1. [SnapPDF](#snappdf)
    1. [特徴 / Features](#特徴--features)
    2. [使い方 / Usage](#使い方--usage)
    3. [各バージョンの説明 / Versions](#各バージョンの説明--versions)
    4. [バージョンの選択 / Version Selection](#バージョンの選択--version-selection)
2. [SnapSearch](#snapsearch)
    1. [特徴 / Features](#snapsearch-特徴--features)
    2. [使い方 / Usage](#snapsearch-使い方--usage)
    3. [特記事項 / Notes](#snapsearch-特記事項--notes)
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
- 「SnapPDF」: 複数の画像に加え、エクセルファイルのデータも一つのPDFファイルに統合する
- インストール不要で、Pythonスクリプトを直接実行  
- Combine multiple images into one PDF file
- Images can be selected from multiple folders
- "SnapPDF2, 4, 6, 15": Place up to 2, 4, 6, 15 photos on one A4 page
- "SnapPDF": Combine multiple images as well as Excel data into one PDF file
- No installation required Direct execution of Python scripts
  
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
- `SnapPDF4.py`と`SnapPDF6.py`: 中間のサイズで写真を表示したい場合に適しています。
- `SnapPDF.py`と`SnapPDF15.py`: 一つのページに多くの写真を配置し、コンパクトなアルバムを作成したい場合に最適です。

# SnapSearch

SnapSearchは、PDFファイルの中身をキーワードで検索し、一致する内容を持つファイルを見つけ出す強力なツールです。指定されたディレクトリ内のPDFファイルを対象に、入力されたキーワードでAND検索を行い、検索結果をCSVファイルに出力します。日本語も検索できます。
SnapSearch is a powerful tool that searches the contents of PDF files by keywords to find files with matching contents. It performs AND searches on PDF files in a specified directory using entered keywords and outputs the search results to a CSV file. Japanese can also be searched.

## SnapSearch 特徴 / Features
- 複数キーワードによるAND検索機能
- 指定ディレクトリ内のPDFファイルを対象とした検索
- 検索結果のCSV出力機能
- 日本語キーワード検索に対応
- シンプルなGUIによる直感的な操作性

## SnapSearch 使い方 / Usage
1. `SnapSearch.py`をダウンロードし、実行したいディレクトリに配置します。
2. コマンドプロンプトまたはターミナルを開き、以下のコマンドを実行します：
```bash
python SnapSearch.py
```
4. GUIから検索したいディレクトリとキーワードを入力し、検索を開始します。

## SnapSearch 特記事項 / Notes
日本語環境の場合、`PdfReadWarning: Advanced encoding /UniJIS-UCS2-H not implemented yet`という警告メッセージが表示されることがあります。これは、使用しているPDF処理ライブラリが特定の日本語エンコーディングを完全にサポートしていないことを示しています。しかし、この警告はプログラムの実行を停止させるものではなく、検索は引き続き行われます。したがって、このメッセージが表示されても心配する必要はありません。検索が完了するまでしばらくお待ちください。

## SnapSearch  必要条件
- Python 3.x
- PyPDF2ライブラリ

# インストールガイド

SnapPDFとSnapSearchを使用する前に、以下の手順に従って必要なソフトウェアをインストールしてください。

## Pythonのインストール
SnapPDFとSnapSearchはPython 3.xを必要とします。まだインストールしていない場合は、以下の手順に従ってください。

1. Python公式ウェブサイトにアクセスします。
2. お使いのオペレーティングシステムに合わせたPython 3.xのインストーラーをダウンロードします。
3. ダウンロードしたインストーラーを実行し、画面の指示に従ってインストールを完了させます。
4. インストールが完了したら、コマンドプロンプトまたはターミナルを開き、`python --version`を実行して、Pythonが正しくインストールされていることを確認します。

# 依存関係

SnapPDFは、以下のPythonライブラリを使用しています。これらのライブラリは、画像処理、PDF生成、GUI操作など、SnapPDFの機能を実現するために必要です。

- `datetime`: 日付と時刻の操作に使用します。
- `PIL (Python Imaging Library)`: 画像の開閉、処理、保存に使用します。
- `reportlab`: PDF文書の生成に使用します。
- `tkinter`: Pythonの標準GUIツールキットで、ユーザーインターフェースを作成するために使用します。
- `os`: オペレーティングシステムとのやり取り、ファイルパスの操作に使用します。
- `subprocess`: 新しいプロセスを生成し、入出力ストリームを取得し、プロセスを管理するために使用します。
- `pandas`: データ分析と操作のためのライブラリです。
- `tkinterdnd2`: tkinterでドラッグ&ドロップ機能を実装するためのライブラリです。

これらのライブラリをインストールするには、以下のコマンドを実行してください。

```bash
pip install Pillow
pip install reportlab
pip install tk
pip install pandas
pip install tkinterdnd2
```

SnapSearchはPyPDF2ライブラリを使用します。以下のコマンドを実行してインストールしてください。

```bash
pip install PyPDF2
```
## 著者
Copyright (c) 2023 NAGATA Mizuho, 永田 みず穂 - Institute of Laser Engineering, Osaka University

## ライセンス License
このプロジェクトはMITライセンスの下で公開されています。ライセンスの全文については、[LICENSE](https://github.com/Mizuho-NAGATA/SnapPDF/blob/main/LICENSE) をご覧ください。
This project is released under the MIT License. For the full text of the license, please see the LICENSE file.

## 謝辞 Acknowledgments
- このプログラムは、ChatGPTの助力によって開発されました。また、ChatGPTを紹介してくれた私の家族に感謝します。
- このREADEMEファイルは、Copilotの協力によって作成されました。
- 本開発は文部科学省先端研究基盤共用促進事業（先端研究設備プラットフォームプログラム） JPMXS0450300021である[パワーレーザーDXプラットフォーム](https://powerlaser.jp/)で共用された機器を利用した成果です。
- このプログラムは、第2回身近な研究DXコンテスト2023 の受賞作品です。
- This program was developed with the assistance of ChatGPT. I would like to express my gratitude to my family for introducing me to ChatGPT.
- This READEME file was created with the help of Copilot.
- This work was the result of using research equipment shared by the [“Power Laser DX Platform”](https://powerlaser.jp/), which is MEXT Project for promoting public utilization of advanced research infrastructure（Program for advanced research equipment platforms）Grant Number JPMXS0450300021.
- This program is the winner of the 2nd Familiar Research DX Contest 2023.
