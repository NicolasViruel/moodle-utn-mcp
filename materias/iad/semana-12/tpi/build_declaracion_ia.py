"""PDF de declaración de uso de IA generativa – TPI IAD Entrega 5."""
from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "Declaracion-uso-IA-TPI-IAD_Nicolas_Viruel.pdf"
FONT = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
FONT_BOLD = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")


class DeclaracionPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")
        self.set_text_color(0, 0, 0)


def body(pdf: FPDF, texto: str, size: int = 10, bold: bool = False, lh: float = 5.4) -> None:
    pdf.set_x(pdf.l_margin)
    pdf.set_font("DejaVu", "B" if bold else "", size)
    pdf.multi_cell(pdf.epw, lh, texto)
    pdf.ln(0.6)


def check(pdf: FPDF, marcado: bool, texto: str) -> None:
    marca = "[X]" if marcado else "[ ]"
    body(pdf, f"{marca}  {texto}", size=10, bold=False, lh=5.2)


def main() -> None:
    pdf = DeclaracionPDF()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_font("DejaVu", "", str(FONT))
    pdf.add_font("DejaVu", "B", str(FONT_BOLD))
    pdf.add_page()

    body(pdf, "DECLARACIÓN DE USO DE INTELIGENCIA ARTIFICIAL GENERATIVA", size=13, bold=True, lh=7)
    body(pdf, "Trabajo Práctico Integrador - IAD", size=11, bold=True, lh=6)
    body(
        pdf,
        "Esta declaración se adjunta junto con el archivo .ipynb correspondiente "
        "a cada entrega del TPI, a partir de la Entrega 5. Debe completarse tanto "
        "si se utilizaron como si no se utilizaron herramientas de inteligencia "
        "artificial generativa.",
    )
    pdf.ln(2)

    body(pdf, "Datos de la entrega", size=11, bold=True, lh=6)
    for linea in [
        "Integrantes del TPI: Viruel, Nicolás",
        "Comisión: 10 (Grupo J)",
        "Dataset asignado: hotel_booking_TPI_grupo_J.csv",
        "Entrega N°: 5",
        "Fecha: 19/10/2026",
    ]:
        body(pdf, linea)
    pdf.ln(2)

    body(pdf, "1. Declaración de uso", size=12, bold=True, lh=6.5)
    check(
        pdf,
        False,
        "El equipo declara que no utilizó herramientas de inteligencia artificial "
        "generativa para la realización de esta entrega.",
    )
    check(
        pdf,
        True,
        "El equipo declara que utilizó herramientas de inteligencia artificial "
        "generativa como apoyo para la realización de esta entrega.",
    )
    pdf.ln(1)

    body(pdf, "Herramienta/s utilizada/s", size=11, bold=True, lh=6)
    body(
        pdf,
        "Cursor (asistente de código), usado como copiloto para escribir y revisar "
        "el notebook. Las decisiones de análisis, las variables y la interpretación "
        "son del integrante.",
    )
    pdf.ln(1)

    body(pdf, "Finalidad de uso", size=11, bold=True, lh=6)
    check(pdf, True, "Comprender o revisar conceptos de análisis de datos, EDA o aprendizaje automático.")
    check(pdf, True, "Consultar procedimientos, métodos o criterios para realizar el análisis.")
    check(pdf, True, "Generar o proponer consultas SQL o código en Python/R.")
    check(pdf, True, "Revisar, explicar o depurar consultas SQL o código en Python/R.")
    check(pdf, True, "Interpretar mensajes de error o problemas de ejecución.")
    check(pdf, False, "Construir, revisar o interpretar visualizaciones y resultados.")
    check(pdf, False, "Contrastar cálculos, métricas, modelos, interpretaciones o conclusiones.")
    check(pdf, True, "Revisar la redacción, claridad u organización del notebook/trabajo.")
    check(pdf, False, "Organizar la presentación del análisis o planificar los pasos de trabajo.")
    check(pdf, False, "Otro uso.")
    pdf.ln(1)

    body(pdf, "Descripción del uso realizado", size=11, bold=True, lh=6)
    body(
        pdf,
        "Armé esta entrega con un asistente de código como copiloto. Yo definí el "
        "problema (clasificar si una reserva se cancela), elegí los predictores a "
        "partir del EDA y de la planificación de Semana 11, y decidí qué variables "
        "no entrarían porque no están disponibles al registrar la reserva. También "
        "escribí la interpretación de las predicciones y las limitaciones del modelo.",
    )
    body(
        pdf,
        "Le pedí a la herramienta que pasara esas decisiones a celdas SQL + Python "
        "(carga en DuckDB, partición train/test y árbol de decisión como en la "
        "práctica de la semana) y que revisara que el notebook corriera de punta "
        "a punta. Corregí el texto, ejecuté el notebook y contrasté los resultados "
        "con lo que ya había observado en entregas anteriores antes de darlo por "
        "cerrado.",
    )
    pdf.ln(3)

    body(pdf, "2. Declaración de responsabilidad académica", size=12, bold=True, lh=6.5)
    body(
        pdf,
        "Quienes integramos el equipo declaramos que revisamos los datos, las consultas "
        "SQL, el código en Python, las visualizaciones, los resultados, los modelos "
        "y las interpretaciones presentadas; que podemos explicar y fundamentar los "
        "procedimientos, decisiones y conclusiones del trabajo; y que asumimos la "
        "responsabilidad académica por la totalidad de la entrega, independientemente "
        "de las herramientas empleadas durante su elaboración.",
    )
    check(
        pdf,
        True,
        "El equipo confirma que la información consignada en esta declaración es "
        "completa y refleja el uso realizado de herramientas de IA generativa.",
    )
    pdf.ln(8)

    body(pdf, "Firma y aclaración", size=11, bold=True, lh=6)
    pdf.ln(8)
    body(pdf, "________________________________")
    body(pdf, "Viruel, Nicolás")
    body(pdf, "Comisión 10 - Grupo J - 19/10/2026")

    pdf.output(str(OUT))
    print(f"Escrito: {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
