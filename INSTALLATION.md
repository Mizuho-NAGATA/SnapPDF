# SnapPDF v2.0.0 インストールガイド / Installation Guide

## 📋 システム要件 / System Requirements

### 必須要件 / Required
- **Python**: 3.7 以上 / 3.7 or higher
- **OS**: Windows 10/11, macOS 10.14+, Linux (Ubuntu, Debian, Fedora等)
- **メモリ / RAM**: 最小 2GB / Minimum 2GB
- **ディスク容量 / Disk Space**: 100MB以上の空き容量 / 100MB+ free space

### 推奨環境 / Recommended
- **Python**: 3.9 以上 / 3.9 or higher
- **メモリ / RAM**: 4GB以上 / 4GB or more
- **画面解像度 / Screen Resolution**: 1280x720 以上 / 1280x720 or higher

---

## 🚀 クイックインストール / Quick Installation

### ステップ1: Pythonの確認 / Step 1: Verify Python

```bash
python --version
```

Python 3.7以上がインストールされていることを確認してください。  
Verify that Python 3.7 or higher is installed.

### ステップ2: 依存パッケージのインストール / Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### ステップ3: インストール確認 / Step 3: Verify Installation

```bash
python test_installation.py
```

すべてのテストが✓でパスすれば成功です！  
If all tests pass with ✓, you're ready to go!

### ステップ4: アプリケーションの起動 / Step 4: Run Application

```bash
python snappdf_unified.py
```

---

## 📦 詳細インストール手順 / Detailed Installation

### Windows

#### 1. Pythonのインストール / Python Installation

