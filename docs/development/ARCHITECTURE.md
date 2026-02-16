# SnapPDF Tabbed Architecture
# SnapPDF タブ版アーキテクチャ

## 📐 システム構成図 / System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SnapPDF Tabbed                           │
│                     (SnapPDF.py)                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ├── Main Application Layer
                              │   └── SnapPDFTabbedApp (Notebook/Tabs)
                              │       ├── PDF Creation Tab
                              │       └── PDF Search Tab
                              │
                              ├── PDF Creation Tab (SnapPDFTab)
                              │   ├── GUI Components
                              │   │   ├── Title/Remarks Input
                              │   │   ├── Layout Selection (Radio Buttons)
                              │   │   ├── Excel File Selection
                              │   │   ├── Image Selection
                              │   │   ├── Thumbnail Display (Scrollable)
                              │   │   └── PDF Export Button
                              │   │
                              │   ├── Business Logic
                              │   │   ├── Layout Configuration (LAYOUT_PRESETS)
                              │   │   ├── Image Processing (Parallel)
                              │   │   ├── Thumbnail Generation (LRU Cache)
                              │   │   └── Excel Data Handling
                              │   │
                              │   └── PDF Generation (ReportLab)
                              │       ├── Page Layout
                              │       ├── Header/Footer
                              │       └── Image Table
                              │
                              ├── PDF Search Tab (PDFSearchTab)
                              │   ├── GUI Components
                              │   │   ├── Folder Selection
                              │   │   ├── Keyword Input (Multiple)
                              │   │   ├── Search Button
                              │   │   └── Results Display
                              │   │
                              │   └── Search Logic
                              │       ├── PDF Text Extraction (PyPDF2)
                              │       ├── Keyword Matching
                              │       ├── Results Window
                              │       └── CSV Export
                              │
                              └── Cross-Platform Support
                                  ├── Multi-Platform Font Selection
                                  │   ├── select_font_for_pdf()
                                  │   └── select_font_for_gui()
                                  └── PDF Opening (OS-specific)
```

## 🔄 データフロー / Data Flow

### PDF Creation Tab Flow (PDF作成タブフロー)

```
1. User Input
   ↓
┌──────────────────────────────┐
│  Select Layout (2/4/6/15)    │
│  Select Excel File (Optional)│
│  Select Images               │
└──────────────────────────────┘
   ↓
2. Processing
   ↓
┌──────────────────────────────┐
│  Load Excel Data             │
│  Generate Thumbnails (Cache) │
│  Process Images (Parallel)   │
└──────────────────────────────┘
   ↓
3. Layout Generation
   ↓
┌──────────────────────────────┐
│  Get Layout Preset           │
│  Calculate Image Dimensions  │
│  Build Page Structure        │
└──────────────────────────────┘
   ↓
4. PDF Generation
   ↓
┌──────────────────────────────┐
│  Create PDF Document         │
│  Add Excel Table (if any)    │
│  Add Image Tables            │
│  Add Headers/Footers         │
└──────────────────────────────┘
   ↓
5. Output
   ↓
┌──────────────────────────────┐
│  Save PDF File               │
│  Open PDF (Platform-Specific)│
└──────────────────────────────┘
```

### PDF Search Tab Flow (PDF検索タブフロー)

```
1. User Input
   ↓
┌──────────────────────────────┐
│  Select Folder               │
│  Enter Keywords (Multiple)   │
│  Click Search                │
└──────────────────────────────┘
   ↓
2. Search Processing
   ↓
┌──────────────────────────────┐
│  Scan Folder for PDFs        │
│  Extract Text (PyPDF2)       │
│  Match Keywords              │
└──────────────────────────────┘
   ↓
3. Results Display
   ↓
