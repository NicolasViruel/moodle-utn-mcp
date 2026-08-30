"""Genera PDF de entrega desde Markdown (fpdf2)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    from fpdf import FPDF
except ImportError:
    raise SystemExit("Instalá fpdf2: pip install fpdf2")

FONT = Path(r"C:\Windows\Fonts\arial.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")
FONT_MONO = Path(r"C:\Windows\Fonts\consola.ttf")


class InformePDF(FPDF):
    def footer(self) -> None:
        self.set_y(-15)
        self.set_font("Arial", "", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")


def strip_md(text: str) -> str:
    text = text.replace("\u2011", "-").replace("\u2013", "-").replace("\u2014", "-")
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    return text


def md_to_pdf(md_path: Path, out_pdf: Path) -> None:
    if not md_path.exists():
        raise FileNotFoundError(md_path)
    if not FONT.exists():
        raise FileNotFoundError(f"No se encontró fuente: {FONT}")

    lines = md_path.read_text(encoding="utf-8").splitlines()
    pdf = InformePDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    pdf.add_font("Arial", "", str(FONT))
    pdf.add_font("Arial", "B", str(FONT_BOLD))
    if FONT_MONO.exists():
        pdf.add_font("Consolas", "", str(FONT_MONO))

    in_fence = False

    for raw in lines:
        line = raw.rstrip()
        pdf.set_x(pdf.l_margin)

        if line.startswith("```"):
            in_fence = not in_fence
            continue

        if in_fence:
            font = "Consolas" if FONT_MONO.exists() else "Arial"
            pdf.set_font(font, "", 9)
            pdf.multi_cell(0, 4.5, strip_md(line))
            continue

        if line.startswith("|") and "---" in line:
            continue
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            row = " — ".join(strip_md(c) for c in cells if c.strip())
            pdf.set_font("Arial", "", 10)
            pdf.multi_cell(0, 5, row)
            continue

        if not line.strip():
            pdf.ln(3)
            continue

        if line.startswith("# "):
            pdf.ln(4)
            pdf.set_font("Arial", "B", 16)
            pdf.multi_cell(0, 8, strip_md(line[2:].strip()))
            continue
        if line.startswith("## "):
            pdf.ln(3)
            pdf.set_font("Arial", "B", 13)
            pdf.multi_cell(0, 7, strip_md(line[3:].strip()))
            continue
        if line.startswith("### "):
            pdf.ln(2)
            pdf.set_font("Arial", "B", 11)
            pdf.multi_cell(0, 6, strip_md(line[4:].strip()))
            continue
        if line.strip() == "---":
            pdf.ln(2)
            continue
        if line.startswith("- "):
            pdf.set_font("Arial", "", 10)
            pdf.multi_cell(0, 5, "• " + strip_md(line[2:].strip()))
            continue
        if re.match(r"^\d+\.\s", line):
            pdf.set_font("Arial", "", 10)
            pdf.multi_cell(0, 5, strip_md(line.strip()))
            continue

        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 5, strip_md(line.strip()))

    pdf.output(str(out_pdf))
    print(f"Generado: {out_pdf}")


def main() -> None:
    root = Path(__file__).resolve().parent
    md = root / (sys.argv[1] if len(sys.argv) > 1 else "tp-resuelto_Nicolas_Viruel.md")
    out = md.with_suffix(".pdf")
    md_to_pdf(md, out)


if __name__ == "__main__":
    main()
