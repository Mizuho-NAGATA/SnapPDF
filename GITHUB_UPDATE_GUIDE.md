# GitHub v2.0.0 更新手順ガイド / GitHub Update Guide

## 📋 状況 / Situation

GitHubのメインブランチに既に古いv2.0.0が存在し、これを新しく更新したv2.0.0に置き換えたい。

---

## 🎯 推奨される方法 / Recommended Approach

### オプション1: 既存のv2.0.0を更新（同じバージョン番号を維持）

この方法は、バージョン番号を変えずに内容を更新します。

#### ステップ1: Gitリポジトリの準備

```bash
# 1. 現在のローカルリポジトリに移動
cd /path/to/your/local/SnapPDF

# 2. 最新の状態を取得
git pull origin main

# 3. 現在のブランチを確認
git branch
```

#### ステップ2: 新しいファイルで既存のファイルを置き換え

```bash
# デスクトップの新しいファイルをローカルリポジトリにコピー
# Windows例:
xcopy /E /Y "C:\Users\000332\Desktop\SnapPDF-v2.0.0\*" "C:\path\to\your\local\SnapPDF\"

# macOS/Linux例:
cp -r ~/Desktop/SnapPDF-v2.0.0/* /path/to/your/local/SnapPDF/
```

#### ステップ3: 変更をコミット

```bash
# 変更されたファイルを確認
git status

# 新しいファイルを追加
git add .

# コミット
git commit -m "Update v2.0.0: Add batch launch files and comprehensive documentation

- Add run_snappdf.bat and run_snapsearch.bat for easy Windows launch
- Add HOW_TO_RUN.md with detailed launch instructions for all OS
- Add RELEASE_NOTES.md with complete release information
- Update all documentation with batch file launch methods
- Add .gitignore for clean repository
- Add multiple guide documents for better user experience"

# プッシュ
git push origin main
```

#### ステップ4: 既存のv2.0.0タグとリリースを削除（必要な場合）

既にv2.0.0タグやリリースが存在する場合：

**GitHub Web上で:**
1. リポジトリの「Releases」ページに移動
2. 既存のv2.0.0リリースを見つける
3. 右側の「...」メニューから「Delete release」を選択
4. 削除を確認

**Gitコマンドでタグを削除:**
```bash
# ローカルのタグを削除
git tag -d v2.0.0

# リモートのタグを削除
git push origin :refs/tags/v2.0.0
```

#### ステップ5: 新しいv2.0.0リリースを作成

**GitHub Web上で:**
1. 「Releases」→「Draft a new release」
2. Tag version: `v2.0.0`
3. Target: `main` ブランチ
4. Release title: `SnapPDF v2.0.0 - Unified Application with Easy Launch`
5. Description: `RELEASE_NOTES.md`の内容をコピー
6. `SnapPDF-v2.0.0.zip`をアップロード
7. 「Publish release」をクリック

---

### オプション2: v2.0.1として新規リリース（より安全）

バージョン番号を上げて、混乱を避ける方法です。

#### メリット:
- ✅ 既存のv2.0.0ユーザーに影響なし
- ✅ 履歴が明確
- ✅ タグの削除が不要

#### デメリット:
- ⚠️ バージョン番号が変わる
- ⚠️ 全ドキュメントでバージョン番号を更新する必要あり

#### 手順:

```bash
# 1. バージョン番号を更新（全ドキュメント内の2.0.0を2.0.1に）
# 以下のファイルを編集:
# - README.md
# - VERSION_INFO.md
# - RELEASE_NOTES.md
# - INSTALLATION.md
# - 他の全ドキュメント

# 2. コミット
git add .
git commit -m "Release v2.0.1: Enhanced documentation and launch methods"

# 3. プッシュ
git push origin main

# 4. 新しいタグを作成
git tag -a v2.0.1 -m "Version 2.0.1"
git push origin v2.0.1

# 5. GitHub Webでv2.0.1リリースを作成
```

---

### オプション3: v2.0.0パッチ版として扱う（中間的アプローチ）

v2.0.0-patch1 や v2.0.0.1 のような形式でリリース。

```bash
git tag -a v2.0.0-patch1 -m "Version 2.0.0 Patch 1: Documentation and launch improvements"
git push origin v2.0.0-patch1
```

---

## 🚀 最も簡単な手順（推奨）

### クイック更新ステップ

```bash
# ステップ1: ローカルリポジトリに移動
cd /path/to/your/SnapPDF/repository

# ステップ2: 新しいファイルをコピー
# （デスクトップのSnapPDF-v2.0.0から、リポジトリに上書き）

# ステップ3: 変更を確認
git status

# ステップ4: 全てを追加してコミット
git add .
git commit -m "Update v2.0.0: Add enhanced launch methods and documentation"

# ステップ5: プッシュ
git push origin main

# ステップ6: GitHub Webで既存のv2.0.0リリースを削除

# ステップ7: 新しいv2.0.0リリースを作成してZIPをアップロード
```

---

## 📝 詳細な手順書（初心者向け）

### Windows での手順

#### 1. GitHubリポジトリをローカルにクローン（まだの場合）

```cmd
cd C:\Users\000332\Desktop
git clone https://github.com/Mizuho-NAGATA/SnapPDF.git SnapPDF-repo
cd SnapPDF-repo
```

