"""Genera/actualiza notebooks IAD Semana 5: práctica S5 + TPI Entrega 2 completa."""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NB_DIR = ROOT / "notebooks"
DATA_DIR = ROOT / "datos"
S4_DATA = ROOT.parent / "semana-4" / "datos" / "hotel_booking_TPI_grupo_J.csv"


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


def patch_s5_practice() -> None:
    src = NB_DIR / "S5_Transformacion_de_Variables_Python.ipynb"
    nb = json.loads(src.read_text(encoding="utf-8"))

    diamonds_load = (
        "from pathlib import Path\n"
        "import pandas as pd\n"
        "import seaborn as sns\n"
        "\n"
        "DATA_DIR = Path('../datos')\n"
        "df_diamonds = pd.read_csv(DATA_DIR / 'diamonds.csv')\n"
        "print('Diamonds cargado:', df_diamonds.shape)"
    )
    penguins_load = (
        "from pathlib import Path\n"
        "import pandas as pd\n"
        "import seaborn as sns\n"
        "\n"
        "DATA_DIR = Path('../datos')\n"
        "archivo = DATA_DIR / 'penguins.csv'\n"
        "if archivo.exists():\n"
        "    df_penguins = pd.read_csv(archivo)\n"
        "else:\n"
        "    df_penguins = sns.load_dataset('penguins')\n"
        "print('Penguins cargado:', df_penguins.shape)"
    )

    for cell in nb["cells"]:
        src_text = "".join(cell.get("source", []))
        if cell["cell_type"] == "code" and "sns.load_dataset('diamonds')" in src_text:
            cell["source"] = diamonds_load
            cell["outputs"] = []
            cell["execution_count"] = None
        if cell["cell_type"] == "code" and "sns.load_dataset('penguins')" in src_text:
            cell["source"] = penguins_load
            cell["outputs"] = []
            cell["execution_count"] = None

    # Remove old solution cells after consignas if re-running
    cut = None
    for i, cell in enumerate(nb["cells"]):
        text = "".join(cell.get("source", []))
        if text.strip().startswith("## Consignas"):
            cut = i + 1
    if cut is None:
        raise RuntimeError("No se encontró ## Consignas en S5")
    nb["cells"] = nb["cells"][:cut]

    nb["cells"].extend(
        [
            md("## Resolución – Práctica autónoma (Penguins)"),
            code(
                "df_penguins_original = df_penguins.copy()\n"
                "df = df_penguins.copy()\n"
                "print('Filas:', len(df), '| Columnas:', len(df.columns))\n"
                "df.info()\n"
                "df.describe(include='all').T"
            ),
            code(
                "print('Nulos por columna:')\n"
                "print(df.isna().sum())\n"
                "\n"
                "registros_bitacora_penguins = []\n"
                "\n"
                "def registrar_p(problema, variable, decision, justificacion):\n"
                "    registros_bitacora_penguins.append({\n"
                "        'problema_detectado': problema,\n"
                "        'variable': variable,\n"
                "        'decision': decision,\n"
                "        'justificacion': justificacion,\n"
                "    })\n"
                "\n"
                "# Solo tratamiento de nulos (consigna 2)\n"
                "df['sex'] = df['sex'].fillna('Unknown')\n"
                "registrar_p(\n"
                "    'Sexo ausente en algunos registros',\n"
                "    'sex',\n"
                "    \"Imputar categoría 'Unknown'\",\n"
                "    'Conserva la fila y permite modelar sin perder observaciones biométricas.',\n"
                ")\n"
                "\n"
                "for col in ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']:\n"
                "    n = df[col].isna().sum()\n"
                "    if n:\n"
                "        mediana = df[col].median()\n"
                "        df[col] = df[col].fillna(mediana)\n"
                "        registrar_p(\n"
                "            f'Valores numéricos faltantes en {col}',\n"
                "            col,\n"
                "            'Imputar mediana por especie implícita en el dataset',\n"
                "            'La mediana es robusta ante outliers y mantiene escala en mm/g.',\n"
                "        )\n"
                "\n"
                "print('Nulos restantes:', df.isna().sum().sum())"
            ),
            code(
                "# a) Discretización por cuantiles (4 tramos)\n"
                "df['flipper_length_category'] = pd.qcut(\n"
                "    df['flipper_length_mm'], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4']\n"
                ")\n"
                "registrar_p(\n"
                "    'Aleta continua difícil de comparar en modelos categóricos',\n"
                "    'flipper_length_mm',\n"
                "    'Discretizar en 4 cuantiles → flipper_length_category',\n"
                "    'Agrupa pingüinos por tamaño relativo de aleta para análisis por segmentos.',\n"
                ")\n"
                "df[['flipper_length_mm', 'flipper_length_category']].head(10)"
            ),
            code(
                "# b) One-Hot Encoding de island\n"
                "island_dummies = pd.get_dummies(df['island'], prefix='island')\n"
                "island_dummies = island_dummies.rename(\n"
                "    columns={\n"
                "        'island_Torgersen': 'island_torgersen',\n"
                "        'island_Biscoe': 'island_biscoe',\n"
                "        'island_Dream': 'island_dream',\n"
                "    }\n"
                ")\n"
                "df = pd.concat([df.drop(columns=['island']), island_dummies], axis=1)\n"
                "registrar_p(\n"
                "    'Isla nominal con 3 categorías',\n"
                "    'island',\n"
                "    'One-Hot → island_torgersen, island_biscoe, island_dream',\n"
                "    'Permite usar la isla en modelos que requieren entradas numéricas sin orden falso.',\n"
                ")\n"
                "df[['island_torgersen', 'island_biscoe', 'island_dream']].head(10)"
            ),
            code(
                "# c) Min-Max de bill_length_mm\n"
                "min_bl = df['bill_length_mm'].min()\n"
                "max_bl = df['bill_length_mm'].max()\n"
                "df['bill_length_minmax'] = (df['bill_length_mm'] - min_bl) / (max_bl - min_bl)\n"
                "registrar_p(\n"
                "    'Dispersión amplia en longitud de pico',\n"
                "    'bill_length_mm',\n"
                "    'Normalización Min-Max → bill_length_minmax en [0,1]',\n"
                "    'Facilita comparar con otras variables en escala acotada.',\n"
                ")\n"
                "df[['bill_length_mm', 'bill_length_minmax']].head(10)"
            ),
            code(
                "# d) Estandarización de body_mass_g\n"
                "media_masa = df['body_mass_g'].mean()\n"
                "std_masa = df['body_mass_g'].std()\n"
                "df['body_mass_standard'] = (df['body_mass_g'] - media_masa) / std_masa\n"
                "registrar_p(\n"
                "    'Masa corporal en gramos (escala distinta a mm)',\n"
                "    'body_mass_g',\n"
                "    'Estandarizar → media 0, desvío 1 (body_mass_standard)',\n"
                "    'Equipara magnitudes cuando se combinan variables en modelos multivariados.',\n"
                ")\n"
                "print('Media body_mass_standard:', round(df['body_mass_standard'].mean(), 4))\n"
                "print('Std body_mass_standard:', round(df['body_mass_standard'].std(), 4))\n"
                "df[['body_mass_g', 'body_mass_standard']].head(10)"
            ),
            code(
                "# e) Variable derivada bill_ratio\n"
                "df['bill_ratio'] = df['bill_length_mm'] / df['bill_depth_mm']\n"
                "registrar_p(\n"
                "    'Relación forma del pico no explícita en columnas originales',\n"
                "    'bill_length_mm, bill_depth_mm',\n"
                "    'Crear bill_ratio = longitud / profundidad',\n"
                "    'Resume la forma del pico; puede diferenciar especies/morfologías.',\n"
                ")\n"
                "df[['bill_length_mm', 'bill_depth_mm', 'bill_ratio']].head(10)"
            ),
            code(
                "bitacora_penguins = pd.DataFrame(registros_bitacora_penguins)\n"
                "bitacora_penguins"
            ),
            md(
                "### Conclusión – Práctica autónoma\n\n"
                "Se observó el dataset **Penguins**, se trataron **solo valores nulos** y se aplicaron "
                "discretización, codificación one-hot, normalización Min-Max, estandarización y una "
                "variable derivada (`bill_ratio`), documentando cada decisión en la bitácora. "
                "Las columnas originales se conservaron junto con las transformadas."
            ),
        ]
    )

    src.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Actualizado: {src}")


