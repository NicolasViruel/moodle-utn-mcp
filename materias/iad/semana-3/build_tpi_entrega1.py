import json
from pathlib import Path

cells = []

def md(source):
    cells.append({"cell_type": "markdown", "metadata": {}, "source": source})

def code(source):
    cells.append({"cell_type": "code", "metadata": {}, "source": source, "outputs": [], "execution_count": None})

md([
    "# Trabajo Práctico Integrador – Entrega 1\n",
    "\n",
    "**Materia:** Introducción al Análisis de Datos  \n",
    "**Tema:** Cancelación de reservas hoteleras  \n",
    "**Comisión:** 10 (Grupo J)  \n",
    "**Integrante:** Nicolás Viruel  \n",
    "**Entrega:** 1 – Unidad N° 1  \n",
    "**Año:** 2026\n",
])

md([
    "## 1. Presentación del problema\n",
    "\n",
    "El hotel necesita entender **por qué se cancelan las reservas** antes del check-in. Cada registro del dataset representa una reserva con características como tipo de hotel, anticipación (`lead_time`), canal de distribución, tipo de depósito y la variable objetivo `is_canceled`.\n",
    "\n",
    "Desde el ciclo de vida del análisis, estamos en una **fase inicial de comprensión y exploración**: todavía no modelamos ni predecimos, pero sí convertimos datos crudos en **información** (estructura, conteos, promedios) que después puede convertirse en **conocimiento** si se interpreta en contexto.\n",
    "\n",
    "**Variable objetivo:** `is_canceled` (0 = no cancelada, 1 = cancelada).\n",
    "\n",
    "**Preguntas que orientan este primer avance:**\n",
    "1. ¿Qué porcentaje de reservas se cancela?\n",
    "2. ¿Qué variables numéricas y categóricas tenemos disponibles?\n",
    "3. ¿Cómo se distribuyen los tipos de hotel y los canales de reserva?\n",
    "4. ¿Qué rangos presentan variables como `lead_time` o `adr`?\n",
])

md([
    "## 2. Dataset asignado\n",
    "\n",
    "- **Comisión:** 10  \n",
    "- **Archivo:** `hotel_booking_TPI_grupo_J.csv`  \n",
    "- **Origen:** subset asignado por la cátedra (Hotel Booking Demand)\n",
    "\n",
    "> Subí el CSV en la misma carpeta que este notebook (Colab/Drive) antes de ejecutar la carga.\n",
])

code([
    "import pandas as pd\n",
    "\n",
    "archivo = \"hotel_booking_TPI_grupo_J.csv\"\n",
    "df = pd.read_csv(archivo)\n",
    "print(\"Dataset cargado:\", archivo)\n",
])

md(["## 3. Vista inicial del dataset"])

code(["df.head()"])

md(["## 4. Estructura general"])

code([
    "filas, columnas = df.shape\n",
    "print(f\"Filas (reservas): {filas}\")\n",
    "print(f\"Columnas (variables): {columnas}\")\n",
    "print(\"\\nNombres de columnas:\")\n",
    "print(df.columns.tolist())\n",
])

md(["## 5. Tipos de datos"])

code([
    "print(df.dtypes)\n",
    "print(\"\\n--- info() ---\")\n",
    "df.info()\n",
])

md([
    "## 6. Clasificación inicial de variables\n",
    "\n",
    "Clasificación manual según el dominio del problema:\n",
])

code([
    "numericas = [\n",
    "    \"is_canceled\", \"lead_time\", \"arrival_date_year\", \"arrival_date_week_number\",\n",
    "    \"arrival_date_day_of_month\", \"stays_in_weekend_nights\", \"stays_in_week_nights\",\n",
    "    \"adults\", \"children\", \"babies\", \"previous_cancellations\",\n",
    "    \"previous_bookings_not_canceled\", \"booking_changes\", \"days_in_waiting_list\",\n",
    "    \"adr\", \"required_car_parking_spaces\", \"total_of_special_requests\",\n",
    "]\n",
    "categoricas = [\n",
    "    \"booking_id\", \"hotel\", \"arrival_date_month\", \"arrival_date\", \"meal\", \"country\",\n",
    "    \"market_segment\", \"distribution_channel\", \"reserved_room_type\", \"assigned_room_type\",\n",
    "    \"deposit_type\", \"customer_type\",\n",
    "]\n",
    "temporales = [\"arrival_date_year\", \"arrival_date_month\", \"arrival_date\", \"arrival_date_week_number\", \"arrival_date_day_of_month\"]\n",
    "\n",
    "print(\"Numéricas:\", len(numericas))\n",
    "print(\"Categóricas:\", len(categoricas))\n",
    "print(\"Temporales (también presentes en el dataset):\", temporales)\n",
])

md(["## 7. Caracterización descriptiva inicial"])

code([
    "df.describe().round(2)\n",
])

code([
    "print(\"Distribución de la variable objetivo:\")\n",
    "print(df[\"is_canceled\"].value_counts())\n",
    "print(f\"\\nPorcentaje de cancelaciones: {df['is_canceled'].mean() * 100:.2f}%\")\n",
])

code([
    "print(\"Tipo de hotel:\")\n",
    "print(df[\"hotel\"].value_counts())\n",
    "\n",
    "print(\"\\nCanal de distribución:\")\n",
    "print(df[\"distribution_channel\"].value_counts().head())\n",
])

md([
    "## 8. Primeras observaciones\n",
    "\n",
    "- El dataset tiene **25.000 reservas** y **32 variables**, lo que permite un análisis exploratorio inicial amplio.\n",
    "- Aproximadamente **37%** de las reservas están canceladas (`is_canceled = 1`), un nivel relevante para el negocio.\n",
    "- Hay dos tipos de hotel (**City Hotel** y **Resort Hotel**); conviene comparar cancelaciones entre ambos en entregas futuras.\n",
    "- `lead_time` varía desde reservas de último momento hasta más de 600 días de anticipación; la media ronda los 100 días (según `describe()`).\n",
    "- Variables como `agent` y `company` tienen muchos valores faltantes (se observa en `info()`), lo que limitará su uso directo sin tratamiento posterior.\n",
])

md([
    "## 9. Consideraciones éticas iniciales\n",
    "\n",
    "- Los datos corresponden a reservas reales anonimizadas; no deben usarse para identificar huéspedes ni compartirse fuera del ámbito académico.\n",
    "- En esta etapa **no afirmo causas** (por ejemplo, que un canal \"provoca\" cancelaciones): solo describo patrones que después deberán validarse con más análisis.\n",
    "- Cualquier recomendación al hotel debería basarse en evidencia acumulada y considerar el impacto en clientes (políticas de depósito, sobreventa, etc.).\n",
])

nb = {
    "nbformat": 4,
    "nbformat_minor": 0,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11.0"},
    },
    "cells": cells,
}

out = Path("materias/iad/semana-3/notebooks/TPI_Entrega1_Nicolas_Viruel.ipynb")
out.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
print("Wrote", out)
