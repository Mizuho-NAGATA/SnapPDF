# GitHub Web版での更新ガイド / GitHub Web Update Guide

## 🌐 コマンドライン不要！ブラウザだけで完結

このガイドでは、Gitコマンドを使わずに、Web版GitHubだけで古いv2.0.0を新しいファイルに置き換える方法を説明します。

---

## 📋 2つの方法 / Two Approaches

### 方法A: v2.0.0を上書き更新
- 同じバージョン番号を維持
- 既存のファイルを1つずつ置き換え

### 方法B: v2.0.1として新規リリース（推奨）
- より安全で標準的
- 新しいバージョンとして追加

---

## 🚀 方法A: Web版でv2.0.0を上書き更新

### ステップ1: 既存のリリースを削除

1. **GitHubリポジトリにアクセス**
   ```
   https://github.com/Mizuho-NAGATA/SnapPDF
   ```

2. **Releasesタブをクリック**
   - リポジトリページの右側にある「Releases」をクリック

3. **既存のv2.0.0リリースを削除**
   - v2.0.0リリースを見つける
   - 右側の「...」メニューボタンをクリック
   - 「Delete release」を選択
   - 確認ダイアログで「Delete this release」をクリック

### ステップ2: ファイルを1つずつ更新

#### 2-1. 新しいファイルを追加

1. **リポジトリのメインページに移動**
   - 「Code」タブをクリック

2. **「Add file」→「Upload files」をクリック**

3. **新しいファイルをドラッグ&ドロップ**
   - `run_snappdf.bat`
   - `run_snapsearch.bat`
   - `HOW_TO_RUN.md`
   - `RELEASE_NOTES.md`
   - `GITHUB_RELEASE_CHECKLIST.md`
   - `GITHUB_RELEASE_README.md`
   - `.gitignore`

4. **コミットメッセージを入力**
   ```
   Add new batch files and documentation
   
   - Add run_snappdf.bat and run_snapsearch.bat for easy Windows launch
   - Add comprehensive documentation guides
   ```

5. **「Commit changes」をクリック**

#### 2-2. 既存のファイルを更新

各ファイルを個別に更新します：

1. **更新したいファイルをクリック**（例: `README.md`）

2. **鉛筆アイコン（Edit this file）をクリック**

3. **内容を全て選択してコピー**
   - Ctrl+A（全選択）→ Ctrl+C（コピー）

4. **デスクトップの新しいファイルを開く**
   - `C:\Users\000332\Desktop\SnapPDF-v2.0.0\README.md`
   - 内容を全てコピー

5. **GitHubのエディタに貼り付け**
   - 既存の内容を全て削除
   - Ctrl+V で新しい内容を貼り付け

6. **「Commit changes」をクリック**
   - コミットメッセージを入力（例: "Update README.md with new launch methods"）
   - 「Commit changes」をクリック

**更新が必要なファイル:**
- `README.md`
- `QUICKSTART_JP.md`
- `INSTALLATION.md`
- `MIGRATION_GUIDE.md`
- `VERSION_INFO.md`

#### 2-3. snappdfフォルダ内のファイルを確認

`snappdf` フォルダが変更されていない場合はスキップしてOKです。

### ステップ3: 新しいリリースを作成

1. **Releasesページに移動**
   ```
   https://github.com/Mizuho-NAGATA/SnapPDF/releases
   ```

2. **「Draft a new release」をクリック**

3. **リリース情報を入力**
   - **Choose a tag**: `v2.0.0` と入力（既存のタグを選択またはタイプ）
   - **Target**: `main` ブランチを選択
   - **Release title**: 
     ```
     SnapPDF v2.0.0 - Unified Application with Easy Launch
     ```

4. **説明文を入力**
   
   デスクトップの `RELEASE_NOTES.md` を開いて、内容を全てコピー＆ペースト

5. **ZIPファイルをアップロード**
   
   a. まずZIPファイルを作成:
   - `C:\Users\000332\Desktop\SnapPDF-v2.0.0` フォルダを右クリック
   - 「送る」→「圧縮 (zip形式) フォルダー」
   - ファイル名: `SnapPDF-v2.0.0.zip`
   
   b. GitHubにアップロード:
   - 「Attach binaries...」エリアにZIPファイルをドラッグ&ドロップ
   - またはクリックしてファイルを選択

6. **「Publish release」をクリック**

### ステップ4: 確認

1. **Releasesページで新しいv2.0.0が表示されているか確認**
2. **ZIPファイルがダウンロード可能か確認**
3. **ダウンロードして解凍し、動作確認**

---

## 🆕 方法B: v2.0.1として新規リリース（推奨）

この方法の方がシンプルで安全です！

### ステップ1: ローカルでバージョン番号を変更

1. **UPDATE_VERSION_TO_2.0.1.batを実行**
   ```
   C:\Users\000332\Desktop\SnapPDF-v2.0.0\UPDATE_VERSION_TO_2.0.1.bat
   ```
   をダブルクリック

