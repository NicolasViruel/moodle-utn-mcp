"""Genera los PDF de la Unidad 5 (MS2) desde Markdown."""
from __future__ import annotations

import re
import zipfile
from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parent
FONT = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
FONT_BOLD = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")


class InformePDF(FPDF):
    def footer(self) -> None:
        self.set_y(-15)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, f"Página {self.page_no()}", align="C")
        self.set_text_color(0, 0, 0)


def strip_md(text: str) -> str:
    text = text.replace("\u2011", "-").replace("\u2013", "-").replace("\u2014", "-")
    text = text.replace("\u201c", '"').replace("\u201d", '"').replace("\u2018", "'").replace("\u2019", "'")
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    return text


def write_line(pdf: InformePDF, text: str, size: int, bold: bool, lh: float) -> None:
    pdf.set_x(pdf.l_margin)
    pdf.set_font("DejaVu", "B" if bold else "", size)
    pdf.multi_cell(pdf.epw, lh, text)


def md_to_pdf(md_path: Path, out_pdf: Path) -> None:
    lines = md_path.read_text(encoding="utf-8").splitlines()
    pdf = InformePDF()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_font("DejaVu", "", str(FONT))
    pdf.add_font("DejaVu", "B", str(FONT_BOLD))
    pdf.add_page()

    for raw in lines:
        line = raw.rstrip()
        if line.startswith("|") and set(line.replace("|", "").replace("-", "").replace(":", "").strip()) == set():
            continue
        if line.startswith("|") and re.match(r"^\|?\s*-{3,}", line.replace("|", " | ")):
            continue
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            row = " | ".join(strip_md(c) for c in cells if c.strip())
            write_line(pdf, row, 8, False, 4.4)
            continue
        if not line.strip():
            pdf.ln(2)
            continue
        if line.startswith("# "):
            pdf.ln(2)
            write_line(pdf, strip_md(line[2:].strip()), 15, True, 7)
            continue
        if line.startswith("## "):
            pdf.ln(2)
            write_line(pdf, strip_md(line[3:].strip()), 12, True, 6)
            continue
        if line.startswith("### "):
            pdf.ln(1)
            write_line(pdf, strip_md(line[4:].strip()), 11, True, 5.5)
            continue
        if line.strip() == "---":
            pdf.ln(1)
            continue
        if line.startswith("- "):
            write_line(pdf, "• " + strip_md(line[2:].strip()), 10, False, 5)
            continue
        write_line(pdf, strip_md(line), 10, False, 5)

    pdf.output(str(out_pdf))
    print(f"Escrito: {out_pdf} ({out_pdf.stat().st_size} bytes)")


def zip_entrega(folder: Path, pdf_name: str, md_name: str, zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(folder / pdf_name, pdf_name)
        zf.write(folder / md_name, md_name)
    print(f"ZIP: {zip_path} ({zip_path.stat().st_size} bytes)")


def main() -> None:
    jobs = [
        (
            "tp1-elicitacion",
            "tp1-resuelto_Nicolas_Viruel.md",
            "tp1-resuelto_Nicolas_Viruel.pdf",
            "Viruel_Nicolas_TP1_Elicitacion.zip",
        ),
        (
            "tp2-demos",
            "tp2-resuelto_Nicolas_Viruel.md",
            "tp2-resuelto_Nicolas_Viruel.pdf",
            "Viruel_Nicolas_TP2_Demos.zip",
        ),
        (
            "tp3-ia-copiloto",
            "tp3-resuelto_Nicolas_Viruel.md",
            "tp3-resuelto_Nicolas_Viruel.pdf",
            "Viruel_Nicolas_TP3_IA_Copiloto.zip",
        ),
    ]
    for folder, md_name, pdf_name, zip_name in jobs:
        base = ROOT / folder
        md_to_pdf(base / md_name, base / pdf_name)
        zip_entrega(base, pdf_name, md_name, ROOT / zip_name)


if __name__ == "__main__":
    main()
