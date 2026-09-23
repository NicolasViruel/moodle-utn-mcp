#!/usr/bin/env sh
# Pre-commit local — formatter, linter, tests (TP3 laboratorio)
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/tp2-testing-contratos" || exit 1

echo "==> [1/3] Formatter (ruff format --check)"
python -m ruff format --check pedidos_descuento.py test_pedidos_descuento.py

echo "==> [2/3] Linter (ruff check)"
python -m ruff check pedidos_descuento.py test_pedidos_descuento.py

echo "==> [3/3] Unit tests"
python -m unittest test_pedidos_descuento.py -v

echo "Pre-commit OK: todos los controles pasaron."
