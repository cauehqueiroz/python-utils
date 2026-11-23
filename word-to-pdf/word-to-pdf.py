import argparse
from pathlib import Path

import win32com.client


def main():
    parser = argparse.ArgumentParser(description="Convert a Word document to PDF.")
    parser.add_argument("input", type=Path, help="Word document to convert")
    parser.add_argument(
        "-o", "--output", type=Path,
        help="PDF output path (default: same folder and filename as input)",
    )
    args = parser.parse_args()

    input_path = args.input.resolve()
    output_path = (
        args.output.resolve()
        if args.output
        else input_path.with_suffix(".pdf")
    )

    if not input_path.is_file():
        parser.error(f"Input file not found: {input_path}")

    word = None
    document = None
    try:
        word = win32com.client.DispatchEx("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0

        document = word.Documents.Open(str(input_path), ReadOnly=True)
        document.ExportAsFixedFormat(str(output_path), 17)  # 17 = PDF
        print(f"Created: {output_path}")
    finally:
        if document is not None:
            document.Close(False)
        if word is not None:
            word.Quit()


if __name__ == "__main__":
    main()