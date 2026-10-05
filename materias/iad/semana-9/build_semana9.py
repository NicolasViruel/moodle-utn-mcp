"""Genera TPI Entrega 4 (EDA) – Semanas 9 y 10 · IAD."""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NB_DIR = ROOT / "notebooks"
DATA_DIR = ROOT / "datos"
HOTEL_SRC = ROOT.parent / "semana-6" / "datos" / "hotel_booking_TPI_grupo_J.csv"


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


def write_nb(path: Path, cells: list) -> None:
    nb = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3"},
        },
        "cells": cells,
    }
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Escrito: {path}")


def build_tpi_entrega4() -> None:
    cells: list = []

    def add_md(t: str) -> None:
        cells.append(md(t))

    def add_code(t: str) -> None:
        cells.append(code(t))

    add_md(
        "# Trabajo Práctico Integrador – Entrega 4\n\n"
        "**Materia:** Introducción al Análisis de Datos  \n"
        "**Tema:** Cancelación de reservas hoteleras  \n"
        "**Comisión:** 10 (Grupo J)  \n"
        "**Integrante:** Viruel, Nicolás  \n"
        "**Entrega:** 4 – Unidad N° 4 · Análisis exploratorio de datos  \n"
        "**Recorrido:** SQL (DuckDB) + Python  \n"
        "**Dataset:** `hotel_booking_TPI_grupo_J.csv`  \n"
        "**Variable objetivo:** `is_canceled`  \n"
        "**Año:** 2026\n\n"
        "> Notebook **independiente y reproducible** desde cero. "
        "Las secciones 1–7 corresponden al avance de la Semana 9; "
        "las secciones 8–9 cierran el EDA comparativo (Semana 10) para la entrega en Moodle."
    )

    add_md(
        "## 1. Contexto del análisis exploratorio\n\n"
        "El hotel necesita comprender **patrones en las reservas** antes de modelar o predecir cancelaciones. "
        "En esta entrega aplicamos un **EDA sistemático**: reconocimiento del dataset, descripción univariada "
        "y, en la etapa final, **comparación entre reservas canceladas y no canceladas** con conclusiones "
        "fundamentadas en evidencia."
    )

    add_md("## 2. Entorno, carga del dataset y registro en DuckDB")

    add_code(
        "import duckdb\n"
        "import pandas as pd\n"
        "import numpy as np\n"
        "import matplotlib.pyplot as plt\n"
        "import seaborn as sns\n"
        "from pathlib import Path\n"
        "\n"
        "sns.set_theme(style='whitegrid', palette='colorblind')\n"
        "plt.rcParams['figure.figsize'] = (9, 5)\n"
        "plt.rcParams['figure.dpi'] = 100\n"
        "\n"
        "DATA_DIR = Path('../datos')\n"
        "CSV_PATH = DATA_DIR / 'hotel_booking_TPI_grupo_J.csv'\n"
        "\n"
        "con = duckdb.connect(database=':memory:')\n"
        "con.execute(\n"
        "    \"\"\"\n"
        "    CREATE OR REPLACE TABLE reservas AS\n"
        "    SELECT * FROM read_csv_auto(?, header=true)\n"
        "    \"\"\",\n"
        "    [str(CSV_PATH.resolve())],\n"
        ")\n"
        "n_filas = con.execute('SELECT COUNT(*) FROM reservas').fetchone()[0]\n"
        "print(f'Filas cargadas en DuckDB: {n_filas}')"
    )

    add_md(
        "## 3. Unidad de análisis y variable objetivo\n\n"
        "- **Unidad de análisis:** cada **fila** representa una **reserva hotelera** (una solicitud de estadía).\n"
        "- **`is_canceled`:** `0` = la reserva **no** fue cancelada; `1` = **fue cancelada** antes del check-in.\n"
        "- El resto del TPI estudia qué características de la reserva se asocian con `is_canceled = 1`."
    )

    add_code(
        "con.execute(\n"
        "    \"\"\"\n"
        "    SELECT is_canceled, COUNT(*) AS reservas\n"
        "    FROM reservas\n"
        "    GROUP BY is_canceled\n"
        "    ORDER BY is_canceled\n"
        "    \"\"\"\n"
        ").df()"
    )

    add_md("## 4. Estructura del dataset (SQL)")

    add_code(
        "con.execute('DESCRIBE reservas').df()"
    )

    add_code(
        "con.execute(\n"
        "    \"\"\"\n"
        "    SELECT column_name, column_type\n"
        "    FROM (DESCRIBE reservas)\n"
        "    ORDER BY column_name\n"
        "    \"\"\"\n"
        ").df()"
    )

    add_code(
        "con.execute('SELECT * FROM reservas LIMIT 5').df()"
    )

    add_md(
        "## 5. Preparación mínima reproducible (Python)\n\n"
        "Reconstruimos variables derivadas usadas en entregas anteriores, **dentro de este notebook**, "
        "sin depender de otros archivos ejecutados previamente."
    )

    add_code(
        "df = con.execute('SELECT * FROM reservas').df()\n"
        "\n"
        "df['children'] = df['children'].fillna(0)\n"
        "df['arrival_date'] = pd.to_datetime(df['arrival_date'], errors='coerce')\n"
        "df['total_nights'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']\n"
        "df['total_guests'] = df['adults'] + df['children'] + df['babies']\n"
        "df['is_canceled_label'] = df['is_canceled'].map({0: 'No cancelada', 1: 'Cancelada'})\n"
        "\n"
        "con.register('reservas_prep', df)\n"
        "print('Columnas:', df.shape[1], '| Filas:', df.shape[0])"
    )

    add_md(
        "## 6. Variables seleccionadas para el EDA\n\n"
        "Para esta etapa exploratoria se priorizan:\n\n"
        "| Variable | Tipo | Motivo |\n"
        "|----------|------|--------|\n"
        "| `is_canceled` | Binaria | Objetivo del TPI |\n"
        "| `lead_time` | Numérica | Anticipación de la reserva |\n"
        "| `hotel` | Categórica | Tipo de establecimiento |\n"
        "| `market_segment` | Categórica | Canal / segmento comercial |\n"
        "| `deposit_type` | Categórica | Política de depósito |\n"
        "| `total_nights` | Numérica derivada | Duración de la estadía |"
    )

    add_md(
        "### 6.1 Distribución de `is_canceled` (Semana 9)\n\n"
        "**Pregunta:** ¿Con qué frecuencia aparecen cancelaciones en el dataset?\n\n"
        "Solo se describe la variable objetivo; aún no se comparan otras dimensiones."
    )

    add_code(
        "tab_cancel = con.execute(\n"
        "    \"\"\"\n"
        "    SELECT\n"
        "        is_canceled,\n"
        "        COUNT(*) AS n,\n"
        "        ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct\n"
        "    FROM reservas_prep\n"
        "    GROUP BY is_canceled\n"
        "    ORDER BY is_canceled\n"
        "    \"\"\"\n"
        ").df()\n"
        "tab_cancel"
    )

    add_code(
        "fig, ax = plt.subplots()\n"
        "sns.barplot(data=tab_cancel, x='is_canceled', y='n', ax=ax)\n"
        "ax.set_title('Cantidad de reservas según cancelación')\n"
        "ax.set_xlabel('is_canceled (0=no, 1=sí)')\n"
        "ax.set_ylabel('Reservas')\n"
        "plt.tight_layout()\n"
        "plt.show()"
    )

    add_md(
        "**Interpretación (S9):** El dataset contiene tanto reservas confirmadas como canceladas; "
        "la proporción de canceladas define la **prevalencia del problema** y el balance de clases "
        "para etapas predictivas futuras."
    )

    add_md(
        "### 6.2 `lead_time` – distribución global (Semana 9)\n\n"
        "Se describe la anticipación **sin segmentar** por cancelación."
    )

    add_code(
        "con.execute(\n"
        "    \"\"\"\n"
        "    SELECT\n"
        "        MIN(lead_time) AS minimo,\n"
        "        ROUND(AVG(lead_time), 2) AS media,\n"
        "        MEDIAN(lead_time) AS mediana,\n"
        "        MAX(lead_time) AS maximo\n"
        "    FROM reservas_prep\n"
        "    \"\"\"\n"
        ").df()"
    )

    add_code(
        "fig, ax = plt.subplots()\n"
        "sns.histplot(data=df, x='lead_time', bins=40, ax=ax)\n"
        "ax.set_title('Distribución de lead_time (todas las reservas)')\n"
        "ax.set_xlabel('Días de anticipación')\n"
        "plt.tight_layout()\n"
        "plt.show()"
    )

    add_md(
        "**Interpretación (S9):** `lead_time` es **asimétrica** hacia la derecha: muchas reservas "
        "cercanas al check-in y una cola de reservas muy anticipadas."
    )

    add_md("### 6.3 `hotel` – frecuencias (Semana 9)")

    add_code(
        "con.execute(\n"
        "    \"\"\"\n"
        "    SELECT hotel, COUNT(*) AS n\n"
        "    FROM reservas_prep\n"
        "    GROUP BY hotel\n"
        "    ORDER BY n DESC\n"
        "    \"\"\"\n"
        ").df()"
    )

    add_code(
        "fig, ax = plt.subplots()\n"
        "sns.countplot(data=df, x='hotel', ax=ax)\n"
        "ax.set_title('Reservas por tipo de hotel')\n"
        "plt.tight_layout()\n"
        "plt.show()"
    )

    add_md("### 6.4 `market_segment` – frecuencias (Semana 9)")

    add_code(
        "seg = con.execute(\n"
        "    \"\"\"\n"
        "    SELECT market_segment, COUNT(*) AS n\n"
        "    FROM reservas_prep\n"
        "    GROUP BY market_segment\n"
        "    ORDER BY n DESC\n"
        "    \"\"\"\n"
        ").df()\n"
        "seg.head(10)"
    )

    add_md("### 6.5 `deposit_type` y `total_nights` (Semana 9)")

    add_code(
        "con.execute(\n"
        "    \"\"\"\n"
        "    SELECT deposit_type, COUNT(*) AS n\n"
        "    FROM reservas_prep\n"
        "    GROUP BY deposit_type\n"
        "    ORDER BY n DESC\n"
        "    \"\"\"\n"
        ").df()"
    )

    add_code(
        "con.execute(\n"
        "    \"\"\"\n"
        "    SELECT\n"
        "        MIN(total_nights) AS min_noches,\n"
        "        ROUND(AVG(total_nights), 2) AS promedio,\n"
        "        MAX(total_nights) AS max_noches\n"
        "    FROM reservas_prep\n"
        "    \"\"\"\n"
        ").df()"
    )

    add_md(
        "## 7. Preguntas e hipótesis para la Semana 10\n\n"
        "Durante la Semana 9 se plantearon varias líneas de exploración. "
        "Para la **Entrega 4** selecciono **tres hipótesis centrales** (obligatorias en la consigna) "
        "y dos preguntas complementarias que amplían el análisis:\n\n"
        "**Hipótesis seleccionadas (desarrollo principal en §8):**\n\n"
        "1. ¿La **tasa de cancelación** difiere entre City Hotel y Resort Hotel?\n"
        "2. ¿Las reservas canceladas presentan **mayor `lead_time`** (más anticipación)?\n"
        "3. ¿El **tipo de depósito** se asocia con distintas tasas de cancelación?\n\n"
        "**Exploración complementaria:**\n\n"
        "4. ¿Algunos **segmentos de mercado** concentran más cancelaciones?\n"
        "5. ¿Reservas **más largas** (`total_nights`) se cancelan con distinta frecuencia?"
    )

    add_md(
        "## 8. EDA comparativo y conclusiones (Semana 10 · entrega Moodle)\n\n"
        "A continuación se **comparan** reservas canceladas vs no canceladas. "
        "Las interpretaciones se limitan a **asociaciones observables** en los datos (no causalidad)."
    )

    add_md("### 8.1 Tasa de cancelación por tipo de hotel")

    add_code(
        "tasa_hotel = con.execute(\n"
        "    \"\"\"\n"
        "    SELECT\n"
        "        hotel,\n"
        "        COUNT(*) AS n,\n"
        "        ROUND(100.0 * AVG(is_canceled), 2) AS tasa_cancel_pct\n"
        "    FROM reservas_prep\n"
        "    GROUP BY hotel\n"
        "    ORDER BY tasa_cancel_pct DESC\n"
        "    \"\"\"\n"
        ").df()\n"
        "tasa_hotel"
    )

    add_code(
        "fig, ax = plt.subplots()\n"
        "sns.barplot(data=tasa_hotel, x='hotel', y='tasa_cancel_pct', ax=ax)\n"
        "ax.set_title('Tasa de cancelación (%) por hotel')\n"
        "ax.set_ylabel('% canceladas')\n"
        "plt.tight_layout()\n"
        "plt.show()"
    )

    add_md(
        "**Interpretación:** Si un tipo de hotel muestra mayor porcentaje de cancelaciones, "
        "el segmento puede requerir políticas comerciales distintas. Conviene contrastar con el **volumen** (`n`)."
    )

    add_md("### 8.2 `lead_time` vs cancelación")

    add_code(
        "fig, ax = plt.subplots()\n"
        "sns.boxplot(data=df, x='is_canceled_label', y='lead_time', ax=ax, showfliers=False)\n"
        "ax.set_title('lead_time según estado de cancelación')\n"
        "ax.set_xlabel('Estado')\n"
        "ax.set_ylabel('Días de anticipación')\n"
        "plt.tight_layout()\n"
        "plt.show()\n"
        "\n"
        "df.groupby('is_canceled_label')['lead_time'].median()"
    )

    add_md(
        "**Interpretación:** Una **mediana** de `lead_time` más alta en canceladas sugiere que reservas "
        "muy anticipadas pueden ser más volátiles. No implica por sí sola mayor \"probabilidad\" sin "
        "un análisis formal; es una **hipótesis** apoyada en el gráfico."
    )

    add_md("### 8.3 Depósito y segmento de mercado")

    add_code(
        "tasa_dep = con.execute(\n"
        "    \"\"\"\n"
        "    SELECT\n"
        "        deposit_type,\n"
        "        COUNT(*) AS n,\n"
        "        ROUND(100.0 * AVG(is_canceled), 2) AS tasa_cancel_pct\n"
        "    FROM reservas_prep\n"
        "    GROUP BY deposit_type\n"
        "    ORDER BY tasa_cancel_pct DESC\n"
        "    \"\"\"\n"
        ").df()\n"
        "tasa_dep"
    )

    add_code(
        "tasa_seg = con.execute(\n"
        "    \"\"\"\n"
        "    SELECT\n"
        "        market_segment,\n"
        "        COUNT(*) AS n,\n"
        "        ROUND(100.0 * AVG(is_canceled), 2) AS tasa_cancel_pct\n"
        "    FROM reservas_prep\n"
        "    GROUP BY market_segment\n"
        "    HAVING COUNT(*) >= 50\n"
        "    ORDER BY tasa_cancel_pct DESC\n"
        "    \"\"\"\n"
        ").df()\n"
        "tasa_seg"
    )

    add_code(
        "fig, ax = plt.subplots(figsize=(10, 5))\n"
        "sns.barplot(data=tasa_seg, x='market_segment', y='tasa_cancel_pct', ax=ax)\n"
        "ax.set_title('Tasa de cancelación por segmento (n ≥ 50)')\n"
        "ax.tick_params(axis='x', rotation=30)\n"
        "plt.tight_layout()\n"
        "plt.show()"
    )

    add_md("### 8.4 `total_nights` vs cancelación")

    add_code(
        "fig, ax = plt.subplots()\n"
        "sns.boxplot(data=df, x='is_canceled_label', y='total_nights', ax=ax, showfliers=False)\n"
        "ax.set_title('Duración de estadía vs cancelación')\n"
        "plt.tight_layout()\n"
        "plt.show()"
    )

    add_md(
        "## 9. Cierre del EDA (Semana 10)\n\n"
        "### 9.1 Variables candidatas para etapas predictivas\n\n"
        "A partir de las comparaciones exploratorias, estas variables podrían aportar señal para "
        "modelar `is_canceled` más adelante (sin garantizar poder predictivo hasta entrenar y validar):\n\n"
        "| Variable | Motivo |\n"
        "|----------|--------|\n"
        "| `lead_time` | Diferencias de mediana entre canceladas y no canceladas |\n"
        "| `hotel` | Tasas de cancelación distintas por tipo de establecimiento |\n"
        "| `deposit_type` | Política de depósito ligada a distintos `%` de cancelación |\n"
        "| `market_segment` | Segmentos con tasas altas y volumen razonable (n ≥ 50) |\n"
        "| `total_nights` | Posible relación con duración de estadía y riesgo operativo |\n\n"
        "Variables con muchos nulos (`agent`, `company`) o poco uso en este EDA quedan pendientes de evaluar."
    )

    add_md(
        "### 9.2 Tres hallazgos respaldados por la evidencia\n\n"
        "1. **Prevalencia:** aproximadamente tres de cada diez reservas en el subset corresponden a "
        "cancelaciones (`is_canceled = 1`), lo que confirma que el fenómeno es relevante para la operación.\n"
        "2. **Hotel y canal:** las tasas de cancelación difieren entre tipos de hotel y segmentos de mercado; "
        "convendría monitorear por separado los segmentos con mayor `%` y volumen suficiente.\n"
        "3. **Anticipación y depósito:** canceladas suelen mostrar `lead_time` más alto y depósitos "
        "no reembolsables se asocian con menores tasas, coherente con mayor compromiso económico "
        "(asociación observada, no causalidad)."
    )

    add_md(
        "### 9.3 Alcances y limitaciones\n\n"
        "1. **Observacional:** las diferencias entre grupos **no demuestran** causas; variables no "
        "controladas (temporada, precio, canal) pueden confundir la lectura.\n"
        "2. **Muestra y categorías:** segmentos con pocos casos producen tasas inestables; no se "
        "generalizó a otros hoteles ni períodos fuera del CSV de la comisión.\n"
        "3. **Sin modelado:** no se estimó probabilidad predictiva ni se validó en hold-out; "
        "los boxplots muestran **distribución y mediana**, no inferencia formal."
    )

    write_nb(NB_DIR / "Viruel_Nicolas_10_Entrega4.ipynb", cells)


def copy_dataset() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    NB_DIR.mkdir(parents=True, exist_ok=True)
    if HOTEL_SRC.exists():
        shutil.copy2(HOTEL_SRC, DATA_DIR / HOTEL_SRC.name)
        print(f"Copiado: {DATA_DIR / HOTEL_SRC.name}")
    else:
        raise FileNotFoundError(f"No se encontró {HOTEL_SRC}")


def main() -> None:
    copy_dataset()
    build_tpi_entrega4()


if __name__ == "__main__":
    main()
