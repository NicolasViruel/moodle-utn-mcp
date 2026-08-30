"""
TP3 – Observer | Metodología de Sistemas II
Alumno: Nicolás Viruel

Justificación: InventoryManager dejó de conocer servicios concretos.
Solo mantiene suscriptores de StockObserver y notifica con notify().
El try/except está DENTRO del loop para que un observer roto no detenga a los demás.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class StockObserver(ABC):
    @abstractmethod
    def on_low_stock(self, product_id: str, quantity: int) -> None: ...


class EmailAlertObserver(StockObserver):
    def on_low_stock(self, product_id: str, quantity: int) -> None:
        print(f"[EMAIL] Stock bajo: {product_id} (qty={quantity})")


class AnalyticsObserver(StockObserver):
    def on_low_stock(self, product_id: str, quantity: int) -> None:
        print(f"[ANALYTICS] Evento registrado: {product_id}")


class ReplenishObserver(StockObserver):
    def on_low_stock(self, product_id: str, quantity: int) -> None:
        print(f"[REPLENISH] Orden automática x100 para {product_id}")


class PushNotificationObserver(StockObserver):
    """Observador nuevo agregado sin tocar InventoryManager."""

    def on_low_stock(self, product_id: str, quantity: int) -> None:
        print(f"[PUSH] Alerta móvil: {product_id} quedó en {quantity}")


class BrokenObserver(StockObserver):
    def on_low_stock(self, product_id: str, quantity: int) -> None:
        raise RuntimeError("error de red simulado")


class InventoryManager:
    def __init__(self) -> None:
        self._stock: dict[str, int] = {}
        self._observers: list[StockObserver] = []
        self._errors: list[str] = []

    def subscribe(self, observer: StockObserver) -> None:
        self._observers.append(observer)

    def unsubscribe(self, observer: StockObserver) -> None:
        self._observers.remove(observer)

    def _notify(self, product_id: str, quantity: int) -> None:
        for observer in self._observers:
            try:
                observer.on_low_stock(product_id, quantity)
            except Exception as exc:  # noqa: BLE001 — consigna pide continuar la cadena
                msg = f"Observer {observer.__class__.__name__} falló: {exc}"
                self._errors.append(msg)
                print(f"[ERROR registrado] {msg}")

    def update_stock(self, product_id: str, quantity: int) -> None:
        self._stock[product_id] = quantity
        if quantity < 10:
            self._notify(product_id, quantity)

    def sell_product(self, product_id: str, sold: int) -> None:
        self._stock[product_id] = self._stock.get(product_id, 0) - sold
        if self._stock[product_id] < 10:
            self._notify(product_id, self._stock[product_id])


# --- Código ANTES (referencia consigna) ---
# class InventoryManager:
#     def __init__(self):
#         self.emailService = EmailAlertService()
#         self.analytics = AnalyticsDashboard()
#         ...


if __name__ == "__main__":
    manager = InventoryManager()
    manager.subscribe(EmailAlertObserver())
    manager.subscribe(AnalyticsObserver())
    manager.subscribe(BrokenObserver())
    manager.subscribe(ReplenishObserver())
    manager.subscribe(PushNotificationObserver())

    print("=== update_stock('PROD-001', 5) ===")
    manager.update_stock("PROD-001", 5)
    print("\nErrores aislados:", manager._errors)
