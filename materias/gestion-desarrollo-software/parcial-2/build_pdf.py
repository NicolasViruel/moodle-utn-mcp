"""Genera parcial-2_Nicolas_Viruel.pdf desde el Markdown (tablas en grilla)."""
from pathlib import Path
import re

try:
    from fpdf import FPDF
except ImportError:
    raise SystemExit("Instalá fpdf2: pip install fpdf2")

ROOT = Path(__file__).resolve().parent
MD = ROOT / "parcial-2_Nicolas_Viruel.md"
OUT_PDF = ROOT / "parcial-2_Nicolas_Viruel.pdf"

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
        self.set_font("Body", "", 8)
        self.set_text_color(100, 100, 100)
        self.cell(
            0, 10,
            f"Nicolás Viruel — GDS, Evaluación Parcial 2 — pág. {self.page_no()}",
            align="C",
        )
        self.set_text_color(0, 0, 0)


def strip_md(text: str) -> str:
    text = text.replace("\u2011", "-")
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    return text


def render_table(pdf: FPDF, rows: list[list[str]]) -> None:
    ncols = max(len(r) for r in rows)
    rows = [r + [""] * (ncols - len(r)) for r in rows]
    usable = pdf.w - pdf.l_margin - pdf.r_margin
    # Ancho proporcional al largo máximo de cada columna, con piso.
    lens = [max(len(r[i]) for r in rows) for i in range(ncols)]
    lens = [max(l, 3) for l in lens]
    # Columnas cortas (números) no deberían ensancharse demasiado.
    weights = [min(l, 60) for l in lens]
    total = sum(weights)
    widths = [max(usable * w / total, 9) for w in weights]
    scale = usable / sum(widths)
    widths = [w * scale for w in widths]

    pdf.set_font("Body", "", 8.5)
    line_h = 4.2
    with pdf.table(
        col_widths=widths,
        line_height=line_h,
        text_align="LEFT",
        borders_layout="ALL",
        padding=1,
    ) as table:
        for i, r in enumerate(rows):
            row = table.row()
            for cell in r:
                if i == 0:
                    pdf.set_font("Body", "B", 8.5)
                else:
                    pdf.set_font("Body", "", 8.5)
                row.cell(strip_md(cell))
    pdf.set_font("Body", "", 10)
    pdf.ln(2)


def main() -> None:
    if not MD.exists():
        raise FileNotFoundError(MD)
    regular, bold = next(
        ((a, b) for a, b in FONT_CANDIDATES if a.exists() and b.exists()),
        (None, None),
    )
    if regular is None:
        raise FileNotFoundError("No se encontró DejaVu Sans ni Arial.")

    lines = MD.read_text(encoding="utf-8").splitlines()
    pdf = InformePDF()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()
    pdf.add_font("Body", "", str(regular))
    pdf.add_font("Body", "B", str(bold))

    table_rows: list[list[str]] = []

    def flush_table():
        nonlocal table_rows
        if table_rows:
            render_table(pdf, table_rows)
            table_rows = []

    for raw in lines:
        line = raw.rstrip()
        pdf.set_x(pdf.l_margin)

        if line.startswith("|"):
            if "---" in line and set(line.replace("|", "").strip()) <= set("-: "):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            table_rows.append(cells)
            continue
        flush_table()

        if not line.strip():
            pdf.ln(2.5)
            continue
        if line.startswith("# "):
            pdf.ln(2)
            pdf.set_font("Body", "B", 15)
            pdf.multi_cell(0, 8, strip_md(line[2:].strip()))
            continue
        if line.startswith("## "):
            pdf.ln(2)
            pdf.set_font("Body", "B", 12.5)
            pdf.multi_cell(0, 7, strip_md(line[3:].strip()))
            continue
        if line.startswith("### "):
            pdf.ln(1.5)
            pdf.set_font("Body", "B", 10.5)
            pdf.multi_cell(0, 6, strip_md(line[4:].strip()))
            continue
        if line.strip() == "---":
            pdf.ln(1)
            continue
        if line.startswith("- "):
            pdf.set_font("Body", "", 10)
            pdf.set_x(pdf.l_margin + 3)
            pdf.multi_cell(0, 5, "• " + strip_md(line[2:].strip()))
            continue
        if re.match(r"^\d+\.\s", line):
            pdf.set_font("Body", "", 10)
            pdf.set_x(pdf.l_margin + 3)
            pdf.multi_cell(0, 5, strip_md(line.strip()))
            continue

        pdf.set_font("Body", "", 10)
        pdf.multi_cell(0, 5, strip_md(line.strip()))

    flush_table()
    pdf.output(str(OUT_PDF))
    print(f"Generado: {OUT_PDF} ({OUT_PDF.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
