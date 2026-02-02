@echo off
chcp 65001 >nul
echo ============================================================
echo   SnapPDF v2.0.0 GitHub更新スクリプト
echo   GitHub Update Script
echo ============================================================
echo.

REM 現在のディレクトリを保存
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo [ステップ 1/7] 現在のディレクトリを確認 / Checking current directory
echo 現在のディレクトリ: %CD%
echo.
pause

echo [ステップ 2/7] Gitリポジトリのステータス確認 / Checking Git status
git status
echo.
echo 上記の変更内容を確認してください。
echo Please review the changes above.
echo.
pause

echo [ステップ 3/7] 変更をステージング / Staging changes
git add .
echo すべての変更がステージングされました。
echo All changes have been staged.
echo.
pause

echo [ステップ 4/7] コミット / Committing
echo コミットメッセージを入力してください（Enterで既定のメッセージを使用）:
echo Enter commit message (press Enter to use default):
set /p COMMIT_MSG=">> "

if "%COMMIT_MSG%"=="" (
    set "COMMIT_MSG=Update v2.0.0: Add batch files and enhanced documentation"
)

git commit -m "%COMMIT_MSG%"
echo.
echo コミットが完了しました。
echo Commit completed.
echo.
pause

echo [ステップ 5/7] リモートリポジトリにプッシュ / Pushing to remote
echo これからリモートリポジトリにプッシュします。
echo About to push to remote repository.
echo.
echo 続行しますか？ (Y/N)
set /p CONFIRM=">> "

if /i "%CONFIRM%"=="Y" (
    git push origin main
    echo.
    echo プッシュが完了しました。
    echo Push completed.
) else (
    echo プッシュをキャンセルしました。
    echo Push cancelled.
)
echo.
pause

echo [ステップ 6/7] タグの管理 / Tag management
echo.
echo 既存のv2.0.0タグを削除して再作成しますか？ (Y/N)
echo Delete and recreate v2.0.0 tag? (Y/N)
set /p TAG_CONFIRM=">> "

if /i "%TAG_CONFIRM%"=="Y" (
    echo ローカルタグを削除中...
    git tag -d v2.0.0 2>nul
    echo リモートタグを削除中...
    git push origin :refs/tags/v2.0.0 2>nul
    echo.
    echo 新しいタグを作成中...
    git tag -a v2.0.0 -m "SnapPDF v2.0.0 - Unified Application with Easy Launch"
    echo タグをプッシュ中...
    git push origin v2.0.0
    echo.
    echo タグの更新が完了しました。
    echo Tag update completed.
) else (
    echo タグの更新をスキップしました。
    echo Tag update skipped.
)
echo.
pause

echo [ステップ 7/7] 完了 / Completed
echo ============================================================
echo   更新が完了しました！
echo   Update completed!
echo ============================================================
echo.
echo 次の作業:
echo Next steps:
echo.
echo 1. GitHubのReleasesページにアクセス
echo    Visit GitHub Releases page
echo    https://github.com/Mizuho-NAGATA/SnapPDF/releases
echo.
echo 2. 既存のv2.0.0リリースを削除（必要な場合）
echo    Delete existing v2.0.0 release (if needed)
echo.
echo 3. 新しいリリースを作成
echo    Create new release
echo    - Tag: v2.0.0
echo    - Title: SnapPDF v2.0.0 - Unified Application with Easy Launch
echo    - Description: RELEASE_NOTES.mdの内容をコピー
echo    - Upload: SnapPDF-v2.0.0.zip
echo.
echo 4. リリースを公開
echo    Publish release
echo.
pause
