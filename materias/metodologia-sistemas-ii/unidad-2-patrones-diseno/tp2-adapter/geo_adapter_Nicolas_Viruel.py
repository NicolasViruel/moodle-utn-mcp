"""
TP2 – Adapter | Metodología de Sistemas II
Alumno: Nicolás Viruel

Único archivo nuevo permitido: GeoServiceAdapter.
OldGeoService, NewGeoProvider y el cliente no se modifican.

Si llega un tercer proveedor (FutureGeoProvider):
  solo hay que crear FutureGeoAdapter con la misma interfaz OldGeoService
  y cambiar la línea de inyección geo = GeoServiceAdapter() por el nuevo adapter.
  Los 40 archivos cliente siguen igual.
"""

from __future__ import annotations

from dataclasses import dataclass


# --- API vieja: no se modifica ---
class OldGeoService:
    def get_location(self, ip: str) -> dict[str, float | str]:
        return {
            "lat": -34.6037,
            "lng": -58.3816,
            "city": "Buenos Aires (legacy)",
            "country": "AR",
        }


# --- Proveedor nuevo: no se modifica ---
@dataclass
class Coordinates:
    latitude: float
    longitude: float


@dataclass
class Address:
    locality: str
    nation: str


@dataclass
class LocateResult:
    coordinates: Coordinates
    address: Address


class NewGeoProvider:
    def locate(self, ip: str) -> LocateResult:
        return LocateResult(
            coordinates=Coordinates(latitude=-34.6037, longitude=-58.3816),
            address=Address(locality="Buenos Aires", nation="Argentina"),
        )


# --- Único archivo nuevo: Adapter ---
class GeoServiceAdapter(OldGeoService):
    def __init__(self) -> None:
        self._provider = NewGeoProvider()

    def get_location(self, ip: str) -> dict[str, float | str]:
        result = self._provider.locate(ip)
        return {
            "lat": result.coordinates.latitude,
            "lng": result.coordinates.longitude,
            "city": result.address.locality,
            "country": result.address.nation,
        }


# --- Cliente del sistema (40 archivos): no se modifica ---
def cliente_sistema(geo: OldGeoService, ip: str) -> None:
    data = geo.get_location(ip)
    print(f"{data['city']}, lat={data['lat']}")


if __name__ == "__main__":
    ip = "200.45.123.10"

    print("ANTES:")
    cliente_sistema(OldGeoService(), ip)

    print("\nDESPUÉS (único cambio: instanciar el adapter):")
    cliente_sistema(GeoServiceAdapter(), ip)
