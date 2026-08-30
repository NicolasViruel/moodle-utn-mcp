"""Sincroniza TPI_Maestro con contenido de Entrega 1 y Entrega 2."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "notebooks" / "TPI_Maestro_Nicolas_Viruel.ipynb"


def md(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": text}


def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "metadata": {},
        "source": text,
        "outputs": [],
        "execution_count": None,
    }


cells = [
    md(
        "# TPI – Notebook Maestro\n\n"
        "## Análisis de cancelaciones de reservas hoteleras\n\n"
        "**Materia:** Introducción al Análisis de Datos  \n"
        "**Comisión:** 10 (Grupo J)  \n"
        "**Integrante:** Nicolás Viruel  \n"
        "**Año:** 2026\n\n"
        "> Documento integrador del TPI. Secciones 1–4 sincronizadas con Entregas 1 y 2 (Semanas 3–4)."
    ),
    md(
        "# 1. Definición del problema\n\n"
        "El problema consiste en analizar las **cancelaciones de reservas hoteleras** antes del check-in.\n\n"
        "Las cancelaciones afectan la planificación de ocupación, disponibilidad de habitaciones e ingresos. "
        "El objetivo es identificar qué características de las reservas se relacionan con la cancelación.\n\n"
        "**Variable objetivo:** `is_canceled` (0 = no cancelada, 1 = cancelada)."
    ),
    md(
        "# 2. Preguntas de análisis\n\n"
        "1. ¿Qué **porcentaje** de reservas se cancela en el dataset?\n"
        "2. ¿Las cancelaciones varían según el **tipo de depósito**, **canal de reserva** o **anticipación** (`lead_time`)?\n"
        "3. ¿Hay diferencias por **temporada**, **tipo de habitación** o **país** del cliente?\n"
        "4. ¿Clientes **repetidos** cancelan menos que clientes nuevos?\n"
        "5. ¿Qué variables parecen más relacionadas con `is_canceled` en una primera exploración?\n"
        "6. ¿Qué decisiones concretas podría tomar el hotel si confirma ciertos patrones?"
    ),
    md(
        "# 3. Descripción del dataset\n\n"
        "- **Archivo:** `hotel_booking_TPI_grupo_J.csv` (Comisión 10, Grupo J)\n"
        "- **Origen:** subset asignado por la cátedra (Hotel Booking Demand)\n"
        "- **Unidad:** Entrega 1 – caracterización descriptiva inicial"
    ),
    code(
        "import pandas as pd\n"
        "import numpy as np\n"
        "from pathlib import Path\n"
        "\n"
        "DATA_DIR = Path('../datos')\n"
        "archivo = DATA_DIR / 'hotel_booking_TPI_grupo_J.csv'\n"
        "df_hotel = pd.read_csv(archivo)\n"
        "print('Dataset cargado:', df_hotel.shape)"
    ),
    code("df_hotel.head()"),
    code(
        "filas, columnas = df_hotel.shape\n"
        "print(f'Filas (reservas): {filas}')\n"
        "print(f'Columnas (variables): {columnas}')\n"
        "print('\\nColumnas:', df_hotel.columns.tolist())"
    ),
    code(
        "print(df_hotel.dtypes)\n"
        "print('\\n--- info() ---')\n"
        "df_hotel.info()"
    ),
    code(
        "numericas = [\n"
        "    'is_canceled', 'lead_time', 'arrival_date_year', 'arrival_date_week_number',\n"
        "    'arrival_date_day_of_month', 'stays_in_weekend_nights', 'stays_in_week_nights',\n"
        "    'adults', 'children', 'babies', 'previous_cancellations',\n"
        "    'previous_bookings_not_canceled', 'booking_changes', 'days_in_waiting_list',\n"
        "    'adr', 'required_car_parking_spaces', 'total_of_special_requests',\n"
        "]\n"
        "categoricas = [\n"
        "    'booking_id', 'hotel', 'arrival_date_month', 'arrival_date', 'meal', 'country',\n"
        "    'market_segment', 'distribution_channel', 'reserved_room_type', 'assigned_room_type',\n"
        "    'deposit_type', 'customer_type',\n"
        "]\n"
        "print('Numéricas:', len(numericas), '| Categóricas:', len(categoricas))"
    ),
    code("df_hotel.describe().round(2)"),
    code(
        "print('Distribución is_canceled:')\n"
        "print(df_hotel['is_canceled'].value_counts())\n"
        "print(f\"\\nPorcentaje cancelaciones: {df_hotel['is_canceled'].mean() * 100:.2f}%\")\n"
        "print('\\nTipo de hotel:')\n"
        "print(df_hotel['hotel'].value_counts())\n"
        "print('\\nCanal de distribución:')\n"
        "print(df_hotel['distribution_channel'].value_counts().head())"
    ),
    md(
        "### Observaciones iniciales (Entrega 1)\n\n"
        "- **25.000 reservas** × **32 variables**.\n"
        "- ~**37%** de cancelaciones; nivel relevante para el negocio.\n"
        "- Predominan reservas en **City Hotel** y canal **TA/TO**.\n"
        "- `agent` y `company` presentan muchos faltantes (se documentan en la limpieza)."
    ),
    md(
        "# 4. Preparación y limpieza de datos\n\n"
        "**Unidad:** Entrega 2 – diagnóstico y limpieza inicial (Semana 4).\n\n"
        "Se conserva el dataset original y se trabaja sobre una copia. Cada decisión queda registrada en la bitácora."
    ),
    code(
        "df_hotel_original = df_hotel.copy()\n"
        "df = df_hotel.copy()\n"
        "\n"
        "registros_bitacora = []\n"
        "\n"
        "def registrar(problema, variable, decision, justificacion):\n"
        "    registros_bitacora.append({\n"
        "        'problema_detectado': problema,\n"
        "        'variable': variable,\n"
        "        'decision': decision,\n"
        "        'justificacion': justificacion,\n"
        "    })"
    ),
    code(
        "print('Dimensiones:', df.shape)\n"
        "print('Duplicados exactos:', df.duplicated().sum())\n"
        "cols_sugeridas = [\n"
        "    'children', 'adults', 'babies', 'stays_in_weekend_nights',\n"
        "    'stays_in_week_nights', 'adr', 'lead_time', 'country', 'agent', 'company',\n"
        "]\n"
        "df[cols_sugeridas].describe(include='all').T"
    ),
    code(
        "nulos = df.isna().sum().sort_values(ascending=False)\n"
        "print(nulos[nulos > 0])\n"
        "\n"
        "registrar('Alta proporción de company nulo', 'company', 'Conservar NaN',\n"
        "          '94% sin empresa; patrón real, no error masivo.')\n"
        "registrar('Agent nulo en ~14%', 'agent', 'Conservar NaN',\n"
        "          'Reservas directas o sin intermediario.')\n"
        "registrar('Country ausente en 117 reservas', 'country', 'Conservar NaN',\n"
        "          'Menos del 0,5% del total; eliminar sesgaría países minoritarios.')"
    ),
    code(
        "print('adr <= 0:', (df['adr'] <= 0).sum())\n"
        "print('adults == 0:', (df['adults'] == 0).sum())\n"
        "print('Sin huéspedes:', ((df['adults'] + df['children'] + df['babies']) == 0).sum())\n"
        "\n"
        "registrar('adr nulo, cero o negativo', 'adr', 'Marcar; conservar por ahora',\n"
        "          'Puede ser cortesía o error; no eliminar sin contexto de negocio.')\n"
        "registrar('adults == 0', 'adults', 'Conservar y analizar',\n"
        "          'Posible error o reserva especial.')\n"
        "if ((df['adults'] + df['children'] + df['babies']) == 0).any():\n"
        "    registrar('Estadía sin huéspedes', 'adults, children, babies',\n"
        "              'Conservar para revisión', 'Combinación atípica en operación normal.')"
    ),
    code(
        "def detectar_outliers_iqr(serie):\n"
        "    s = serie.dropna()\n"
        "    q1, q3 = s.quantile(0.25), s.quantile(0.75)\n"
        "    iqr = q3 - q1\n"
        "    lim_inf, lim_sup = q1 - 1.5 * iqr, q3 + 1.5 * iqr\n"
        "    return s[(s < lim_inf) | (s > lim_sup)]\n"
        "\n"
        "for col in ['lead_time', 'adr', 'stays_in_week_nights', 'stays_in_weekend_nights']:\n"
        "    out = detectar_outliers_iqr(df[col])\n"
        "    print(f'{col}: {len(out)} atípicos IQR')\n"
        "\n"
        "registrar('lead_time muy alto', 'lead_time', 'Conservar',\n"
        "          'Anticipación extrema posible en resorts.')\n"
        "registrar('adr atípico por IQR', 'adr', 'Conservar',\n"
        "          'Tarifas premium válidas; evaluar en EDA.')"
    ),
    code(
        "df['arrival_date'] = pd.to_datetime(df['arrival_date'], errors='coerce')\n"
        "print('Fechas inválidas:', df['arrival_date'].isna().sum())\n"
        "print('Rango:', df['arrival_date'].min(), '→', df['arrival_date'].max())\n"
        "registrar('Unificación arrival_date', 'arrival_date', 'Convertir a datetime',\n"
        "          'Coherencia temporal; sin fechas inválidas detectadas.')"
    ),
    code(
        "bitacora = pd.DataFrame(registros_bitacora)\n"
        "bitacora"
    ),
    code(
        "df_hotel_limpio = df.copy()\n"
        "print('Original:', df_hotel_original.shape, '| Limpio:', df_hotel_limpio.shape)\n"
        "df_hotel_limpio[cols_sugeridas].head()"
    ),
    md(
        "### Cierre limpieza (Semana 4)\n\n"
        "Diagnóstico inicial completado: faltantes documentados, valores imposibles identificados "
        "y atípicos analizados con IQR **sin eliminación automática**. "
        "Transformaciones adicionales se completarán en Semana 5 (Entrega 2 formal)."
    ),
    md(
        "# 5. Análisis exploratorio de datos\n\n"
        "*Pendiente – Semana 5 en adelante.*\n\n"
        "Visualizaciones, tablas cruzadas y comparaciones por `hotel`, `deposit_type`, "
        "`lead_time`, `country`, etc."
    ),
    md(
        "# 6. Análisis de la variable objetivo: is_canceled\n\n"
        "La variable objetivo es **`is_canceled`**:\n\n"
        "- `0`: reserva no cancelada\n"
        "- `1`: reserva cancelada\n\n"
        "En la caracterización inicial (Sección 3) se observó ~37% de cancelaciones. "
        "En entregas futuras se profundizará qué variables se asocian con cada valor."
    ),
    code(
        "pct_cancel = df_hotel['is_canceled'].mean() * 100\n"
        "print(f'Cancelaciones: {pct_cancel:.2f}%')\n"
        "df_hotel.groupby('hotel')['is_canceled'].mean().mul(100).round(2)"
    ),
    md(
        "# 7. Modelado\n\n"
        "*Pendiente – unidades posteriores.*\n\n"
        "Modelo de clasificación, partición train/test, métricas (accuracy, precision, recall, F1)."
    ),
    md(
        "# 8. Resultados y conclusiones\n\n"
        "*Pendiente – entrega final.*\n\n"
        "Conclusiones vinculadas a las preguntas de la Sección 2, limitaciones y recomendaciones al hotel."
    ),
]

nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3"},
    },
    "cells": cells,
}

OUT.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"Sincronizado: {OUT}")
