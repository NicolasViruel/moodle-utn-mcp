"""Pruebas unitarias con patrón AAA — TP2 Metodología II U3."""

from __future__ import annotations

import unittest

from pedidos_descuento import calcular_descuento_envio


class TestCalcularDescuentoEnvioAAA(unittest.TestCase):
    """Cada test separa explícitamente Arrange, Act y Assert."""

    def test_premium_con_cupon_envio_gratis(self) -> None:
        # Arrange
        peso = 2.5
        premium = True
        cupon = True

        # Act
        descuento = calcular_descuento_envio(peso, premium, cupon)

        # Assert
        self.assertEqual(descuento, 0.0)

    def test_premium_sin_cupon_descuento_fijo(self) -> None:
        # Arrange
        peso = 8.0
        premium = True
        cupon = False

        # Act
        descuento = calcular_descuento_envio(peso, premium, cupon)

        # Assert
        self.assertEqual(descuento, 5.0)

    def test_no_premium_peso_alto(self) -> None:
        # Arrange
        peso = 35.0
        premium = False
        cupon = False

        # Act
        descuento = calcular_descuento_envio(peso, premium, cupon)

        # Assert
        self.assertEqual(descuento, 15.0)

    def test_no_premium_cupon_estandar(self) -> None:
        # Arrange
        peso = 10.0
        premium = False
        cupon = True

        # Act
        descuento = calcular_descuento_envio(peso, premium, cupon)

        # Assert
        self.assertEqual(descuento, 10.0)

    def test_no_premium_sin_cupon_tarifa_default(self) -> None:
        # Arrange
        peso = 10.0
        premium = False
        cupon = False

        # Act
        descuento = calcular_descuento_envio(peso, premium, cupon)

        # Assert
        self.assertEqual(descuento, 12.0)

    def test_peso_invalido_lanza_error(self) -> None:
        # Arrange
        peso = 0.0
        premium = False
        cupon = False

        # Act / Assert
        with self.assertRaises(ValueError):
            calcular_descuento_envio(peso, premium, cupon)


if __name__ == "__main__":
    unittest.main()
