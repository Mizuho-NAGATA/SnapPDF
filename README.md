# SnapPDF
***DEMO:***
![demo](https://private-user-images.githubusercontent.com/139824384/338382248-dfad27ff-ebde-4a63-b8ac-7b1ef79e2423.gif?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTgwNjMwMzMsIm5iZiI6MTcxODA2MjczMywicGF0aCI6Ii8xMzk4MjQzODQvMzM4MzgyMjQ4LWRmYWQyN2ZmLWViZGUtNGE2My1iOGFjLTdiMWVmNzllMjQyMy5naWY_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwNjEwJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDYxMFQyMzM4NTNaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT02ZWY3MjJiZGQxN2JhMTgzMWJlOGUwMTk0YjM3MzdhNTgxZDFkZjZhZDllODQxNTVhOGYwODYxY2RiNjllNDEzJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.FpA4McH2ash2PxgtwQgKMscbnf_yAylQ4EoFCE36ifs)

SnapPDFは、複数の画像を一つのPDFファイルにまとめるシンプルで強力なツールです。このプログラムは、特定の枚数の写真をA4横のページに配置し、プレゼンテーションやアーカイブ用のPDFを瞬時に作成します。
SnapPDF is a simple and powerful tool that combines multiple images into a single PDF file. The program places a specific number of photos on an A4 horizontal page and instantly creates a PDF for presentation or archival purposes.

## 特徴
- 複数の画像を一つのPDFに統合
- A4横のページに2, 4, 6, 15枚の写真を配置
- インストール不要で、Pythonスクリプトを直接実行

## 使い方
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
- `SnapPDF2.py`: A4横1ページに2枚の写真をPDF出力します。
- `SnapPDF4.py`: A4横1ページに4枚の写真をPDF出力します。
- `SnapPDF6.py`: A4横1ページに6枚の写真をPDF出力します。
- `SnapPDF15.py`: A4横1ページに15枚の写真をPDF出力します。

## バージョンの選択
SnapPDFは、ユーザーのニーズに合わせて写真の表示サイズを調整できるように、異なるバージョンを提供しています。写真を大きく表示したい場合は、写真の枚数が少ないバージョンを選択してください。一方、小さいサイズで多くの写真を一つのページに表示させたい場合は、15枚の写真を配置するバージョンが最適です。

- `SnapPDF2.py`: 写真を大きく、詳細に表示したい場合に適しています。
- `SnapPDF4.py`と`SnapPDF6.py`: 中間のサイズで写真を表示したい場合に適しています。
- `SnapPDF15.py`: 一つのページに多くの写真を配置し、コンパクトなアルバムを作成したい場合に最適です。

この柔軟性により、プレゼンテーションやアーカイブ、イベントの記録など、さまざまな用途に合わせてPDFをカスタマイズすることができます。

# SnapSearch

SnapSearchは、PDFファイルの中身をキーワードで検索し、一致する内容を持つファイルを見つけ出す強力なツールです。指定されたディレクトリ内のPDFファイルを対象に、入力されたキーワードでAND検索を行い、検索結果をCSVファイルに出力します。

## 主な特徴
- 複数キーワードによるAND検索機能
- 指定ディレクトリ内のPDFファイルを対象とした検索
- 検索結果のCSV出力機能
- 日本語キーワード検索に対応
- シンプルなGUIによる直感的な操作性

## 使い方
1. `SnapSearch.py`をダウンロードし、実行したいディレクトリに配置します。
2. コマンドプロンプトまたはターミナルを開き、以下のコマンドを実行します：
```bash
python SnapSearch.py
```
4. GUIから検索したいディレクトリとキーワードを入力し、検索を開始します。

## 必要条件
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

これらのライブラリをインストールするには、以下のコマンドを実行してください。

```bash
pip install Pillow
pip install reportlab
pip install tk
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
- 本開発は文部科学省先端研究基盤共用促進事業（先端研究設備プラットフォームプログラム） JPMXS0450300021である「パワーレーザーDXプラットフォーム」で共用された機器を利用した成果です。
- このプログラムは、第2回身近な研究DXコンテスト2023 の受賞作品です。
- This program was developed with the assistance of ChatGPT. I would like to express my gratitude to my family for introducing me to ChatGPT.
- This READEME file was created with the help of Copilot.
- This work was the result of using research equipment shared by the “Power Laser DX Platform,” which is MEXT Project for promoting public utilization of advanced research infrastructure（Program for advanced research equipment platforms）Grant Number JPMXS0450300021.
- This program is the winner of the 2nd Familiar Research DX Contest 2023.
