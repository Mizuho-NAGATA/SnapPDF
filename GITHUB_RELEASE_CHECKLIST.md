# GitHub リリース準備チェックリスト / GitHub Release Checklist

## 📋 SnapPDF v2.0.0 リリース前チェックリスト

このチェックリストに従って、GitHubリリースの準備を進めてください。

---

## ✅ ステップ1: ファイルの確認 / Step 1: Verify Files

### 必須ファイルが揃っているか確認 / Check Required Files

- [ ] `snappdf_unified.py` - メインアプリケーション
- [ ] `SnapSearch.py` - PDF検索ツール
- [ ] `test_installation.py` - インストール検証スクリプト
- [ ] `run_snappdf.bat` - Windows起動スクリプト
- [ ] `run_snapsearch.bat` - SnapSearch起動スクリプト
- [ ] `requirements.txt` - 依存パッケージリスト
- [ ] `LICENSE` - ライセンスファイル

### snappdfパッケージ / snappdf Package

- [ ] `snappdf/__init__.py`
- [ ] `snappdf/config.py`
- [ ] `snappdf/core.py`
- [ ] `snappdf/ui.py`
- [ ] `snappdf/utils.py`

### ドキュメント / Documentation

- [ ] `README.md` - メインドキュメント
- [ ] `HOW_TO_RUN.md` - 起動方法ガイド
- [ ] `QUICKSTART_JP.md` - クイックスタートガイド
- [ ] `INSTALLATION.md` - インストールガイド
- [ ] `MIGRATION_GUIDE.md` - 移行ガイド
- [ ] `VERSION_INFO.md` - バージョン情報
- [ ] `REFACTORING_SUMMARY.md` - リファクタリング記録
- [ ] `RELEASE_NOTES.md` - リリースノート
- [ ] `.gitignore` - Git除外設定
- [ ] `GITHUB_RELEASE_CHECKLIST.md` - このファイル

---

## ✅ ステップ2: 不要なファイルの削除 / Step 2: Remove Unnecessary Files

### 削除すべきファイル / Files to Remove

- [ ] `snappdf/__pycache__/` - Pythonキャッシュディレクトリ ✓ (削除済み)
- [ ] `*.pyc` - コンパイル済みPythonファイル
- [ ] `*.pyo` - 最適化されたPythonファイル
- [ ] `.DS_Store` - macOSシステムファイル
- [ ] `Thumbs.db` - Windowsサムネイルキャッシュ
- [ ] `*.tmp` - 一時ファイル
- [ ] `*.log` - ログファイル
- [ ] テスト用に生成したPDFファイル

### 確認コマンド（Windows） / Verification Command (Windows)

```cmd
dir /s /b *.pyc
dir /s /b __pycache__
dir /s /b *.log
```

---

## ✅ ステップ3: 動作確認 / Step 3: Functional Testing

### インストールテスト / Installation Test

- [ ] `python test_installation.py` を実行
- [ ] すべてのテストが✓でパス
- [ ] エラーメッセージがないことを確認

### 起動テスト / Launch Test

**Windows:**
- [ ] `run_snappdf.bat` をダブルクリックして起動
- [ ] GUIが正常に表示される
- [ ] `run_snapsearch.bat` をダブルクリックして起動
- [ ] SnapSearchが正常に表示される

**Python コマンド:**
- [ ] `python snappdf_unified.py` で起動
- [ ] `python SnapSearch.py` で起動

### 機能テスト / Feature Test

- [ ] 各レイアウトオプションが選択可能
- [ ] 画像選択ボタンが動作
- [ ] 画像の並び替え（↑/↓）が動作
- [ ] PDF生成が成功
- [ ] 生成されたPDFが正常に開ける

---

## ✅ ステップ4: ドキュメントの最終確認 / Step 4: Documentation Review

### バージョン情報の確認 / Version Information

- [ ] すべてのドキュメントでバージョンが `2.0.0` になっている
- [ ] リリース日が正しい（2026-02-02）
- [ ] リンクが正しく機能する

### ドキュメントの整合性 / Documentation Consistency

- [ ] README.mdの目次が正しい
- [ ] HOW_TO_RUN.mdの起動方法が最新
- [ ] INSTALLATION.mdの手順が正確
- [ ] RELEASE_NOTES.mdの内容が完全

---

## ✅ ステップ5: 圧縮ファイルの作成 / Step 5: Create Archive

### 圧縮方法 / Compression Method

**方法1: Windowsエクスプローラー（推奨）**

1. `SnapPDF-v2.0.0` フォルダを右クリック
2. 「送る」→「圧縮 (zip形式) フォルダー」を選択
3. ファイル名を `SnapPDF-v2.0.0.zip` に変更

**方法2: コマンドライン**

```cmd
cd C:\Users\000332\Desktop
powershell Compress-Archive -Path "SnapPDF-v2.0.0" -DestinationPath "SnapPDF-v2.0.0.zip"
```

### 圧縮ファイルの確認 / Verify Archive

- [ ] ZIPファイルのサイズが適切（目安: 50-200KB）
- [ ] ZIPファイルを解凍して内容を確認
- [ ] 解凍後、`run_snappdf.bat` が動作することを確認

---

## ✅ ステップ6: GitHubリリースの作成 / Step 6: Create GitHub Release

