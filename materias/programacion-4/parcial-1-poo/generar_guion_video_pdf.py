"""Genera PDF con guion paso a paso para video de defensa Parcial 1."""
from pathlib import Path

from fpdf import FPDF

OUT = Path(__file__).resolve().parent / "Guion_Video_Parcial1_Viruel.pdf"
MD = Path(__file__).resolve().parent / "Guion_Video_Parcial1_Viruel.md"


def ascii_safe(text: str) -> str:
    replacements = {
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
        "ñ": "n", "ü": "u",
        "Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U",
        "Ñ": "N",
        "—": "-", "–": "-", "…": "...", "↔": "<->", "→": "->", "•": "-",
        "`": "",
        "**": "",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.strip()


class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Pagina {self.page_no()}", align="C")


def main() -> None:
    if not MD.exists():
        raise FileNotFoundError(MD)

    raw_lines = MD.read_text(encoding="utf-8").splitlines()
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", size=10)
    pdf.set_margins(15, 15, 15)

    for line in raw_lines:
        line = ascii_safe(line.strip())
        if not line or line in {"-", "*", "**"}:
            pdf.ln(3)
            continue
        if line.startswith("# "):
            pdf.set_font("Helvetica", "B", 14)
            pdf.multi_cell(pdf.epw, 7, line[2:])
            pdf.set_font("Helvetica", size=10)
            pdf.ln(2)
        elif line.startswith("## "):
            pdf.set_font("Helvetica", "B", 12)
            pdf.multi_cell(pdf.epw, 6, line[3:])
            pdf.set_font("Helvetica", size=10)
            pdf.ln(1)
        elif line.startswith("---"):
            pdf.ln(2)
        elif line.startswith("- "):
            bullet = line[2:].strip()
            if bullet:
                pdf.multi_cell(pdf.epw, 5, f"  * {bullet}")
        elif line.startswith("> "):
            pdf.set_font("Helvetica", "I", 10)
            pdf.multi_cell(pdf.epw, 5, line[2:])
            pdf.set_font("Helvetica", size=10)
        elif line[0].isdigit() and ". " in line[:4]:
            pdf.multi_cell(pdf.epw, 5, line)
        else:
            pdf.multi_cell(pdf.epw, 5, line)

    pdf.output(str(OUT))
    print(f"PDF generado: {OUT}")


if __name__ == "__main__":
    main()
