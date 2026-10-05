"""Genera PDFs de TP1 y TP2 desde Markdown."""
from pathlib import Path
import re
import sys

try:
    from fpdf import FPDF
except ImportError:
    raise SystemExit("Instalá fpdf2: pip install fpdf2")

ROOT = Path(__file__).resolve().parent
FONT = Path(r"C:\Windows\Fonts\arial.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")


class InformePDF(FPDF):
    def footer(self):
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

    for raw in lines:
        line = raw.rstrip()
        pdf.set_x(pdf.l_margin)

        if line.startswith("|") and "---" in line:
            continue
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            row = " | ".join(strip_md(c) for c in cells if c.strip())
            pdf.set_font("Arial", "", 8)
            pdf.multi_cell(0, 4.5, row)
            pdf.ln(1)
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

        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 5, strip_md(line))

    pdf.output(str(out_pdf))
    print(f"Escrito: {out_pdf}")


def main() -> None:
    jobs = [
        ("tp1-resuelto_Nicolas_Viruel.md", "tp1-resuelto_Nicolas_Viruel.pdf"),
        ("tp2-resuelto_Nicolas_Viruel.md", "tp2-resuelto_Nicolas_Viruel.pdf"),
    ]
    for md_name, pdf_name in jobs:
        md_to_pdf(ROOT / md_name, ROOT / pdf_name)


if __name__ == "__main__":
    main()
