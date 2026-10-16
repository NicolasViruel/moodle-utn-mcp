"""Repository Pattern: acceso a colecciones en memoria, sin lógica de negocio."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Generic, TypeVar

T = TypeVar("T")


class InMemoryRepository(Generic[T]):
    def __init__(self, store: list[T], id_attr: str = "id") -> None:
        self._store = store
        self._id_attr = id_attr

    def list(self, predicate: Callable[[T], bool] | None = None) -> list[T]:
        rows = list(self._store)
        if predicate is None:
            return rows
        return [row for row in rows if predicate(row)]

    def get(self, item_id: int) -> T | None:
        for row in self._store:
            if getattr(row, self._id_attr, None) == item_id:
                return row
        return None

    def add(self, row: T) -> T:
        self._store.append(row)
        return row

    def remove(self, row: T) -> None:
        self._store.remove(row)

    def replace_where(self, keep: Callable[[T], bool]) -> None:
        self._store[:] = [row for row in self._store if keep(row)]

    def all(self) -> Iterable[T]:
        return tuple(self._store)