┌──────────────────────────────┐
│  Show Results Window         │
│  Display Matches             │
│  Option to Save as CSV       │
└──────────────────────────────┘
```

## 🎨 レイアウトシステム / Layout System

### レイアウトプリセット構成 / Layout Preset Configuration

```python
LAYOUT_PRESETS = {
    "2": {
        "cols": 2,      # 列数 / Columns
        "rows": 1,      # 行数 / Rows
        "total": 2,     # 1ページあたりの画像数 / Images per page
        "name": "2 images (2×1)"
    },
    "4": {
        "cols": 2,
        "rows": 2,
        "total": 4,
        "name": "4 images (2×2)"
    },
    "6": {
        "cols": 3,
        "rows": 2,
        "total": 6,
        "name": "6 images (3×2)"
    },
    "15": {
        "cols": 5,
        "rows": 3,
        "total": 15,
        "name": "15 images (5×3)"
    }
}
```

**Note**: Unicode multiplication sign (U+00D7: ×) is used instead of ASCII 'x' to prevent character encoding issues.

### 動的サイズ計算 / Dynamic Size Calculation

```
利用可能エリア / Available Area:
- Width:  A4横幅 - 2インチマージン
- Height: A4高さ - 2.5インチ(上) - 0.5インチ(下)

画像サイズ計算 / Image Size Calculation:
target_width  = available_width / cols - 10
target_height = available_height / rows - 10

アスペクト比保持 / Maintain Aspect Ratio:
if new_height > target_height:
    new_height = target_height
    new_width = new_height × image_ratio
```

## 📊 クラス構造 / Class Structure

```
┌──────────────────────────────────────────────┐
│         SnapPDFTabbedApp                     │
│         (Main Application)                   │
├──────────────────────────────────────────────┤
│ Attributes:                                  │
│  - root: Tk                                  │
│  - notebook: ttk.Notebook                    │
│  - snap_pdf: SnapPDFTab                      │
│  - pdf_search: PDFSearchTab                  │
├──────────────────────────────────────────────┤
│ Methods:                                     │
│  + __init__()                                │
│  + run()                                     │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│         SnapPDFTab                           │
│         (PDF Creation)                       │
├──────────────────────────────────────────────┤
│ Attributes:                                  │
│  - parent: Frame                             │
│  - image_paths: List[str]                    │
│  - photo_images: List[PhotoImage]            │
│  - entries: List[Entry]                      │
│  - excel_data: List[List]                    │
│  - excel_headers: List[str]                  │
│  - selected_layout: StringVar                │
│  - thumbnail_canvas: Canvas                  │
│  - thumbnail_inner_frame: Frame              │
├──────────────────────────────────────────────┤
│ Methods:                                     │
│  + __init__(parent)                          │
│  + _build_gui()                              │
│  + select_excel_file()                       │
│  + select_images()                           │
│  + generate_thumbnail(path) @lru_cache       │
│  + display_thumbnails()                      │
│  + process_image_for_pdf(path, config)       │
│  + create_pdf()                              │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│         PDFSearchTab                         │
│         (PDF Search)                         │
├──────────────────────────────────────────────┤
│ Attributes:                                  │
│  - parent: Frame                             │
│  - folder_path: str                          │
│  - keyword_entries: List[Entry]              │
├──────────────────────────────────────────────┤
│ Methods:                                     │
│  + __init__(parent)                          │
│  + _build_gui()                              │
│  + select_folder()                           │
│  + search_pdfs()                             │
│  + extract_text_from_pdf(path)               │
│  + save_to_csv(results)                      │
│  + show_results(results)                     │
└──────────────────────────────────────────────┘
```

## 🔧 主要コンポーネント / Key Components

### 1. タブインターフェース / Tabbed Interface

```
Root Window (Tk)
│
└── Notebook (ttk.Notebook)
    ├── PDF Creation Tab
    │   └── SnapPDFTab Components
    └── PDF Search Tab
        └── PDFSearchTab Components
```

### 2. PDF Creation Tab GUI Components

```
PDF Creation Tab (Frame)
│
├── Input Frame
│   ├── Title Entry
│   └── Remarks Entry
│
├── Layout Frame (LabelFrame)
│   └── Radio Buttons (2/4/6/15)
│
├── Control Buttons
│   ├── Select Excel Button
│   ├── Select Images Button
│   └── Output to PDF Button
│
└── Thumbnail Frame (Scrollable Canvas)
    └── Image Grid (10 columns)
        └── Mousewheel Support
