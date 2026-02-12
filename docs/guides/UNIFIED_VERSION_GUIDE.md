# SnapPDF Unified Version Guide
# SnapPDF 統合版ガイド

## 概要 / Overview

SnapPDF Unified (`SnapPDF_unified.py`) は、すべてのSnapPDFバリエーション（2, 4, 5, 6, 15枚/ページ）を1つのプログラムに統合した新バージョンです。

SnapPDF Unified (`SnapPDF_unified.py`) is a new version that consolidates all SnapPDF variations (2, 4, 5, 6, 15 images/page) into a single program.

---

## 主な変更点 / Key Changes

### 🎯 統合による利点 / Benefits of Unification

1. **単一のプログラムで全レイアウトに対応**
   - 5つの別々のファイルを使い分ける必要がなくなりました
   - GUIのラジオボタンでレイアウトを簡単に切り替え可能

2. **コードの保守性向上**
   - 重複コードを削減（約95%の共通コード）
   - バグ修正や機能追加が1箇所で完結

3. **すべての機能を統合**
   - Excel読み込み機能
   - サムネイル表示
   - 並列画像処理
   - すべてのレイアウトオプション

---

## 使用方法 / How to Use

### 起動 / Launch

```bash
python SnapPDF_unified.py
```

### レイアウト選択 / Layout Selection

プログラムを起動すると、以下のレイアウトオプションがラジオボタンで表示されます：

When you launch the program, the following layout options will appear as radio buttons:

- **2 images (1×2)** - 大きく写真を表示 / Display photos large
- **4 images (2×2)** - 標準的なサイズ / Standard size
- **5 images (5×1)** - 横並び / Horizontal strip
- **6 images (3×2)** - バランスの良いサイズ / Balanced size
- **15 images (5×3)** - コンパクトに多数表示 / Compact display of many photos

---

## 従来バージョンからの移行 / Migration from Traditional Versions

### 機能比較 / Feature Comparison

| 機能 / Feature | 従来版 / Traditional | 統合版 / Unified |
|----------------|---------------------|------------------|
| レイアウト選択 / Layout Selection | 5個の別ファイル / 5 separate files | ラジオボタン / Radio buttons |
| Excel読み込み / Excel Import | SnapPDF.pyのみ / SnapPDF.py only | ✅ 利用可能 / Available |
| 画像選択 / Image Selection | ✅ | ✅ |
| サムネイル表示 / Thumbnails | ✅ | ✅ |
| 並列処理 / Parallel Processing | ✅ | ✅ |
| コード行数 / Lines of Code | ~2,000行 (5ファイル) / lines (5 files) | ~400行 (1ファイル) / lines (1 file) |

### 互換性 / Compatibility

従来のSnapPDFファイル（SnapPDF.py, SnapPDF2.py, SnapPDF4.py, SnapPDF6.py, SnapPDF15.py）は引き続き利用可能です。後方互換性のために保持されています。

The traditional SnapPDF files (SnapPDF.py, SnapPDF2.py, SnapPDF4.py, SnapPDF6.py, SnapPDF15.py) remain available and are kept for backward compatibility.

---

## 技術的な詳細 / Technical Details

### レイアウト設定 / Layout Configuration

統合版では、以下の設定がプリセットとして定義されています：

The unified version defines the following presets:

```python
LAYOUT_PRESETS = {
    "2": {"cols": 1, "rows": 2, "total": 2, "name": "2 images (1×2)"},
    "4": {"cols": 2, "rows": 2, "total": 4, "name": "4 images (2×2)"},
    "5": {"cols": 5, "rows": 1, "total": 5, "name": "5 images (5×1)"},
    "6": {"cols": 3, "rows": 2, "total": 6, "name": "6 images (3×2)"},
    "15": {"cols": 5, "rows": 3, "total": 15, "name": "15 images (5×3)"},
}
```

### アーキテクチャ / Architecture

- **クラスベース設計**: `SnapPDFUnifiedApp`クラスで全機能を管理
- **動的レイアウト生成**: 選択されたプリセットに基づいてPDFレイアウトを動的に構築
- **並列処理**: ThreadPoolExecutorを使用した高速画像処理（順序保持）
- **キャッシュ**: LRUキャッシュによるサムネイル生成の最適化

---

## FAQ

### Q: 統合版と従来版のどちらを使うべきですか？

**A:** 新規ユーザーには統合版の使用を強く推奨します。1つのプログラムで全機能にアクセスでき、今後のアップデートも統合版を中心に行われる予定です。

### Q: Should I use the unified version or traditional versions?

**A:** We strongly recommend the unified version for new users. It provides access to all features in one program, and future updates will focus on the unified version.

### Q: 従来のファイルは削除されますか？

**A:** いいえ。後方互換性のために従来のファイルは保持されます。ただし、新機能の追加は主に統合版で行われます。

### Q: Will the traditional files be deleted?

**A:** No. Traditional files will be kept for backward compatibility. However, new features will primarily be added to the unified version.

### Q: 統合版で問題が発生した場合は？

**A:** GitHubのIssuesでバグ報告をお願いします。また、緊急の場合は従来版を使用することもできます。

### Q: What if I encounter issues with the unified version?

**A:** Please report bugs on GitHub Issues. You can also use the traditional versions in urgent cases.

---

## 今後の開発計画 / Future Development Plans

1. **ドラッグ＆ドロップ対応の強化**
   - 画像のドラッグ＆ドロップによる追加と並び替え

2. **プレビュー機能**
   - PDF生成前のページレイアウトプレビュー

3. **カスタムレイアウト**
   - ユーザー定義のレイアウト設定

4. **バッチ処理**
   - 複数のPDFを一度に生成

---

## サポート / Support

問題や質問がある場合は、GitHubのIssuesページでお気軽にお問い合わせください。

For issues or questions, please feel free to contact us on the GitHub Issues page.

**GitHub Repository:** https://github.com/Mizuho-NAGATA/SnapPDF

---

## クレジット / Credits

この統合版は、AIリファクタリングツール（picoclaw風）を使用して開発されました。

This unified version was developed using AI refactoring tools (picoclaw-style).

Copyright (c) 2023-2026 NAGATA Mizuho  
Institute of Laser Engineering, Osaka University