2. **フォルダ名を変更**
   - `SnapPDF-v2.0.0` → `SnapPDF-v2.0.1` にリネーム

3. **ZIPファイルを作成**
   - `SnapPDF-v2.0.1` フォルダを右クリック
   - 「送る」→「圧縮 (zip形式) フォルダー」
   - ファイル名: `SnapPDF-v2.0.1.zip`

### ステップ2: Web版で新しいファイルをアップロード

#### オプションA: 個別にファイルをアップロード（推奨）

1. **GitHubリポジトリにアクセス**
   ```
   https://github.com/Mizuho-NAGATA/SnapPDF
   ```

2. **「Add file」→「Upload files」をクリック**

3. **新しい/更新されたファイルをドラッグ&ドロップ**
   
   新規ファイル:
   - `run_snappdf.bat`
   - `run_snapsearch.bat`
   - `HOW_TO_RUN.md`
   - `RELEASE_NOTES.md`
   - `GITHUB_RELEASE_CHECKLIST.md`
   - `GITHUB_RELEASE_README.md`
   - `GITHUB_WEB_UPDATE_GUIDE.md`
   - `.gitignore`
   - `UPDATE_VERSION_TO_2.0.1.bat`
   - `UPDATE_GITHUB.bat`
   - `GITHUB_UPDATE_GUIDE.md`

4. **コミットメッセージを入力**
   ```
   Release v2.0.1: Enhanced launch methods and documentation
   
   - Add Windows batch files for easy launch
   - Add comprehensive documentation
   - Update all guides with new launch methods
   ```

5. **「Commit changes」をクリック**

6. **既存ファイルを更新**（方法Aのステップ2-2を参照）
   - `README.md`
   - `QUICKSTART_JP.md`
   - `INSTALLATION.md`
   - `MIGRATION_GUIDE.md`
   - `VERSION_INFO.md`

#### オプションB: GitHub Desktopを使用（より簡単）

1. **GitHub Desktopをダウンロード**
   ```
   https://desktop.github.com/
   ```

2. **インストールしてサインイン**

3. **リポジトリをクローン**
   - File → Clone repository
   - `Mizuho-NAGATA/SnapPDF` を選択
   - ローカルパスを指定

4. **ファイルをコピー**
   ```
   C:\Users\000332\Desktop\SnapPDF-v2.0.1\*
   →
   クローンしたリポジトリフォルダ
   ```

5. **GitHub Desktopで確認**
   - 変更されたファイルが左側に表示される
   - コミットメッセージを入力
   - 「Commit to main」をクリック
   - 「Push origin」をクリック

### ステップ3: v2.0.1リリースを作成

1. **Releasesページに移動**
   ```
   https://github.com/Mizuho-NAGATA/SnapPDF/releases
   ```

2. **「Draft a new release」をクリック**

3. **リリース情報を入力**
   - **Choose a tag**: `v2.0.1` と入力（新しいタグを作成）
   - **Target**: `main` ブランチを選択
   - **Release title**: 
     ```
     SnapPDF v2.0.1 - Enhanced Launch Methods and Documentation
     ```

4. **説明文を入力**
   
   以下のテンプレートを使用:

   ```markdown
   # SnapPDF v2.0.1 - Enhanced Launch Methods and Documentation 🚀

   ## 🎉 新機能 / What's New

   ### Windows ユーザー向けの簡単起動！
   - ✨ `run_snappdf.bat` をダブルクリックするだけ！
   - ✨ `run_snapsearch.bat` でSnapSearchも簡単起動！
   - ✨ コマンド入力不要で初心者にも優しい

   ### 充実したドキュメント
   - 📚 `HOW_TO_RUN.md` - 全OS対応の起動方法ガイド（新規）
   - 📚 全ドキュメントを更新し、バッチファイル起動方法を追加
   - 📚 リリースノートとチェックリストを追加

   ## 📦 ダウンロードとインストール

   1. 下の `SnapPDF-v2.0.1.zip` をダウンロード
   2. 任意の場所に解凍
   3. `pip install -r requirements.txt` で依存パッケージをインストール
   4. **Windows**: `run_snappdf.bat` をダブルクリック
   5. **macOS/Linux**: `python3 snappdf_unified.py` を実行

   ## 📋 主な変更点 / Changes from v2.0.0

   - ✅ Windows用起動バッチファイルを追加
   - ✅ 包括的なドキュメントを追加
   - ✅ 全ドキュメントを更新
   - ✅ .gitignoreを追加
   - ✅ Git/GitHub管理ツールを追加

   ## 📚 ドキュメント

   - **HOW_TO_RUN.md** - 起動方法ガイド（推奨）
   - **QUICKSTART_JP.md** - 5分で始めるガイド
   - **INSTALLATION.md** - 詳細なインストール手順
   - **README.md** - 完全なドキュメント

   ## システム要件

   - Python 3.7以上
   - Windows 10/11, macOS 10.14+, Linux
   - RAM: 2GB以上

   完全なリリースノートは `RELEASE_NOTES.md` をご覧ください。
   ```

