"""
TP1 – Factory Method | Metodología de Sistemas II
Alumno: Nicolás Viruel

Variante elegida: Static Factory (Simple Factory) en ReportFactory.create().
Justificación Factory Method vs Abstract Factory:
  Solo existe un tipo de producto (Report) con variantes por formato.
  Abstract Factory tendría sentido si debiéramos crear familias coordinadas
  (p. ej. Report + Exporter + Template del mismo “tema”). Acá no hay familias
  relacionadas, por eso centralizar la decisión en un factory estático alcanza.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date


class Report(ABC):
    @abstractmethod
    def set_data(self, data: list[dict]) -> None: ...

    @abstractmethod
    def add_header(self, text: str) -> None: ...

    @abstractmethod
    def add_footer(self, text: str) -> None: ...

    @abstractmethod
    def render(self) -> None: ...

    @abstractmethod
    def get_output(self) -> str: ...


class _BaseReport(Report):
    def __init__(self, tag: str) -> None:
        self._tag = tag
        self._data: list[dict] = []
        self._header = ""
        self._footer = ""
        self._rendered = False

    def set_data(self, data: list[dict]) -> None:
        self._data = data

    def add_header(self, text: str) -> None:
        self._header = text

    def add_footer(self, text: str) -> None:
        self._footer = text

    def render(self) -> None:
        self._rendered = True

    def get_output(self) -> str:
        if not self._rendered:
            raise RuntimeError("Debe llamar a render() antes de get_output()")
        body = ", ".join(str(row) for row in self._data)
        return f"[{self._tag}] {self._header} | {body} | {self._footer}"


class PDFReport(_BaseReport):
    def __init__(self) -> None:
        super().__init__("PDF")


class ExcelReport(_BaseReport):
    def __init__(self) -> None:
        super().__init__("EXCEL")


class CSVReport(_BaseReport):
    def __init__(self) -> None:
        super().__init__("CSV")


class HTMLReport(_BaseReport):
    """Nuevo formato agregado sin modificar ReportService."""

    def __init__(self) -> None:
        super().__init__("HTML")


class ReportFactory:
    @staticmethod
    def create(format_type: str) -> Report:
        match format_type.lower():
            case "pdf":
                return PDFReport()
            case "excel":
                return ExcelReport()
            case "csv":
                return CSVReport()
            case "html":
                return HTMLReport()
            case _:
                raise ValueError(f"Formato no soportado: {format_type}")


class ReportService:
    def generate(self, data: list[dict], format_type: str) -> str:
        report = ReportFactory.create(format_type)
        report.set_data(data)
        report.add_header("Reporte Mensual")
        report.add_footer(f"Generado el {date.today().isoformat()}")
        report.render()
        return report.get_output()


# --- Código ANTES (problemático, referencia de la consigna) ---
# class ReportService:
#     def generate(self, data, format_type):
#         if format_type == "pdf":
#             report = PDFReport()
#         elif format_type == "excel":
#             report = ExcelReport()
#         elif format_type == "csv":
#             report = CSVReport()
#         else:
#             raise ValueError("Formato no soportado")
#         report.set_data(data)
#         ...


if __name__ == "__main__":
    datos = [{"producto": "A", "ventas": 120}, {"producto": "B", "ventas": 85}]
    servicio = ReportService()
    for fmt in ("pdf", "excel", "csv", "html"):
        print(servicio.generate(datos, fmt))