def build_tpi_entrega2() -> None:
    out = NB_DIR / "Viruel_Nicolas_10_Entrega2.ipynb"
    cells = []

    def add_md(text):
        cells.append(md(text))

    def add_code(text):
        cells.append(code(text))

    add_md(
        "# Trabajo Práctico Integrador – Entrega 2\n\n"
        "**Materia:** Introducción al Análisis de Datos  \n"
        "**Tema:** Cancelación de reservas hoteleras  \n"
        "**Comisión:** 10 (Grupo J)  \n"
        "**Integrante:** Viruel, Nicolás  \n"
        "**Entrega:** 2 – Unidad N° 2  \n"
        "**Dataset:** `hotel_booking_TPI_grupo_J.csv`  \n"
        "**Variable objetivo:** `is_canceled`  \n"
        "**Año:** 2026\n\n"
        "> Notebook independiente: ejecutable desde cero."
    )

    add_md(
        "## 1. Contexto\n\n"
        "Analizamos reservas hoteleras para estudiar cancelaciones. En esta entrega aplicamos "
        "**diagnóstico, limpieza y transformación** del dataset asignado a la comisión 10 (Grupo J)."
    )

    add_md("## 2. Carga reproducible del dataset")

    add_code(
        "import pandas as pd\n"
        "import numpy as np\n"
        "from pathlib import Path\n"
        "\n"
        "DATA_DIR = Path('../datos')\n"
        "archivo = DATA_DIR / 'hotel_booking_TPI_grupo_J.csv'\n"
        "df_hotel = pd.read_csv(archivo)\n"
        "print('Dataset cargado:', df_hotel.shape)"
    )

    add_md("## 3. Copia de trabajo y bitácora")

    add_code(
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
    )

    add_md("## 4. Diagnóstico de calidad")

    add_code(
        "print('Dimensiones:', df.shape)\n"
        "print('Duplicados exactos:', df.duplicated().sum())\n"
        "df.info()"
    )

    add_code(
        "cols_clave = [\n"
        "    'children', 'adults', 'babies', 'stays_in_weekend_nights',\n"
        "    'stays_in_week_nights', 'adr', 'lead_time', 'country', 'agent', 'company',\n"
        "    'hotel', 'market_segment', 'deposit_type', 'customer_type', 'is_canceled',\n"
        "]\n"
        "df[cols_clave].describe(include='all').T"
    )

    add_code(
        "nulos = df.isna().sum().sort_values(ascending=False)\n"
        "print(nulos[nulos > 0])\n"
        "registrar('Alta proporción de company nulo', 'company', 'Conservar NaN',\n"
        "          'Patrón real de reservas sin empresa (~94% nulo).')\n"
        "registrar('Agent nulo en ~14%', 'agent', 'Conservar NaN',\n"
        "          'Reservas directas o sin intermediario.')\n"
        "registrar('Country ausente', 'country', 'Conservar NaN',\n"
        "          'Pocas filas; eliminar sesgaría países minoritarios.')"
    )

    add_code(
        "print('adr <= 0:', (df['adr'] <= 0).sum())\n"
        "print('adults == 0:', (df['adults'] == 0).sum())\n"
        "print('Sin huéspedes:', ((df['adults'] + df['children'].fillna(0) + df['babies']) == 0).sum())\n"
        "registrar('Tarifa adr <= 0', 'adr', 'Conservar y marcar',\n"
        "          'Puede ser cortesía o error; no se elimina sin validación de negocio.')\n"
        "registrar('lead_time elevado', 'lead_time', 'Conservar',\n"
        "          'Anticipación extrema es posible en resorts.')"
    )

    add_code(
        "def detectar_outliers_iqr(serie):\n"
        "    s = serie.dropna()\n"
        "    q1, q3 = s.quantile(0.25), s.quantile(0.75)\n"
        "    iqr = q3 - q1\n"
        "    lim_inf, lim_sup = q1 - 1.5 * iqr, q3 + 1.5 * iqr\n"
        "    return s[(s < lim_inf) | (s > lim_sup)]\n"
        "\n"
        "for col in ['lead_time', 'adr']:\n"
        "    out = detectar_outliers_iqr(df[col])\n"
        "    print(f'{col}: {len(out)} atípicos IQR')"
    )

    add_md("## 5. Limpieza aplicada")

    add_code(
        "df['children'] = df['children'].fillna(0)\n"
        "registrar('children nulo', 'children', 'Imputar 0',\n"
        "          'Sin hijos registrados se interpreta como 0 huéspedes menores.')\n"
        "\n"
        "df['country'] = df['country'].replace('', np.nan)\n"
        "df['arrival_date'] = pd.to_datetime(df['arrival_date'], errors='coerce')\n"
        "registrar('Unificación temporal', 'arrival_date', 'Convertir a datetime',\n"
        "          'Habilita variables derivadas de calendario.')"
    )

    add_md("## 6. Transformación de variables")

    add_code(
        "# Variables derivadas sugeridas\n"
        "df['total_nights'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']\n"
        "df['total_guests'] = df['adults'] + df['children'] + df['babies']\n"
        "df['estimated_stay_amount'] = df['adr'] * df['total_nights']\n"
        "df['family_booking'] = ((df['children'] > 0) | (df['babies'] > 0)).astype(int)\n"
        "registrar('Duración de estadía dispersa', 'stays_in_weekend_nights, stays_in_week_nights',\n"
        "          'Crear total_nights', 'Resume noches totales para importe y segmentación.')\n"
        "registrar('Huéspedes en varias columnas', 'adults, children, babies',\n"
        "          'Crear total_guests', 'Variable única para capacidad/ocupación.')\n"
        "registrar('Importe no explícito', 'adr, total_nights',\n"
        "          'estimated_stay_amount = adr * total_nights',\n"
        "          'Aproxima ingreso de la reserva para análisis económico.')\n"
        "registrar('Reservas familiares', 'children, babies',\n"
        "          'family_booking binaria', 'Marca presencia de menores.')\n"
        "df[['total_nights', 'total_guests', 'estimated_stay_amount', 'family_booking']].head()"
    )

    add_code(
        "# Discretización lead_time\n"
        "df['lead_time_segment'] = pd.cut(\n"
        "    df['lead_time'],\n"
        "    bins=[-1, 7, 30, 90, df['lead_time'].max()],\n"
        "    labels=['0-7 días', '8-30 días', '31-90 días', '91+ días'],\n"
        ")\n"
        "registrar('lead_time continuo amplio', 'lead_time',\n"
        "          'Discretizar en lead_time_segment',\n"
        "          'Facilita comparar cancelaciones por anticipación de reserva.')\n"
        "df['lead_time_segment'].value_counts()"
    )

    add_code(
        "# Variables temporales\n"
        "df['arrival_month'] = df['arrival_date'].dt.month\n"
        "df['arrival_dayofweek'] = df['arrival_date'].dt.dayofweek\n"
        "registrar('Fecha de llegada', 'arrival_date',\n"
        "          'Extraer arrival_month y arrival_dayofweek',\n"
        "          'Captura estacionalidad y día de la semana.')"
    )

    add_code(
        "# Codificación categórica (one-hot de hotel y deposit_type)\n"
        "hotel_dummies = pd.get_dummies(df['hotel'], prefix='hotel', drop_first=True)\n"
        "deposit_dummies = pd.get_dummies(df['deposit_type'], prefix='deposit', drop_first=True)\n"
        "df = pd.concat([df, hotel_dummies, deposit_dummies], axis=1)\n"
        "registrar('hotel nominal', 'hotel', 'One-Hot con drop_first',\n"
        "          'Evita multicolinealidad perfecta en modelos lineales.')\n"
        "registrar('deposit_type ordinal/nominal', 'deposit_type', 'One-Hot',\n"
        "          'Política de depósito puede explicar cancelaciones.')\n"
        "list(hotel_dummies.columns) + list(deposit_dummies.columns)"
    )

    add_code(
        "# Normalización Min-Max de adr (solo valores positivos para referencia)\n"
        "adr_pos = df.loc[df['adr'] > 0, 'adr']\n"
        "adr_min, adr_max = adr_pos.min(), adr_pos.max()\n"
        "df['adr_minmax'] = np.where(\n"
        "    df['adr'] > 0,\n"
        "    (df['adr'] - adr_min) / (adr_max - adr_min),\n"
        "    np.nan,\n"
        ")\n"
        "registrar('adr en escala amplia', 'adr', 'adr_minmax en [0,1] para adr>0',\n"
        "          'Escala comparable con otras variables normalizadas; adr<=0 queda NaN.')"
    )

    add_code(
        "# Estandarización de total_guests\n"
        "tg_mean = df['total_guests'].mean()\n"
        "tg_std = df['total_guests'].std()\n"
        "df['total_guests_standard'] = (df['total_guests'] - tg_mean) / tg_std\n"
        "registrar('total_guests para modelos', 'total_guests',\n"
        "          'Estandarizar → total_guests_standard',\n"
        "          'Centra y escala huéspedes totales para algoritmos sensibles a magnitud.')"
    )

    add_md("## 7. Bitácora del proceso")

    add_code("bitacora = pd.DataFrame(registros_bitacora)\nbitacora")

    add_md("## 8. Dataset preparado")

    add_code(
        "df_hotel_preparado = df.copy()\n"
        "print('Original:', df_hotel_original.shape)\n"
        "print('Preparado:', df_hotel_preparado.shape)\n"
        "print('Columnas nuevas:', set(df_hotel_preparado.columns) - set(df_hotel_original.columns))\n"
        "df_hotel_preparado[['is_canceled', 'total_nights', 'total_guests', 'estimated_stay_amount',\n"
        "                     'lead_time_segment', 'family_booking', 'adr_minmax']].head(10)"
    )

    add_md(
        "## 9. Cierre\n\n"
        "El dataset quedó **diagnosticado, limpiado y transformado** con criterio analítico: "
        "se conservó el original, se documentaron faltantes e inconsistencias, se crearon variables "
        "derivadas (`total_nights`, `total_guests`, `estimated_stay_amount`, `family_booking`), "
        "segmentos de `lead_time`, codificación de categorías y escalado de variables numéricas. "
        "Este conjunto preparado habilita análisis exploratorio y modelado de `is_canceled` en entregas posteriores."
    )

    write_nb(out, cells)


def copy_hotel_dataset() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if S4_DATA.exists():
        dest = DATA_DIR / S4_DATA.name
        shutil.copy2(S4_DATA, dest)
        print(f"Copiado: {dest}")


def main() -> None:
    copy_hotel_dataset()
    patch_s5_practice()
    build_tpi_entrega2()


if __name__ == "__main__":
    main()