5. **ZIPファイルをアップロード**
   - `SnapPDF-v2.0.1.zip` をドラッグ&ドロップ

6. **「Publish release」をクリック**

---

## 📊 方法の比較 / Comparison

| 項目 | 方法A: v2.0.0上書き | 方法B: v2.0.1新規 |
|------|---------------------|-------------------|
| 難易度 | 高い | 低い |
| 作業時間 | 30-60分 | 15-30分 |
| 既存ユーザーへの影響 | あり | なし |
| タグ管理 | 削除・再作成が必要 | 新規作成のみ |
| 推奨度 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🎯 推奨される手順（最もシンプル）

### Web版のみで完結する最短ルート

1. **バージョン番号を2.0.1に変更**
   ```
   UPDATE_VERSION_TO_2.0.1.bat をダブルクリック
   ```

2. **フォルダ名を変更**
   ```
   SnapPDF-v2.0.0 → SnapPDF-v2.0.1
   ```

3. **ZIPを作成**
   ```
   フォルダを右クリック → 圧縮
   ```

4. **GitHubで新しいファイルをアップロード**
   - 「Add file」→「Upload files」
   - 新しいファイル（.bat, 新しい.md）をドラッグ&ドロップ
   - コミット

5. **既存ファイルを1つずつ更新**
   - ファイルをクリック → 鉛筆アイコン → 編集 → コミット
   - 更新が必要: README.md, QUICKSTART_JP.md, INSTALLATION.md, MIGRATION_GUIDE.md, VERSION_INFO.md

6. **v2.0.1リリースを作成**
   - Releases → Draft a new release
   - Tag: v2.0.1
   - ZIPをアップロード
   - Publish

**所要時間: 約20-30分**

---

## 🔧 便利なヒント / Useful Tips

### ファイルの一括編集

複数のファイルを更新する場合：

1. **1つのファイルを編集**
2. **「Commit changes」をクリック前に**
   - 「Create a new branch for this commit」を選択
   - ブランチ名: `update-v2.0.1`
3. **「Propose changes」をクリック**
4. **同じブランチで他のファイルも編集**
5. **全部完了したら、Pull Requestを作成**
6. **自分でマージ**

この方法なら、複数の変更を1つのコミットにまとめられます。

### ファイルの削除

不要なファイルを削除する場合：

1. ファイルをクリック
2. ゴミ箱アイコンをクリック
3. コミットメッセージを入力
4. 「Commit changes」

### ファイル名の変更

1. ファイルをクリック
2. 鉛筆アイコンをクリック
3. ファイル名の部分をクリックして編集
4. 内容も必要に応じて編集
5. 「Commit changes」

---

## ✅ チェックリスト / Checklist

### アップロード前
- [ ] UPDATE_VERSION_TO_2.0.1.batを実行（v2.0.1にする場合）
- [ ] フォルダ名を変更
- [ ] ZIPファイルを作成
- [ ] 不要なファイル（__pycache__等）を削除済み

### Web版での作業
- [ ] 新しいファイルをアップロード済み
- [ ] 既存ファイルを更新済み
- [ ] すべてのコミットが完了

### リリース作成
- [ ] タグを作成（v2.0.1）
- [ ] リリースタイトルを入力
- [ ] 説明文を入力
- [ ] ZIPファイルをアップロード
- [ ] リリースを公開

### 最終確認
- [ ] リリースページで表示確認
- [ ] ZIPファイルがダウンロード可能
- [ ] READMEが正しく表示されている
- [ ] ダウンロードしたZIPが動作する

---

## 🆘 トラブルシューティング / Troubleshooting

### ファイルのアップロードができない

**原因**: ファイルサイズが大きすぎる（25MB制限）

**解決策**:
- __pycache__フォルダを削除
- 画像や動画ファイルを除外
- Git LFSを使用（上級者向け）

### 編集中にエラーが出る

**原因**: 他の人が同時に編集した

**解決策**:
- ページをリフレッシュ
- 変更内容を一度コピー
- 再度編集

### リリースが作成できない

**原因**: タグが既に存在する

**解決策**:
- 異なるタグ名を使用（例: v2.0.1-updated）
- または既存のタグを削除（Settings → Tags）

### コミットが失敗する

**原因**: インターネット接続の問題

**解決策**:
- ネット接続を確認
- ページをリフレッシュして再試行
- 変更内容をコピーして保存

---

## 📞 サポート / Support

Web版での操作で困ったら：

1. **GitHubヘルプ**
   - https://docs.github.com/ja

2. **このガイド**
   - 手順を再確認

3. **GitHub Issues**
   - 質問や問題を報告
   - https://github.com/Mizuho-NAGATA/SnapPDF/issues

---

## 🎉 完了！ / Done!

Web版だけでGitHubリポジトリを更新し、新しいリリースを作成できました！

**お疲れさまでした！**

---

*Last Updated: 2026-02-02*
*Version: 2.0.1*