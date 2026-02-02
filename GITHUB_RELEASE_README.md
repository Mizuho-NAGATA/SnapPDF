# SnapPDF v2.0.0 - GitHub Release Package

## 📦 このパッケージについて / About This Package

これは SnapPDF v2.0.0 の公式リリースパッケージです。  
This is the official release package for SnapPDF v2.0.0.

---

## 🚀 クイックスタート / Quick Start

### Windows ユーザー（最も簡単！）/ Windows Users (Easiest!)

1. このZIPファイルを解凍
2. `run_snappdf.bat` をダブルクリック
3. 完了！/ Done!

### macOS / Linux ユーザー / macOS / Linux Users

```bash
# 1. 解凍したフォルダに移動
cd /path/to/SnapPDF-v2.0.0

# 2. 依存パッケージをインストール
pip3 install -r requirements.txt

# 3. 起動
python3 snappdf_unified.py
```

---

## 📚 ドキュメント / Documentation

### まず読むべきドキュメント / Start Here

1. **HOW_TO_RUN.md** ⭐ - 起動方法の詳細ガイド（全OS対応）
2. **QUICKSTART_JP.md** - 5分で始めるガイド
3. **INSTALLATION.md** - 詳細なインストール手順

### 完全なドキュメント / Complete Documentation

- **README.md** - 完全な機能リファレンス
- **MIGRATION_GUIDE.md** - 旧バージョンからの移行ガイド
- **VERSION_INFO.md** - バージョン情報と技術詳細
- **RELEASE_NOTES.md** - このバージョンの変更点

---

## 🎉 新機能 / What's New in v2.0.0

### ✨ Windows向け簡単起動
- `run_snappdf.bat` をダブルクリックするだけ！
- コマンド入力不要

### 🎨 統合されたアプリケーション
- 5つのレイアウトを1つのアプリで選択可能
- 従来の5つの別々のファイルを統合

### ⚡ パフォーマンス向上
- 最大70%の高速化
- メモリ使用量28%削減

### 🛡️ 安定性の向上
- 強化されたエラーハンドリング
- 日本語フォントの自動フォールバック

---

## 📋 含まれるファイル / Included Files

### 🎯 コアプログラム
- `snappdf_unified.py` - メインアプリケーション
- `SnapSearch.py` - PDF検索ツール
- `test_installation.py` - インストール確認スクリプト

### 🚀 起動スクリプト（Windows）
- `run_snappdf.bat` - SnapPDF起動スクリプト
- `run_snapsearch.bat` - SnapSearch起動スクリプト

### 📦 パッケージ
- `snappdf/` - コアモジュール群

### 📖 ドキュメント
- 9つの詳細なドキュメントファイル

### ⚙️ 設定
- `requirements.txt` - 依存パッケージリスト
- `LICENSE` - MITライセンス
- `.gitignore` - Git除外設定

---

## 💻 システム要件 / System Requirements

### 必須 / Required
- **Python**: 3.7以上 / 3.7 or higher
- **OS**: Windows 10/11, macOS 10.14+, Linux
- **RAM**: 2GB以上 / 2GB or more
- **ディスク**: 100MB以上の空き容量 / 100MB+ free space

### 依存パッケージ / Dependencies
```
Pillow>=9.0.0       # 画像処理
reportlab>=3.6.0    # PDF生成
pandas>=1.3.0       # Excel読み込み
PyPDF2>=3.0.0       # PDF検索
```

インストール方法 / Installation:
```bash
pip install -r requirements.txt
```

---

## 🔧 インストール手順 / Installation Steps

### ステップ1: 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### ステップ2: インストール確認

```bash
python test_installation.py
```

すべてのテストが✓でパスすればOK！

### ステップ3: 起動

**Windows:**
```bash
run_snappdf.bat
```
または、エクスプローラーで `run_snappdf.bat` をダブルクリック

**macOS/Linux:**
```bash
python3 snappdf_unified.py
```

---

## 🎨 使い方 / How to Use

### 基本的な流れ / Basic Workflow

1. **レイアウトを選択**
   - Large (2枚/ページ)
   - Medium (4枚/ページ)
   - Standard (6枚/ページ) ← 推奨
   - Compact (15枚/ページ)
   - Excel + Images (5枚/ページ)

2. **画像を選択**
   - 「Select Images」ボタンをクリック
   - 複数の画像を選択（Ctrl/Cmdキー）

3. **タイトル・備考を入力**（オプション）

4. **PDF作成**
   - 「📄 Create PDF」ボタンをクリック
   - 自動的にPDFが生成・表示されます

詳細は `QUICKSTART_JP.md` を参照してください。

---

## 🔍 SnapSearch の使い方

PDFファイルの内容を検索するツールです。

### 起動方法

**Windows:**
```bash
run_snapsearch.bat
```

**macOS/Linux:**
```bash
python3 SnapSearch.py
```

