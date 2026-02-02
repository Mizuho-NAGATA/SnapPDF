# SnapPDF v2.0 起動方法ガイド / How to Run SnapPDF v2.0

## 🚀 クイックスタート / Quick Start

### Windows ユーザー（最も簡単！）/ Windows Users (Easiest!)

#### SnapPDF の起動
1. エクスプローラーで `run_snappdf.bat` をダブルクリック
2. アプリケーションが起動します

#### SnapSearch の起動
1. エクスプローラーで `run_snapsearch.bat` をダブルクリック
2. 検索ツールが起動します

---

### macOS / Linux ユーザー / macOS / Linux Users

#### SnapPDF の起動
ターミナルを開き、以下のコマンドを実行：
```bash
cd /path/to/SnapPDF-v2.0.0
python3 snappdf_unified.py
```

#### SnapSearch の起動
ターミナルを開き、以下のコマンドを実行：
```bash
cd /path/to/SnapPDF-v2.0.0
python3 SnapSearch.py
```

---

## 📋 全起動方法一覧 / All Launch Methods

### SnapPDF メインアプリケーション

| OS | 方法 | コマンド/操作 |
|---|---|---|
| **Windows** | バッチファイル（推奨） | `run_snappdf.bat` をダブルクリック |
| **Windows** | コマンドプロンプト | `run_snappdf.bat` |
| **Windows** | Pythonコマンド | `python snappdf_unified.py` |
| **macOS** | ターミナル | `python3 snappdf_unified.py` |
| **Linux** | ターミナル | `python3 snappdf_unified.py` |

### SnapSearch (PDF検索ツール)

| OS | 方法 | コマンド/操作 |
|---|---|---|
| **Windows** | バッチファイル（推奨） | `run_snapsearch.bat` をダブルクリック |
| **Windows** | コマンドプロンプト | `run_snapsearch.bat` |
| **Windows** | Pythonコマンド | `python SnapSearch.py` |
| **macOS** | ターミナル | `python3 SnapSearch.py` |
| **Linux** | ターミナル | `python3 SnapSearch.py` |

---

## 🔧 トラブルシューティング / Troubleshooting

### Windows で "python: command not found" エラーが出る

**解決方法1: バッチファイルを使う**
- `run_snappdf.bat` をダブルクリックしてください
- バッチファイルが自動的にPythonを見つけます

**解決方法2: Pythonを再インストール**
1. [Python公式サイト](https://www.python.org/downloads/)からダウンロード
2. インストール時に「Add Python to PATH」にチェックを入れる

### macOS / Linux で "python: command not found" エラーが出る

**解決方法:**
`python` の代わりに `python3` を使用してください
```bash
python3 snappdf_unified.py
```

### バッチファイルをダブルクリックしても何も起きない（Windows）

**原因:** `.bat` ファイルの関連付けが正しくない可能性があります

**解決方法:**
1. `run_snappdf.bat` を右クリック
2. 「プログラムから開く」→「別のプログラムを選択」
3. 「常にこのアプリを使って.batファイルを開く」にチェック
4. 「コマンドプロンプト」を選択

または、コマンドプロンプトから直接実行：
```cmd
cd C:\path\to\SnapPDF-v2.0.0
run_snappdf.bat
```

### 依存パッケージがインストールされていない

**症状:**
```
ModuleNotFoundError: No module named 'PIL'
ModuleNotFoundError: No module named 'reportlab'
```

**解決方法:**
```bash
pip install -r requirements.txt
```

詳細は `INSTALLATION.md` を参照してください。

---

## 💡 便利な使い方 / Tips

### Windows: デスクトップにショートカットを作成

1. `run_snappdf.bat` を右クリック
2. 「ショートカットの作成」を選択
3. 作成されたショートカットをデスクトップに移動
4. 今後はデスクトップからワンクリックで起動できます！

### macOS / Linux: エイリアスを作成（上級者向け）

`.bashrc` または `.zshrc` に以下を追加：

```bash
alias snappdf='cd /path/to/SnapPDF-v2.0.0 && python3 snappdf_unified.py'
alias snapsearch='cd /path/to/SnapPDF-v2.0.0 && python3 SnapSearch.py'
```

ターミナルで `snappdf` と入力するだけで起動できるようになります。

---

## 📚 関連ドキュメント / Related Documentation

- **完全インストールガイド**: `INSTALLATION.md`
- **クイックスタートガイド**: `QUICKSTART_JP.md`
- **完全マニュアル**: `README.md`
- **旧バージョンからの移行**: `MIGRATION_GUIDE.md`

---

## 🎯 起動確認チェックリスト / Launch Checklist

起動前に確認すること：

- [ ] Python 3.7以上がインストールされている
- [ ] 依存パッケージがインストールされている（`pip install -r requirements.txt`）
- [ ] プロジェクトディレクトリに移動している（または正しいパスを指定）

起動できたら：

- [ ] GUIウィンドウが表示される
- [ ] エラーメッセージが表示されない（警告は無視してOK）
- [ ] 「Select Images」ボタンなどが操作可能

---

## ❓ よくある質問 / FAQ

**Q: 毎回コマンドを入力するのが面倒です**

A: Windowsユーザーは `run_snappdf.bat` をダブルクリックするだけで起動できます。デスクトップにショートカットを作成すればさらに便利です。

**Q: バッチファイルとPythonコマンド、どちらが良いですか？**

A: どちらでも同じ結果が得られますが、Windowsユーザーにはバッチファイル（.bat）の方が簡単でおすすめです。

**Q: macOSでバッチファイルは使えますか？**

A: いいえ、バッチファイル（.bat）はWindows専用です。macOS/Linuxでは `python3 snappdf_unified.py` を使用してください。

**Q: 起動するとフォント警告が表示されます**

A: 警告は無視できます。アプリケーションは正常に動作します。日本語フォントが見つからない場合、自動的に代替フォントが使用されます。

**Q: 複数のPythonバージョンがインストールされています**

A: `python3 snappdf_unified.py` を使用することで、Python 3.xを確実に使用できます。

---

## 🆘 それでも起動できない場合 / Still Having Issues?

1. **インストールテストを実行**
   ```bash
   python test_installation.py
   ```
   
2. **エラーメッセージを確認**
   - 赤い✗マークの項目を確認
   - 不足している依存パッケージをインストール

3. **完全なインストールガイドを参照**
   - `INSTALLATION.md` を読んで手順を確認

4. **GitHubでサポートを依頼**
   - エラーメッセージをコピー
   - 使用しているOS、Pythonバージョンを記載
   - [GitHub Issues](https://github.com/Mizuho-NAGATA/SnapPDF/issues) で質問

---

**それでは、SnapPDFをお楽しみください！📸→📄**

---

*Last Updated: 2026-02-02*  
*Version: 2.0.0*