### 事前準備 / Preparation

- [ ] GitHubアカウントにログイン
- [ ] SnapPDFリポジトリにアクセス
- [ ] 最新のコミットがプッシュされている

### リリース作成手順 / Release Creation Steps

1. **リリースページに移動**
   - リポジトリページで「Releases」をクリック
   - 「Create a new release」または「Draft a new release」をクリック

2. **タグを作成**
   - Tag version: `v2.0.0`
   - Target: `main` ブランチ（または適切なブランチ）

3. **リリース情報を入力**
   - Release title: `SnapPDF v2.0.0 - Unified Application with Easy Launch`
   - Description: `RELEASE_NOTES.md` の内容をコピー

4. **ファイルをアップロード**
   - `SnapPDF-v2.0.0.zip` をドラッグ&ドロップ

5. **リリースを公開**
   - 「Publish release」をクリック

---

## ✅ ステップ7: リリース後の確認 / Step 7: Post-Release Verification

### ダウンロードテスト / Download Test

- [ ] GitHubからZIPファイルをダウンロード
- [ ] 新しいフォルダに解凍
- [ ] `test_installation.py` を実行
- [ ] `run_snappdf.bat` で起動確認

### リンクの確認 / Verify Links

- [ ] リリースページのURLをコピー
- [ ] README.mdからリンクが機能するか確認
- [ ] ダウンロードカウンターが動作しているか確認

---

## 📝 GitHubリリース説明文テンプレート / GitHub Release Description Template

以下のテンプレートを使用してください（RELEASE_NOTES.mdの内容をベースに）:

```markdown
# SnapPDF v2.0.0 - Unified Application with Easy Launch 🚀

## 🎉 主な新機能 / What's New

### Windows ユーザー向けの簡単起動！
- ✨ `run_snappdf.bat` をダブルクリックするだけ！
- ✨ コマンド入力不要で初心者にも優しい

### 統合された体験
- 🎨 5つのレイアウトを1つのアプリで選択可能
- ⚡ 最大70%の高速化
- 🛡️ 強化されたエラーハンドリング

## 📦 ダウンロードとインストール

1. 下の `SnapPDF-v2.0.0.zip` をダウンロード
2. 任意の場所に解凍
3. `pip install -r requirements.txt` で依存パッケージをインストール
4. **Windows**: `run_snappdf.bat` をダブルクリック
5. **macOS/Linux**: `python3 snappdf_unified.py` を実行

## 📚 ドキュメント

- **HOW_TO_RUN.md** - 起動方法ガイド（推奨）
- **QUICKSTART_JP.md** - 5分で始めるガイド
- **INSTALLATION.md** - 詳細なインストール手順
- **README.md** - 完全なドキュメント

## 🔄 旧バージョンからの移行

詳細は同梱の `MIGRATION_GUIDE.md` を参照してください。

## システム要件

- Python 3.7以上
- Windows 10/11, macOS 10.14+, Linux
- RAM: 2GB以上

完全なリリースノートは `RELEASE_NOTES.md` をご覧ください。
```

---

## 📊 リリース情報サマリー / Release Information Summary

**バージョン**: v2.0.0  
**リリース日**: 2026-02-02  
**タグ名**: `v2.0.0`  
**ZIPファイル名**: `SnapPDF-v2.0.0.zip`  
**ライセンス**: MIT License  

---

## ✨ 最終チェック / Final Check

リリース前に必ず確認：

- [ ] すべての必須ファイルが含まれている
- [ ] 不要なファイル（__pycache__等）が削除されている
- [ ] test_installation.py がすべてパスする
- [ ] run_snappdf.bat で正常に起動する
- [ ] ドキュメントのリンクが機能する
- [ ] バージョン番号が統一されている
- [ ] ZIPファイルが作成されている
- [ ] ZIPファイルの動作確認ができている

---

## 🎯 リリース後のタスク / Post-Release Tasks

- [ ] GitHubリリースページでダウンロード数を確認
- [ ] README.mdの「ダウンロード」リンクを更新（必要な場合）
- [ ] SNSや関連コミュニティでリリースを告知
- [ ] ユーザーからのフィードバックをモニター
- [ ] Issuesページで質問に対応

---

## 🆘 トラブルシューティング / Troubleshooting

### ZIPファイルが大きすぎる場合

- [ ] __pycache__ディレクトリが削除されているか確認
- [ ] テスト用PDFファイルが含まれていないか確認
- [ ] .gitignoreに従ってファイルが除外されているか確認

### アップロードに失敗する場合

- [ ] ファイルサイズが2GB以下であることを確認
- [ ] インターネット接続を確認
- [ ] GitHubのステータスページで障害がないか確認

### ダウンロード後に動作しない場合

- [ ] ZIPファイルの解凍が完全に完了しているか確認
- [ ] `test_installation.py` の結果を確認
- [ ] Python 3.7以上がインストールされているか確認

---

## 📞 サポート / Support

問題がある場合：
- GitHub Issues: https://github.com/Mizuho-NAGATA/SnapPDF/issues

---

**準備ができたら、GitHubでリリースを公開しましょう！**  
**Once ready, publish the release on GitHub!**

🎉 **Good luck with the release!** 🎉