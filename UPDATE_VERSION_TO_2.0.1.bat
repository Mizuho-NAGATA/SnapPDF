@echo off
chcp 65001 >nul
echo ============================================================
echo   SnapPDF バージョン番号一括変更スクリプト
echo   Version Number Batch Update Script
echo   2.0.0 → 2.0.1
echo ============================================================
echo.

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo 現在のディレクトリ: %CD%
echo.
echo このスクリプトは以下のファイルのバージョン番号を変更します:
echo This script will update version numbers in the following files:
echo.
echo - README.md
echo - VERSION_INFO.md
echo - RELEASE_NOTES.md
echo - INSTALLATION.md
echo - MIGRATION_GUIDE.md
echo - QUICKSTART_JP.md
echo - HOW_TO_RUN.md
echo - REFACTORING_SUMMARY.md
echo - GITHUB_RELEASE_CHECKLIST.md
echo - GITHUB_RELEASE_README.md
echo - GITHUB_UPDATE_GUIDE.md
echo.
echo バージョン 2.0.0 → 2.0.1 に変更します。
echo Version will be changed from 2.0.0 to 2.0.1
echo.
echo 続行しますか？ (Y/N)
set /p CONFIRM=">> "

if /i not "%CONFIRM%"=="Y" (
    echo キャンセルしました。
    echo Cancelled.
    pause
    exit /b
)

echo.
echo [処理中 / Processing...]
echo.

REM PowerShellを使用してファイル内容を置換
powershell -Command "$files = @('README.md', 'VERSION_INFO.md', 'RELEASE_NOTES.md', 'INSTALLATION.md', 'MIGRATION_GUIDE.md', 'QUICKSTART_JP.md', 'HOW_TO_RUN.md', 'REFACTORING_SUMMARY.md', 'GITHUB_RELEASE_CHECKLIST.md', 'GITHUB_RELEASE_README.md', 'GITHUB_UPDATE_GUIDE.md'); foreach ($file in $files) { if (Test-Path $file) { (Get-Content $file -Raw -Encoding UTF8) -replace 'v2\.0\.0', 'v2.0.1' -replace 'Version: 2\.0\.0', 'Version: 2.0.1' -replace 'バージョン.*: 2\.0\.0', 'バージョン: 2.0.1' -replace 'SnapPDF-v2\.0\.0', 'SnapPDF-v2.0.1' | Set-Content $file -Encoding UTF8 -NoNewline; Write-Host \"Updated: $file\" } else { Write-Host \"Not found: $file\" -ForegroundColor Yellow } }"

echo.
echo ============================================================
echo   完了しました！/ Completed!
echo ============================================================
echo.
echo 変更されたファイルを確認してください。
echo Please review the changed files.
echo.
echo 次のステップ:
echo Next steps:
echo.
echo 1. 変更内容を確認
echo    Review changes: git diff
echo.
echo 2. フォルダ名を変更（オプション）
echo    Rename folder (optional):
echo    SnapPDF-v2.0.0 → SnapPDF-v2.0.1
echo.
echo 3. ZIPファイル名も更新
echo    Update ZIP filename:
echo    SnapPDF-v2.0.0.zip → SnapPDF-v2.0.1.zip
echo.
echo 4. Gitでコミット
echo    Commit with Git:
echo    git add .
echo    git commit -m "Release v2.0.1"
echo    git push origin main
echo.
echo 5. タグを作成
echo    Create tag:
echo    git tag -a v2.0.1 -m "Version 2.0.1"
echo    git push origin v2.0.1
echo.
echo 6. GitHubでv2.0.1リリースを作成
echo    Create v2.0.1 release on GitHub
echo.
pause