```

### 3. PDF Search Tab GUI Components

```
PDF Search Tab (Frame)
│
├── Folder Selection
│   ├── Folder Path Label
│   └── Select Folder Button
│
├── Keyword Input Frame
│   └── Multiple Entry Fields (4 keywords)
│
├── Search Button
│
└── Results Display
    ├── Results Window (Toplevel)
    │   └── Scrollable Text Widget
    └── CSV Export Option
```

### 4. 並列処理 / Parallel Processing

```python
# サムネイル生成の並列バッチ処理 / Parallel thumbnail generation
with ThreadPoolExecutor() as executor:
    batch_size = 10
    for start in range(0, num_images, batch_size):
        executor.submit(update_thumbnails, start, start + batch_size)

# PDF用画像処理の並列処理（順序保持） / Parallel image processing (order preserved)
with ThreadPoolExecutor() as executor:
    futures = [
        executor.submit(process_image_for_pdf, path, layout_config)
        for path in image_paths
    ]
    results = [f.result() for f in futures]  # 順序保持 / Order preserved
```

### 5. キャッシュシステム / Cache System

```python
@lru_cache(maxsize=None)
def generate_thumbnail(self, file_path):
    image = Image.open(file_path)
    image.thumbnail((100, 100))
    return ImageTk.PhotoImage(image=image)
```

### 6. PDF 検索機能 / PDF Search Functionality

```python
def extract_text_from_pdf(self, pdf_path):
    """Extract text from all pages of a PDF file"""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def search_pdfs(self):
    """Search for keywords in PDF files"""
    # Scan folder for PDFs
    # Extract text from each PDF
    # Match keywords (case-insensitive)
    # Display results
