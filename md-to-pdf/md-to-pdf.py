import argparse
from html import escape
from pathlib import Path
from typing import Optional

import markdown
from xhtml2pdf import pisa


THEMES = {
    "github": {
        "background": "#ffffff",
        "text": "#24292f",
        "muted": "#57606a",
        "accent": "#0969da",
        "border": "#d0d7de",
        "code_background": "#f6f8fa",
        "quote_background": "#f6f8fa",
        "link": "#0969da",
    },
    "dark": {
        "background": "#161b22",
        "text": "#e6edf3",
        "muted": "#8b949e",
        "accent": "#79c0ff",
        "border": "#30363d",
        "code_background": "#0d1117",
        "quote_background": "#1c2128",
        "link": "#79c0ff",
    },
    "sepia": {
        "background": "#f4ecd8",
        "text": "#433422",
        "muted": "#796a54",
        "accent": "#8c4a2f",
        "border": "#d8c8a8",
        "code_background": "#eae0ca",
        "quote_background": "#eae0ca",
        "link": "#8c4a2f",
    },
    "ocean": {
        "background": "#f0f8ff",
        "text": "#16324f",
        "muted": "#526d82",
        "accent": "#0077b6",
        "border": "#b8d8e8",
        "code_background": "#e2f1f8",
        "quote_background": "#e2f1f8",
        "link": "#0077b6",
    },
}


def build_stylesheet(theme: str) -> str:
    colors = THEMES[theme]
    return f"""
        @page {{
            size: A4;
            margin: 20mm 18mm;
            background-color: {colors["background"]};
        }}
        html, body {{
            background: {colors["background"]};
            color: {colors["text"]};
            font-family: Arial, sans-serif;
            font-size: 10pt;
            line-height: 1.55;
            background-color: {colors["background"]};
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: {colors["accent"]};
            line-height: 1.25;
            -pdf-keep-with-next: true;
        }}
        h1, h2 {{ border-bottom: 1px solid {colors["border"]}; padding-bottom: 0.25em; }}
        a {{ color: {colors["link"]}; }}
        blockquote {{
            background: {colors["quote_background"]};
            border-left: 3px solid {colors["accent"]};
            color: {colors["muted"]};
            margin-left: 0;
            padding: 0.2em 1em;
        }}
        code, pre {{
            background: {colors["code_background"]};
            font-family: "Courier New", monospace;
        }}
        code {{ padding: 0.1em 0.3em; }}
        pre {{
            border: 1px solid {colors["border"]};
            padding: 0.8em;
            -pdf-keep-in-frame-mode: shrink;
        }}
        pre code {{ padding: 0; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid {colors["border"]}; padding: 0.4em 0.6em; }}
        th {{ background: {colors["code_background"]}; text-align: left; }}
        img {{ height: auto; max-width: 100%; }}
        hr {{ border: 0; border-top: 1px solid {colors["border"]}; }}
    """


def convert_markdown_to_pdf(
    input_path: Path,
    output_path: Optional[Path] = None,
    theme: str = "github",
) -> Path:
    input_path = Path(input_path).resolve()
    if not input_path.is_file():
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {input_path}")
    if input_path.suffix.lower() != ".md":
        raise ValueError("O arquivo de entrada deve ter a extensão .md")
    if theme not in THEMES:
        raise ValueError(f"Tema desconhecido: {theme}")

    output_path = Path(output_path).resolve() if output_path else input_path.with_suffix(".pdf")
    if output_path.suffix.lower() != ".pdf":
        raise ValueError("O arquivo de saída deve ter a extensão .pdf")
    if output_path == input_path:
        raise ValueError("Os caminhos de entrada e saída não podem ser iguais")
    if not output_path.parent.is_dir():
        raise FileNotFoundError(f"Pasta de saída não encontrada: {output_path.parent}")

    markdown_text = input_path.read_text(encoding="utf-8-sig")
    body = markdown.markdown(
        markdown_text,
        extensions=["fenced_code", "tables", "sane_lists"],
    )
    document = (
        "<!doctype html><html><head><meta charset=\"utf-8\">"
        f"<title>{escape(input_path.stem)}</title>"
        f"<style>{build_stylesheet(theme)}</style>"
        f"</head><body>{body}</body></html>"
    )
    with output_path.open("wb") as pdf_file:
        result = pisa.CreatePDF(
            document,
            dest=pdf_file,
            path=str(input_path.parent),
            encoding="utf-8",
        )
    if result.err:
        raise RuntimeError(f"Falha ao gerar o PDF: {result.err} erro(s)")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Converte um arquivo Markdown em PDF mantendo sua formatação."
    )
    parser.add_argument("input", type=Path, help="Arquivo .md de entrada")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Caminho do PDF (padrão: mesmo nome e pasta do arquivo de entrada)",
    )
    parser.add_argument(
        "--theme",
        choices=THEMES,
        default="github",
        help="Esquema de cores do PDF (padrão: github)",
    )
    args = parser.parse_args()

    try:
        output_path = convert_markdown_to_pdf(args.input, args.output, args.theme)
    except (FileNotFoundError, ValueError) as error:
        parser.error(str(error))

    print(f"PDF criado: {output_path}")


if __name__ == "__main__":
    main()