#### 2. 新しいファイルを上書きコピー

```cmd
# 新しいファイルをリポジトリにコピー
xcopy /E /Y "C:\Users\000332\Desktop\SnapPDF-v2.0.0\*" "C:\Users\000332\Desktop\SnapPDF-repo\"
```

#### 3. Gitで変更を確認

```cmd
git status
```

緑色や赤色のテキストで変更されたファイルが表示されます。

#### 4. 変更をステージング

```cmd
git add .
```

#### 5. コミット

```cmd
git commit -m "Update v2.0.0: Add batch files and enhanced documentation"
```

#### 6. GitHubにプッシュ

```cmd
git push origin main
```

GitHubのユーザー名とパスワード（またはトークン）を入力してください。

#### 7. GitHub Webで作業

**既存のリリースを削除:**
1. https://github.com/Mizuho-NAGATA/SnapPDF/releases にアクセス
2. v2.0.0リリースを見つける
3. 右側の「...」→「Delete release」
4. 確認

**既存のタグを削除:**
```cmd
git tag -d v2.0.0
git push origin :refs/tags/v2.0.0
```

**新しいリリースを作成:**
1. 「Draft a new release」をクリック
2. Tag: `v2.0.0`
3. Target: `main`
4. Title: `SnapPDF v2.0.0 - Unified Application with Easy Launch`
5. Description: `RELEASE_NOTES.md`の内容をコピペ
6. ZIPファイル（`SnapPDF-v2.0.0.zip`）をアップロード
7. 「Publish release」

---

## 🔧 トラブルシューティング

### 問題1: "Permission denied" エラー

**解決策:**
```bash
# SSH鍵を設定していない場合、HTTPSを使用
git remote set-url origin https://github.com/Mizuho-NAGATA/SnapPDF.git

# または、SSH鍵を設定
# https://docs.github.com/ja/authentication/connecting-to-github-with-ssh
```

### 問題2: "Your branch is behind" メッセージ

**解決策:**
```bash
git pull origin main
# コンフリクトがある場合は解決してから再度プッシュ
```

### 問題3: タグが削除できない

**解決策:**
```bash
# 強制削除
git push origin :refs/tags/v2.0.0 --force

# または、GitHub Web上で手動削除
```

### 問題4: コミットメッセージを間違えた

**解決策:**
```bash
# 最後のコミットメッセージを修正（プッシュ前なら）
git commit --amend -m "新しいメッセージ"

# プッシュ済みの場合は新しいコミットを作成
```

---

## ⚠️ 注意事項

### タグを削除する前に確認すべきこと

1. **他のユーザーがv2.0.0を使用しているか?**
   - 使用されている場合、v2.0.1として新規リリースを推奨

2. **リリースノートや変更履歴を保持したいか?**
   - 保持したい場合、古いリリースを削除せずv2.0.1を作成

3. **DOIやZenodoなどの永続的識別子を使用しているか?**
   - 使用している場合、バージョン番号を変更すべき

---

## 📊 各方法の比較

| 方法 | 難易度 | リスク | 推奨度 |
|------|--------|--------|--------|
| v2.0.0を更新（タグ削除） | 中 | 中 | ⭐⭐⭐⭐ |
| v2.0.1として新規リリース | 低 | 低 | ⭐⭐⭐⭐⭐ |
| v2.0.0-patch1 | 中 | 低 | ⭐⭐⭐ |
| ファイルのみ更新（リリースなし） | 低 | 低 | ⭐⭐ |

---

## 🎯 推奨される最終的な手順

### 最もシンプルで安全な方法: v2.0.1としてリリース

```bash
# 1. バージョン番号を2.0.1に更新
# （全ドキュメントで検索置換: "2.0.0" → "2.0.1"）

# 2. コミット
git add .
git commit -m "Release v2.0.1: Enhanced launch methods and documentation"
git push origin main

# 3. タグを作成
git tag -a v2.0.1 -m "Version 2.0.1"
git push origin v2.0.1

# 4. GitHub Webでリリースを作成
```

**メリット:**
- ✅ 既存のユーザーに影響なし
- ✅ 履歴が保持される
- ✅ 複雑なタグ削除が不要
- ✅ GitHubのベストプラクティスに準拠

---

## 🆘 サポートが必要な場合

1. **GitHubのドキュメント:**
   - [リリースの管理](https://docs.github.com/ja/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
   - [タグの作成](https://docs.github.com/ja/desktop/contributing-and-collaborating-using-github-desktop/managing-commits/managing-tags)

2. **Gitコマンドのヘルプ:**
   ```bash
   git help tag
   git help push
   git help commit
   ```

3. **トラブルシューティング:**
   - Stack Overflow
   - GitHub Community
   - Git公式ドキュメント

---

## ✅ チェックリスト

更新前に確認:
- [ ] ローカルリポジトリが最新（`git pull`済み）
- [ ] 新しいファイルが準備できている
- [ ] バックアップを取った
- [ ] コミットメッセージを準備した

更新後に確認:
- [ ] GitHubでファイルが更新されているか確認
- [ ] リリースページで新しいZIPが表示されているか確認
- [ ] ZIPをダウンロードして動作確認
- [ ] READMEのリンクが正しく機能するか確認

---

**幸運を祈ります！何か問題があれば、このガイドを参照してください。**

*Last Updated: 2026-02-02*