```

## 🌐 クロスプラットフォーム対応 / Cross-Platform Support

### マルチプラットフォームフォント選択 / Multi-Platform Font Selection

```python
def select_font_for_pdf():
    """Select appropriate font for PDF generation based on OS"""
    system = platform.system()
    
    if system == "Windows":
        font_candidates = [
            ("MS-Gothic", "msgothic.ttc"),
            ("Yu-Gothic", "YuGothR.ttc"),
            ("BIZ-UDGothicR", "BIZ-UDGothicR.ttc"),
        ]
    elif system == "Darwin":  # macOS
        font_candidates = [
            ("Hiragino-Sans", "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"),
            ("Hiragino-Kaku", "/System/Library/Fonts/Hiragino Sans GB.ttc"),
            ("Arial-Unicode", "/Library/Fonts/Arial Unicode.ttf"),
        ]
    else:  # Linux
        font_candidates = [
            ("NotoSansCJK", "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
            ("TakaoPGothic", "/usr/share/fonts/truetype/takao-gothic/TakaoPGothic.ttf"),
            ("IPAGothic", "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"),
            ("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        ]
    # Returns font_name (fallback: "Helvetica")

def select_font_for_gui():
    """Select appropriate font for GUI based on OS"""
    system = platform.system()
    
    if system == "Windows":
        return ("Yu Gothic UI", 11)
    elif system == "Darwin":  # macOS
        return ("Hiragino Sans", 13)
    else:  # Linux
        return ("Noto Sans CJK JP", 11)
```

### PDF自動オープン / Automatic PDF Opening

```python
# PDF自動オープン / Open PDF automatically
if os.name == "nt":  # Windows
    os.startfile(pdf_file_path)
elif platform.system() == "Darwin":  # macOS
    subprocess.Popen(["open", pdf_file_path])
else:  # Linux
    subprocess.Popen(["xdg-open", pdf_file_path])
```

## 📦 依存関係 / Dependencies

```
Python 3.x
│
├── Standard Library
│   ├── os
│   ├── platform
│   ├── subprocess
│   ├── threading
│   ├── datetime
│   ├── csv
│   ├── functools (lru_cache)
│   ├── tkinter (GUI)
│   │   ├── ttk (Notebook/Tabs)
│   │   └── filedialog, messagebox
│   └── concurrent.futures (ThreadPoolExecutor)
│
└── Third-Party Libraries
    ├── pandas (Excel読み込み / Excel import)
    ├── PIL/Pillow (画像処理 / Image processing)
    ├── PyPDF2 (PDF検索・テキスト抽出 / PDF search & text extraction)
    ├── reportlab (PDF生成 / PDF generation)
    └── tkinterdnd2 (ドラッグ&ドロップ対応 / Drag & drop support - optional)
```

## 🎯 設計原則 / Design Principles

### 1. タブによる機能分離 / Functional Separation with Tabs
- PDF作成とPDF検索を1つのアプリケーションに統合
- タブインターフェースで機能を分離し、ユーザビリティ向上
- Unified PDF creation and search in one application
- Functional separation with tabs for improved usability

### 2. DRY (Don't Repeat Yourself)
- 重複コードを排除 / Eliminate code duplication
- 設定駆動のレイアウトシステム / Configuration-driven layout system

### 3. 単一責任の原則 (Single Responsibility)
- `SnapPDFTabbedApp`: アプリケーション全体の管理
- `SnapPDFTab`: PDF作成機能
- `PDFSearchTab`: PDF検索機能
- Each class has a specific responsibility

### 4. 拡張性 (Extensibility)
- 新しいレイアウトプリセットを簡単に追加可能
- Easy to add new layout presets
- プラグイン可能なアーキテクチャ / Pluggable architecture

### 5. パフォーマンス (Performance)
- 並列処理による高速化 / Parallel processing for speed
- LRUキャッシュによる最適化 / LRU cache optimization

### 6. クロスプラットフォーム対応 (Cross-Platform)
- OS自動検出によるフォント選択
- プラットフォーム固有の機能を適切に処理
- Automatic font selection based on OS detection
- Proper handling of platform-specific features

## 🔍 コード品質指標 / Code Quality Metrics

```
┌─────────────────────────────────────────┐
│ Metric              │ Value             │
├─────────────────────┼───────────────────┤
│ Lines of Code       │ 684               │
│ Classes             │ 3                 │
│ - SnapPDFTabbedApp  │ (Main App)        │
│ - SnapPDFTab        │ (PDF Creation)    │
│ - PDFSearchTab      │ (PDF Search)      │
│ Methods             │ 17+               │
│ Cyclomatic          │ Low               │
│ Complexity          │                   │
│ Code Duplication    │ 0%                │
│ Test Coverage       │ Manual Testing    │
│ Security Issues     │ 0                 │
└─────────────────────────────────────────┘
```

## 🚀 パフォーマンス特性 / Performance Characteristics

### 並列処理の効率 / Parallel Processing Efficiency

```
Sequential Processing:
Image1 → Image2 → Image3 → Image4 → Image5
(Time = 5T)

Parallel Processing:
Image1 ┐
Image2 ├→ ThreadPoolExecutor
Image3 ├→ Results in order
Image4 ├→ (Time ≈ T + overhead)
Image5 ┘
```

### メモリ使用量 / Memory Usage

```
- サムネイルキャッシュ: LRU Cache (無制限)
- 画像処理: 一時メモリ使用
- PDF生成: ストリーミング書き込み
```

## 📖 参考資料 / References

### 主要技術 / Core Technologies

- **ReportLab Documentation**: https://www.reportlab.com/docs/
  - PDF生成ライブラリ / PDF generation library
- **PIL/Pillow Documentation**: https://pillow.readthedocs.io/
  - 画像処理ライブラリ / Image processing library
- **PyPDF2 Documentation**: https://pypdf2.readthedocs.io/
  - PDF読み取り・テキスト抽出 / PDF reading and text extraction
- **Python ThreadPoolExecutor**: https://docs.python.org/3/library/concurrent.futures.html
  - 並列処理 / Parallel processing
- **Tkinter Documentation**: https://docs.python.org/3/library/tkinter.html
  - GUI フレームワーク / GUI framework
- **ttk (Themed Tkinter)**: https://docs.python.org/3/library/tkinter.ttk.html
  - タブインターフェース / Tab interface

### 関連ドキュメント / Related Documentation

- [QUICKSTART.md](../QUICKSTART.md) - クイックスタートガイド
- [TABBED_VERSION_GUIDE.md](../guides/TABBED_VERSION_GUIDE.md) - タブ版完全ガイド
- [REFACTORING_SUMMARY.md](./REFACTORING_SUMMARY.md) - リファクタリング概要

---

**Last Updated**: 2026-02-13  
**Version**: 3.0 (Tabbed Interface)  
**Author**: NAGATA Mizuho with AI Assistant
