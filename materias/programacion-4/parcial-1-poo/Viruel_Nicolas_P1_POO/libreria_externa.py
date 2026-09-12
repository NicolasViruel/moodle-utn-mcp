"""Ficha del sistema de caja de un tercero. NO SE MODIFICA."""


class FichaPuntoDeVenta:
    """Ficha que genera el sistema de caja de un tercero."""

    def __init__(self, codigo: str, detalle: str) -> None:
        self._codigo = codigo
        self._detalle = detalle

    def exportar(self) -> str:
        return f"POS|{self._codigo}|{self._detalle}"
