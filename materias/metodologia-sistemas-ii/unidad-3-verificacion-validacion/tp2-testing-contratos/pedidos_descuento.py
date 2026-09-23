"""Lógica de descuento de envío — módulo de laboratorio (TP2)."""

from __future__ import annotations


def calcular_descuento_envio(
    peso_kg: float,
    es_cliente_premium: bool,
    cupon_activo: bool,
) -> float:
    """
    Retorna el monto de descuento en pesos sobre el costo base de envío.

    Ramas pensadas para ejercicio de cobertura de branches (TP2 ítem 3).
    """
    if peso_kg <= 0:
        raise ValueError("El peso debe ser mayor a cero")

    if es_cliente_premium:
        if cupon_activo:
            return 0.0
        return 5.0

    if peso_kg > 30:
        return 15.0

    if cupon_activo:
        return 10.0

    return 12.0