1. [Python公式サイト](https://www.python.org/downloads/)にアクセス
2. 最新のPython 3.x（3.9以上推奨）をダウンロード
3. インストーラーを実行
4. **重要**: "Add Python to PATH"にチェックを入れる
5. "Install Now"をクリック

#### 2. コマンドプロンプトを開く / Open Command Prompt

- `Win + R` → `cmd` と入力 → Enter

#### 3. プロジェクトディレクトリに移動 / Navigate to Project Directory

```cmd
cd C:\path\to\SnapPDF-v2.0.0
```

#### 4. 依存パッケージをインストール / Install Dependencies

```cmd
pip install -r requirements.txt
```

#### 5. インストール確認 / Verify Installation

```cmd
python test_installation.py
```

#### 6. 起動 / Launch

```cmd
python snappdf_unified.py
```

---

### macOS

#### 1. Pythonのインストール / Python Installation

**オプション A: 公式インストーラー（推奨）**
1. [Python公式サイト](https://www.python.org/downloads/)にアクセス
2. macOS用のインストーラーをダウンロード
3. インストーラーを実行

**オプション B: Homebrew**
```bash
brew install python3
```

#### 2. ターミナルを開く / Open Terminal

- `Cmd + Space` → "Terminal"と入力 → Enter

#### 3. プロジェクトディレクトリに移動 / Navigate to Project Directory

```bash
cd /path/to/SnapPDF-v2.0.0
```

#### 4. 依存パッケージをインストール / Install Dependencies

```bash
pip3 install -r requirements.txt
```

#### 5. インストール確認 / Verify Installation

```bash
python3 test_installation.py
```

#### 6. 起動 / Launch

```bash
python3 snappdf_unified.py
```

---

### Linux (Ubuntu/Debian)

#### 1. Pythonのインストール / Python Installation

```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk
```

#### 2. プロジェクトディレクトリに移動 / Navigate to Project Directory

```bash
cd /path/to/SnapPDF-v2.0.0
```

#### 3. 依存パッケージをインストール / Install Dependencies

```bash
pip3 install -r requirements.txt
```

#### 4. インストール確認 / Verify Installation

```bash
python3 test_installation.py
```

#### 5. 起動 / Launch

```bash
python3 snappdf_unified.py
```

---

## 🔧 依存パッケージの詳細 / Dependencies Details

### 必須パッケージ / Required Packages

```
Pillow>=9.0.0         # 画像処理 / Image processing
reportlab>=3.6.0      # PDF生成 / PDF generation
pandas>=1.3.0         # Excel読み込み / Excel reading
PyPDF2>=3.0.0         # PDF検索 / PDF search (for SnapSearch)
```

### オプションパッケージ / Optional Packages

```
tkinterdnd2>=0.3.0    # ドラッグ&ドロップ機能 / Drag and drop support
```

**注意**: tkinterはPython標準ライブラリに含まれています。  
**Note**: tkinter is included in Python standard library.

---

## 🐛 トラブルシューティング / Troubleshooting

### 問題1: "python: command not found" / "python: command not found"

**原因 / Cause**: PythonがPATHに追加されていない  
Python is not added to PATH

**解決方法 / Solution**:
- Windows: Pythonを再インストールし、"Add Python to PATH"にチェック
- macOS/Linux: `python3`コマンドを使用

### 問題2: "pip: command not found" / "pip: command not found"

**解決方法 / Solution**:
```bash
python -m pip install -r requirements.txt
```

または / or

```bash
python3 -m pip install -r requirements.txt
```

### 問題3: "ModuleNotFoundError: No module named 'tkinter'"

**Windows**: Pythonインストーラーで"tcl/tk and IDLE"を選択して再インストール  
Reinstall Python with "tcl/tk and IDLE" option selected

**macOS**: Python.orgからインストールしたPythonを使用  
Use Python installed from Python.org

**Linux (Ubuntu/Debian)**:
```bash
sudo apt-get install python3-tk
```

**Linux (Fedora)**:
```bash
sudo dnf install python3-tkinter
```

### 問題4: "Permission denied" エラー

**解決方法 / Solution**:
```bash
pip install --user -r requirements.txt
```

### 問題5: フォント警告 "Could not load font BIZ-UDGothicR.ttc"

**影響 / Impact**: 日本語フォントの代わりにHelveticaが使用されます  
Helvetica will be used instead of Japanese font

**解決方法 / Solution**: 
- この警告は無視できます。アプリケーションは正常に動作します
- This warning can be ignored. The application will work normally
- 日本語フォントを使用したい場合、システムにフォントをインストールしてください
- To use Japanese fonts, install the font file on your system

### 問題6: "ImportError: cannot import name 'TkinterDnD'"

**影響 / Impact**: ドラッグ&ドロップ機能が無効になりますが、他の機能は動作します  
Drag-and-drop will be disabled, but other features will work

**解決方法 / Solution**:
```bash
pip install tkinterdnd2
```

---

## 🧪 インストールの検証 / Verify Installation

インストールが正しく完了したか確認するには:  
To verify that installation completed successfully:

```bash
python test_installation.py
```

### 期待される出力 / Expected Output

```
======================================================================
SnapPDF v2.0 Installation Test
======================================================================

Test 1: Python Version
----------------------------------------------------------------------
✓ Python version is compatible (>= 3.7)

Test 2: Required Dependencies
----------------------------------------------------------------------
✓ Pillow: version X.X.X
✓ reportlab: version X.X.X
✓ pandas: version X.X.X
✓ tkinter (standard library): available

Test 3: Optional Dependencies
----------------------------------------------------------------------
✓ tkinterdnd2 (for drag-and-drop): available
✓ PyPDF2 (for SnapSearch): version X.X.X

...

======================================================================
Installation Test Summary
======================================================================
✓ All tests passed!
```

---

## 📚 次のステップ / Next Steps

インストールが完了したら:  
After installation is complete:

1. **クイックスタートガイドを読む**  
   Read the Quick Start Guide
   ```
   QUICKSTART_JP.md
   ```

2. **アプリケーションを起動**  
   Launch the application
   ```bash
   python snappdf_unified.py
   ```

3. **完全なドキュメントを参照**  
   Refer to complete documentation
   ```
   README.md
   ```

4. **旧バージョンからの移行**  
   Migrating from old version
   ```
   MIGRATION_GUIDE.md
   ```

---

## 🔄 アップデート / Updates

### 最新バージョンの確認 / Check Latest Version

GitHubリポジトリで最新バージョンを確認:  
Check the GitHub repository for the latest version:

[https://github.com/Mizuho-NAGATA/SnapPDF](https://github.com/Mizuho-NAGATA/SnapPDF)

### アップデート方法 / How to Update

1. 新しいバージョンをダウンロード
2. 既存のディレクトリをバックアップ
3. 新しいファイルで置き換え
4. 依存パッケージを更新:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

---

## 🆘 サポート / Support

### 問題が解決しない場合 / If Issues Persist

1. **test_installation.pyを実行して詳細を確認**  
   Run test_installation.py for details
   
2. **エラーメッセージをコピー**  
   Copy the error message

3. **GitHubでIssueを作成**  
   Create an issue on GitHub
   
   必要な情報 / Required information:
   - OS とバージョン / OS and version
   - Pythonバージョン / Python version
   - エラーメッセージ / Error message
   - test_installation.pyの出力 / Output of test_installation.py

---

## 📞 お問い合わせ / Contact

- **GitHub Issues**: [https://github.com/Mizuho-NAGATA/SnapPDF/issues](https://github.com/Mizuho-NAGATA/SnapPDF/issues)
- **Email**: (GitHubプロフィールを参照 / See GitHub profile)

---

## ✅ インストールチェックリスト / Installation Checklist

- [ ] Python 3.7以上がインストールされている
- [ ] pipが使用可能
- [ ] requirements.txtから依存パッケージをインストール
- [ ] test_installation.pyが全てパス
- [ ] snappdf_unified.pyが起動できる
- [ ] ドキュメントを確認した

---

**SnapPDF v2.0.0をお選びいただきありがとうございます！**  
**Thank you for choosing SnapPDF v2.0.0!**

**インストールが完了したら、`QUICKSTART_JP.md`で使い方をご確認ください。**  
**Once installation is complete, check `QUICKSTART_JP.md` for usage instructions.**

---

*Version: 2.0.0*  
*Last Updated: 2026-02-02*  
*Copyright (c) 2023-2026 NAGATA Mizuho*