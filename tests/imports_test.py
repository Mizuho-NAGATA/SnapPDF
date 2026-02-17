import importlib
import sys

REQUIRED_MODULES = [
    "pandas",
    "PIL",        # Pillow
    "PyPDF2",
    "reportlab",
    "openpyxl",
    "xlrd",
]


def test_imports():
    missing = []
    for m in REQUIRED_MODULES:
        try:
            importlib.import_module(m)
        except Exception as e:
            missing.append((m, str(e)))
    if missing:
        print("Missing or failing imports:", missing)
        raise ImportError(f"Missing modules or import failures: {missing}")


if __name__ == "__main__":
    try:
        test_imports()
        print("All required modules imported successfully.")
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)
