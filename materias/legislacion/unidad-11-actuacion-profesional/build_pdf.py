"""Genera el PDF de entrega desde el Markdown."""
from pathlib import Path
import re

try:
    from fpdf import FPDF
except ImportError:
    raise SystemExit("Instalá fpdf2: pip install fpdf2")

ROOT = Path(__file__).resolve().parent
MD = ROOT / "tp-resuelto_Nicolas_Viruel.md"
OUT_PDF = ROOT / "tp-resuelto_Nicolas_Viruel.pdf"

FONT_CANDIDATES = [
    (
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    ),
    (
        Path(r"C:\Windows\Fonts\arial.ttf"),
        Path(r"C:\Windows\Fonts\arialbd.ttf"),
    ),
]


class InformePDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Body", "", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Nicolás Viruel — Legislación, Unidad 11 — pág. {self.page_no()}", align="C")


def strip_md(text: str) -> str:
    text = text.replace("\u2011", "-").replace("\u2013", "-").replace("\u2014", "-")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    return text


def main() -> None:
    regular, bold = next(
        ((a, b) for a, b in FONT_CANDIDATES if a.exists() and b.exists()),
        (None, None),
    )
    if regular is None:
        raise FileNotFoundError("No se encontró DejaVu Sans ni Arial.")

    pdf = InformePDF()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()
    pdf.add_font("Body", "", str(regular))
    pdf.add_font("Body", "B", str(bold))

    for raw in MD.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        pdf.set_x(pdf.l_margin)
        if line.startswith("|") and "---" in line:
            continue
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            row = " — ".join(strip_md(c) for c in cells if c.strip())
            pdf.set_font("Body", "", 10)
            pdf.multi_cell(0, 5, row)
            continue
        if not line.strip():
            pdf.ln(3)
            continue
        if line.startswith("# "):
            pdf.ln(2)
            pdf.set_font("Body", "B", 15)
            pdf.multi_cell(0, 8, strip_md(line[2:].strip()))
            continue
        if line.startswith("## "):
            pdf.ln(3)
            pdf.set_font("Body", "B", 13)
            pdf.multi_cell(0, 7, strip_md(line[3:].strip()))
            continue
        if line.strip() == "---":
            pdf.ln(1)
            continue
        if line.startswith("- "):
            pdf.set_font("Body", "", 10)
            pdf.multi_cell(0, 5, "• " + strip_md(line[2:].strip()))
            continue
        if re.match(r"^\d+\.\s", line):
            pdf.set_font("Body", "", 10)
            pdf.multi_cell(0, 5, strip_md(line.strip()))
            continue
        pdf.set_font("Body", "", 10)
        pdf.multi_cell(0, 5, strip_md(line.strip()))

    pdf.output(str(OUT_PDF))
    print(f"Generado: {OUT_PDF} ({OUT_PDF.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