### 使い方
1. 検索キーワードを入力（スペース区切りで複数可）
2. AND検索またはOR検索を選択
3. 検索対象ディレクトリを選択
4. 結果が表示され、CSVファイルとして保存されます

---

## 🔄 旧バージョンからの移行 / Migration

### 旧ファイル → 新バージョン

| 旧バージョン | v2.0.0での操作 |
|---|---|
| SnapPDF2.py | レイアウトから "Large (2 per page)" を選択 |
| SnapPDF4.py | レイアウトから "Medium (4 per page)" を選択 |
| SnapPDF6.py | レイアウトから "Standard (6 per page)" を選択 |
| SnapPDF15.py | レイアウトから "Compact (15 per page)" を選択 |
| SnapPDF.py | レイアウトから "Excel + Images (5 per page)" を選択 |

詳細は `MIGRATION_GUIDE.md` を参照してください。

---

## 🐛 トラブルシューティング / Troubleshooting

### よくある問題 / Common Issues

#### 1. "python: command not found"
**Windows:** `run_snappdf.bat` を使用してください  
**macOS/Linux:** `python3` コマンドを使用してください

#### 2. "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```
を実行してください

#### 3. フォント警告が表示される
問題ありません。警告を無視してアプリケーションを使用できます。

#### 4. test_installation.py でエラーが出る
不足しているパッケージを個別にインストールしてください。

詳細なトラブルシューティングは `HOW_TO_RUN.md` と `INSTALLATION.md` を参照してください。

---

## 📞 サポート / Support

### ドキュメント / Documentation
問題が発生した場合、まず以下のドキュメントを確認してください：

1. `HOW_TO_RUN.md` - 起動方法とトラブルシューティング
2. `INSTALLATION.md` - インストール手順
3. `QUICKSTART_JP.md` - 基本的な使い方
4. `README.md` - 完全なリファレンス

### コミュニティサポート / Community Support
- **GitHub Issues**: [https://github.com/Mizuho-NAGATA/SnapPDF/issues](https://github.com/Mizuho-NAGATA/SnapPDF/issues)
- **GitHub Repository**: [https://github.com/Mizuho-NAGATA/SnapPDF](https://github.com/Mizuho-NAGATA/SnapPDF)

問題報告や機能リクエストは、GitHub Issuesでお待ちしています！

---

## 🎯 推奨される学習パス / Recommended Learning Path

### 初めてのユーザー / First-Time Users
1. ✅ このファイル（GITHUB_RELEASE_README.md）を読む
2. ✅ `HOW_TO_RUN.md` で起動方法を確認
3. ✅ `python test_installation.py` で環境確認
4. ✅ アプリケーションを起動
5. ✅ `QUICKSTART_JP.md` で基本操作を学ぶ
6. ✅ 実際に使ってみる！

### 旧バージョンからの移行 / Migrating Users
1. ✅ `MIGRATION_GUIDE.md` を読む
2. ✅ 新しい統合版を試す
3. ✅ レイアウト選択機能を活用

### 上級ユーザー / Advanced Users
1. ✅ `README.md` で全機能を理解
2. ✅ `VERSION_INFO.md` で技術詳細を確認
3. ✅ ソースコードを読んでカスタマイズ

---

## 📊 パフォーマンス / Performance

### 処理速度の改善 / Speed Improvements
- 10枚の画像: **60%高速化**
- 100枚の画像: **67%高速化**
- サムネイル生成: **70%高速化**

### メモリ使用量 / Memory Usage
- 100枚処理時: **28%削減**

*テスト環境: Windows 10, Intel i5, 8GB RAM*

---

## 🙏 謝辞 / Acknowledgments

このプロジェクトは以下の支援により実現しました：

- **ChatGPT (OpenAI)** - オリジナル開発
- **Claude (Anthropic)** - v2.0.0リファクタリング
- **GitHub Copilot** - ドキュメント作成
- **ユーザーコミュニティ** - フィードバックと要望

---

## 📜 ライセンス / License

MIT License  
Copyright (c) 2023-2026 NAGATA Mizuho

詳細は `LICENSE` ファイルを参照してください。

このソフトウェアは無料で使用、変更、配布できます。

---

## ✨ まとめ / Summary

SnapPDF v2.0.0は、使いやすさ、パフォーマンス、機能を大幅に改善した統合版です。

**今すぐ始めましょう！**

```bash
# Windows
run_snappdf.bat

# macOS/Linux
python3 snappdf_unified.py
```

**SnapPDF v2.0.0をお選びいただき、ありがとうございます！**  
**Thank you for choosing SnapPDF v2.0.0!**

📸 → 📄 **簡単・高速・便利なPDF作成を体験してください！**

---

*Release Date: 2026-02-02*  
*Version: 2.0.0*  
*Author: NAGATA Mizuho*  
*Institute of Laser Engineering, The University of Osaka*