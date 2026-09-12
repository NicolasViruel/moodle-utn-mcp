"""Genera TPI Entrega 3 (visualización) para IAD Semana 6."""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NB_DIR = ROOT / "notebooks"
DATA_DIR = ROOT / "datos"
HOTEL_SRC = ROOT.parent / "semana-5" / "datos" / "hotel_booking_TPI_grupo_J.csv"


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


def build_tpi_entrega3() -> None:
    out = NB_DIR / "Viruel_Nicolas_10_Entrega3.ipynb"
    cells = []

    def add_md(t):
        cells.append(md(t))

    def add_code(t):
        cells.append(code(t))

    add_md(
        "# Trabajo Práctico Integrador – Entrega 3\n\n"
        "**Materia:** Introducción al Análisis de Datos  \n"
        "**Tema:** Cancelación de reservas hoteleras  \n"
        "**Comisión:** 10 (Grupo J)  \n"
        "**Integrante:** Viruel, Nicolás  \n"
        "**Entrega:** 3 – Unidad N° 3 · Visualización de datos  \n"
        "**Lenguaje:** Python  \n"
        "**Dataset:** `hotel_booking_TPI_grupo_J.csv`  \n"
        "**Variable objetivo:** `is_canceled`  \n"
        "**Año:** 2026\n\n"
        "> Notebook independiente y reproducible desde cero."
    )

    add_md(
        "## 1. Contexto\n\n"
        "En esta entrega aplicamos **visualización e interpretación** al dataset de reservas "
        "hoteleras. El foco no es la cantidad de gráficos, sino responder preguntas concretas "
        "sobre la **cancelación de reservas** (`is_canceled`)."
    )

    add_md("## 2. Carga del dataset y preparación mínima")

    add_code(
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
        "df = pd.read_csv(DATA_DIR / 'hotel_booking_TPI_grupo_J.csv')\n"
        "print('Dataset cargado:', df.shape)"
    )

    add_code(
        "# Preparación mínima para visualizar\n"
        "df['is_canceled_label'] = df['is_canceled'].map({0: 'No cancelada', 1: 'Cancelada'})\n"
        "df['total_nights'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']\n"
        "df['total_guests'] = df['adults'] + df['children'].fillna(0) + df['babies']\n"
        "\n"
        "# lead_time en categorías interpretables (sin imputar children como 0 en el análisis global)\n"
        "df['lead_time_segment'] = pd.cut(\n"
        "    df['lead_time'],\n"
        "    bins=[-1, 7, 30, 90, df['lead_time'].max()],\n"
        "    labels=['0-7 días', '8-30 días', '31-90 días', '91+ días'],\n"
        ")\n"
        "\n"
        "df[['hotel', 'is_canceled', 'lead_time', 'total_nights', 'adr']].head()"
    )

    add_md(
        "## 3. Visualización 1 · Cancelaciones según tipo de hotel\n\n"
        "**Pregunta:** ¿La proporción de cancelaciones difiere entre City Hotel y Resort Hotel?\n\n"
        "**Tipo de gráfico:** barras agrupadas con conteos absolutos. Permite comparar simultáneamente "
        "volumen de reservas y balance cancelada/no cancelada por tipo de hotel.\n\n"
        "**Elementos visuales:** color distingue estado de cancelación; posición en eje X separa hoteles."
    )

    add_code(
        "fig, ax = plt.subplots()\n"
        "sns.countplot(data=df, x='hotel', hue='is_canceled_label', ax=ax)\n"
        "ax.set_title('Cancelaciones de reservas según tipo de hotel')\n"
        "ax.set_xlabel('Tipo de hotel')\n"
        "ax.set_ylabel('Cantidad de reservas')\n"
        "ax.legend(title='Estado', loc='upper right')\n"
        "plt.tight_layout()\n"
        "plt.show()\n"
        "\n"
        "tasa = df.groupby('hotel')['is_canceled'].mean().mul(100).round(1)\n"
        "print('Tasa de cancelación (%):')\n"
        "print(tasa)"
    )

    add_md(
        "**Interpretación:** Si la tasa de cancelación es mayor en un tipo de hotel, el patrón sugiere "
        "que el segmento (ciudad vs resort) enfrenta dinámicas distintas de reserva. Conviene contrastar "
        "con volumen absoluto: un hotel puede tener más cancelaciones totales pero menor proporción."
    )

    add_md(
        "## 4. Visualización 2 · Variable cuantitativa y cancelación\n\n"
        "**Pregunta:** ¿Las reservas canceladas se realizan con mayor anticipación (`lead_time`) "
        "que las no canceladas?\n\n"
        "**Tipo de gráfico:** diagrama de cajas (boxplot) por grupo de cancelación. Resume mediana, "
        "dispersión y valores atípicos de una variable numérica frente a una binaria.\n\n"
        "**Por qué este gráfico:** `lead_time` es continua y asimétrica; el boxplot permite comparar "
        "distribuciones sin asumir normalidad."
    )

    add_code(
        "fig, ax = plt.subplots()\n"
        "sns.boxplot(data=df, x='is_canceled_label', y='lead_time', ax=ax, showfliers=False)\n"
        "ax.set_title('Anticipación de la reserva (lead_time) según cancelación')\n"
        "ax.set_xlabel('Estado de la reserva')\n"
        "ax.set_ylabel('Días de anticipación (lead_time)')\n"
        "plt.tight_layout()\n"
        "plt.show()\n"
        "\n"
        "print(df.groupby('is_canceled_label')['lead_time'].describe()[['mean', '50%', 'max']])"
    )

    add_md(
        "**Interpretación:** Una mediana o media de `lead_time` más alta en canceladas indicaría que "
        "reservas muy anticipadas tienen mayor probabilidad de cancelarse (cambios de planes). "
        "Excluimos outliers del gráfico para mejorar legibilidad, pero conviene recordar que existen "
        "valores extremos que pueden influir en promedios."
    )

    add_md(
        "## 5. Visualización 3 · Pregunta propia de análisis\n\n"
        "**Pregunta:** ¿Cómo varía la tasa de cancelación según el tipo de depósito (`deposit_type`) "
        "y el segmento de mercado (`market_segment`)?\n\n"
        "**Tipo de gráfico:** barras agrupadas con tasas de cancelación (%). Incorpora dos dimensiones "
        "categóricas para detectar combinaciones de mayor riesgo.\n\n"
        "**Por qué este gráfico:** ambas variables son nominales y la respuesta es una proporción; "
        "comparar porcentajes facilita identificar políticas de depósito o canales más expuestos a cancelaciones."
    )

    add_code(
        "tasa_dep = (\n"
        "    df.groupby(['market_segment', 'deposit_type'], observed=True)['is_canceled']\n"
        "    .mean()\n"
        "    .mul(100)\n"
        "    .reset_index(name='tasa_cancelacion_pct')\n"
        ")\n"
        "tasa_dep = tasa_dep.sort_values('tasa_cancelacion_pct', ascending=False)\n"
        "\n"
        "fig, ax = plt.subplots(figsize=(10, 5))\n"
        "sns.barplot(\n"
        "    data=tasa_dep,\n"
        "    x='market_segment',\n"
        "    y='tasa_cancelacion_pct',\n"
        "    hue='deposit_type',\n"
        "    ax=ax,\n"
        ")\n"
        "ax.set_title('Tasa de cancelación por segmento de mercado y tipo de depósito')\n"
        "ax.set_xlabel('Segmento de mercado')\n"
        "ax.set_ylabel('Tasa de cancelación (%)')\n"
        "ax.tick_params(axis='x', rotation=25)\n"
        "ax.legend(title='Depósito', bbox_to_anchor=(1.02, 1), loc='upper left')\n"
        "plt.tight_layout()\n"
        "plt.show()\n"
        "\n"
        "tasa_dep.head(8)"
    )

    add_md(
        "**Interpretación:** Combinaciones con depósito no reembolsable suelen mostrar menor cancelación "
        "que reservas sin depósito, lo cual es coherente con incentivos económicos. Segmentos online/offline "
        "pueden diferir en compromiso del huésped. Hay que interpretar con cautela segmentos con pocas reservas."
    )

    add_md(
        "## 6. Síntesis de hallazgos\n\n"
        "1. **Tipo de hotel:** la tasa de cancelación difiere entre City Hotel y Resort Hotel; conviene "
        "analizar cada segmento por separado en modelos futuros.\n"
        "2. **Anticipación:** las reservas canceladas tienden a concentrarse en mayores valores de "
        "`lead_time`, lo que sugiere que reservas muy anticipadas son más volátiles.\n"
        "3. **Depósito y canal:** la política de depósito y el segmento de mercado se asocian con "
        "distintas tasas de cancelación; reservas sin depósito suelen ser más riesgosas.\n\n"
        "**Limitación / precaución:** estos gráficos muestran **asociaciones**, no causalidad. Además, "
        "categorías con pocos casos pueden producir tasas extremas; antes de generalizar conviene filtrar "
        "por volumen mínimo o usar intervalos de confianza en análisis posteriores."
    )

    nb = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3"},
        },
        "cells": cells,
    }
    out.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Escrito: {out}")


def copy_hotel_dataset() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    NB_DIR.mkdir(parents=True, exist_ok=True)
    if HOTEL_SRC.exists():
        shutil.copy2(HOTEL_SRC, DATA_DIR / HOTEL_SRC.name)
        print(f"Copiado: {DATA_DIR / HOTEL_SRC.name}")


def main() -> None:
    copy_hotel_dataset()
    build_tpi_entrega3()


if __name__ == "__main__":
    main()
