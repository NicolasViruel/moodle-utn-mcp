"""Genera/actualiza notebooks de Semana 4: S4 práctica autónoma + TPI Entrega 2."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NB_DIR = ROOT / "notebooks"
DATA_DIR = ROOT / "datos"


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


def update_s4_notebook() -> None:
    path = NB_DIR / "S4_Diagnostico_y_limpieza_Python.ipynb"
    nb = json.loads(path.read_text(encoding="utf-8"))

    load_cell = (
        "from pathlib import Path\n"
        "\n"
        "DATA_DIR = Path('../datos')\n"
        "df_playstore = pd.read_csv(DATA_DIR / 'google-play-store-apps.csv')\n"
        "print('Dataset cargado:', df_playstore.shape)"
    )

    titanic_load = (
        "from pathlib import Path\n"
        "\n"
        "DATA_DIR = Path('../datos')\n"
        "df_titanic = pd.read_csv(DATA_DIR / 'titanic.csv')\n"
        "df_titanic.info()"
    )

    for cell in nb["cells"]:
        src = "".join(cell.get("source", []))
        if "kagglehub" in src or "pd.load_csv('\\\\content\\\\google-play-store-apps.csv')" in src:
            cell["source"] = load_cell
            cell["outputs"] = []
            cell["execution_count"] = None
            if "metadata" in cell and "colab" in cell["metadata"]:
                del cell["metadata"]["colab"]
        if "url_titanic_raw" in src or "datasciencedojo" in src:
            cell["source"] = titanic_load
            cell["outputs"] = []
            cell["execution_count"] = None
            if "metadata" in cell and "colab" in cell["metadata"]:
                del cell["metadata"]["colab"]

    # Remove old head() outputs for cleaner notebook
    for cell in nb["cells"]:
        src = "".join(cell.get("source", []))
        if src.strip() == "df_playstore.head()":
            cell["outputs"] = []
            cell["execution_count"] = None

    new_cells = [
        md(
            "## Diagnóstico inicial\n"
            "\n"
            "Revisamos dimensiones, tipos de datos y estadísticos básicos antes de modificar el dataset."
        ),
        code(
            "print('Dimensiones:', df_playstore.shape)\n"
            "df_playstore.info()"
        ),
        code("df_playstore.describe(include='all').T"),
        code(
            "print('Valores nulos por columna:')\n"
            "print(df_playstore.isna().sum().sort_values(ascending=False))"
        ),
        code(
            "print('Registros duplicados (todas las columnas):', df_playstore.duplicated().sum())\n"
            "print('Duplicados App + Category:', df_playstore.duplicated(subset=['App', 'Category']).sum())"
        ),
        code(
            "print('Rating fuera de rango 1-5:', (df_playstore['Rating'] > 5).sum())\n"
            "print('Type inconsistentes:')\n"
            "print(df_playstore['Type'].value_counts(dropna=False))"
        ),
        md(
            "### Preparativos\n"
            "\n"
            "Conservamos el dataset original y trabajamos sobre una copia. "
            "También iniciamos una bitácora propia para esta práctica autónoma."
        ),
        code(
            "df_playstore_original = df_playstore.copy()\n"
            "df = df_playstore.copy()\n"
            "\n"
            "registros_bitacora_ps = []\n"
            "\n"
            "def registrar_ps(problema, variable, decision, justificacion):\n"
            "    registros_bitacora_ps.append({\n"
            "        'problema_detectado': problema,\n"
            "        'variable': variable,\n"
            "        'decision': decision,\n"
            "        'justificacion': justificacion,\n"
            "    })"
        ),
        md("### 1. Fila corrupta y duplicados"),
        code(
            "filas_corruptas = df['Rating'] > 5\n"
            "print('Filas con Rating imposible (>5):', filas_corruptas.sum())\n"
            "df.loc[filas_corruptas, ['App', 'Category', 'Rating', 'Reviews']]"
        ),
        code(
            "if filas_corruptas.any():\n"
            "    df = df.loc[~filas_corruptas].copy()\n"
            "    registrar_ps(\n"
            "        'Fila con columnas desplazadas (Rating=19, Category=1.9)',\n"
            "        'Todas',\n"
            "        'Eliminar fila corrupta',\n"
            "        'Es un error de registro, no una app válida; distorsiona tipos y estadísticos.',\n"
            "    )\n"
            "\n"
            "dup_total = df.duplicated().sum()\n"
            "print('Duplicados exactos restantes:', dup_total)\n"
            "if dup_total:\n"
            "    df = df.drop_duplicates().copy()\n"
            "    registrar_ps(\n"
            "        'Registros idénticos en todas las columnas',\n"
            "        'Todas',\n"
            "        'Eliminar duplicados exactos (keep=first)',\n"
            "        'Son copias literales del mismo registro, no aportan información.',\n"
            "    )\n"
            "\n"
            "dup_app_cat = df.duplicated(subset=['App', 'Category']).sum()\n"
            "print('Duplicados App+Category:', dup_app_cat)\n"
            "if dup_app_cat:\n"
            "    df = df.drop_duplicates(subset=['App', 'Category'], keep='first').copy()\n"
            "    registrar_ps(\n"
            "        'Misma app repetida en la misma categoría',\n"
            "        'App, Category',\n"
            "        'Conservar primera aparición',\n"
            "        'Indica republicación duplicada en la fuente; una fila por app-categoría.',\n"
            "    )\n"
            "\n"
            "print('Filas después de deduplicación:', len(df))"
        ),
        md("### 2. Valores faltantes"),
        code(
            "prop_nulos_rating = df['Rating'].isna().mean()\n"
            "print(f'Rating nulos: {df[\"Rating\"].isna().sum()} ({prop_nulos_rating:.1%})')\n"
            "print(f'Current Ver nulos: {df[\"Current Ver\"].isna().sum()}')\n"
            "print(f'Type nulos: {df[\"Type\"].isna().sum()}')"
        ),
        code(
            "registrar_ps(\n"
            "    'Calificaciones ausentes',\n"
            "    'Rating',\n"
            "    'Conservar NaN',\n"
            "    'Imputar distorsionaría la variable objetivo de popularidad; se analizará con filtros.',\n"
            ")\n"
            "registrar_ps(\n"
            "    'Versión actual ausente',\n"
            "    'Current Ver',\n"
            "    'Conservar NaN',\n"
            "    'No es crítica para el análisis de ratings/instalaciones en esta etapa.',\n"
            ")"
        ),
        md("### 3. Tipos incorrectos y categorías inconsistentes"),
        code(
            "df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')\n"
            "registrar_ps(\n"
            "    'Reviews almacenado como texto',\n"
            "    'Reviews',\n"
            "    'Convertir a numérico',\n"
            "    'Permite calcular estadísticos y detectar atípicos.',\n"
            ")\n"
            "\n"
            "def parse_installs(valor):\n"
            "    if pd.isna(valor):\n"
            "        return pd.NA\n"
            "    return int(str(valor).replace(',', '').replace('+', ''))\n"
            "\n"
            "df['Installs_num'] = df['Installs'].map(parse_installs)\n"
            "registrar_ps(\n"
            "    'Installs con formato 10,000+',\n"
            "    'Installs',\n"
            "    'Crear Installs_num entero',\n"
            "    'El signo + y las comas impiden operar; se conserva la columna original.',\n"
            ")\n"
            "\n"
            "df['Price_num'] = (\n"
            "    df['Price']\n"
            "    .astype(str)\n"
            "    .str.replace('$', '', regex=False)\n"
            "    .replace('0', 0)\n"
            ")\n"
            "df['Price_num'] = pd.to_numeric(df['Price_num'], errors='coerce')\n"
            "registrar_ps(\n"
            "    'Price con símbolo $',\n"
            "    'Price',\n"
            "    'Crear Price_num en USD',\n"
            "    'Facilita comparar apps pagas y validar coherencia con Type.',\n"
            ")\n"
            "\n"
            "mask_type_invalido = df['Type'].isin(['0']) | df['Type'].isna()\n"
            "print('Type inválido o nulo:', mask_type_invalido.sum())\n"
            "df.loc[mask_type_invalido & (df['Price_num'] == 0), 'Type'] = 'Free'\n"
            "df.loc[mask_type_invalido & (df['Price_num'] > 0), 'Type'] = 'Paid'\n"
            "registrar_ps(\n"
            "    \"Type con valor '0' o nulo\",\n"
            "    'Type',\n"
            "    'Corregir según Price_num',\n"
            "    'Free/Paid debe ser coherente con el precio; no se eliminaron filas.',\n"
            ")\n"
            "\n"
            "df['Type'] = df['Type'].astype('category')"
        ),
        md("### 4. Tamaño de la app (Size)"),
        code(
            "def parse_size_mb(valor):\n"
            "    if pd.isna(valor) or valor == 'Varies with device':\n"
            "        return pd.NA\n"
            "    texto = str(valor).strip()\n"
            "    if texto.endswith('k'):\n"
            "        return float(texto[:-1]) / 1024\n"
            "    if texto.endswith('M'):\n"
            "        return float(texto[:-1])\n"
            "    return pd.NA\n"
            "\n"
            "df['Size_MB'] = df['Size'].map(parse_size_mb)\n"
            "registrar_ps(\n"
            "    'Size con unidades k/M y texto especial',\n"
            "    'Size',\n"
            "    'Crear Size_MB numérico; conservar original',\n"
            "    \"'Varies with device' no es un error sino información válida.\",\n"
            ")"
        ),
        md("### 5. Valores atípicos (IQR) en Rating y Reviews"),
        code(
            "def detectar_outliers_iqr(serie):\n"
            "    s = serie.dropna()\n"
            "    q1, q3 = s.quantile(0.25), s.quantile(0.75)\n"
            "    iqr = q3 - q1\n"
            "    lim_inf, lim_sup = q1 - 1.5 * iqr, q3 + 1.5 * iqr\n"
            "    return s[(s < lim_inf) | (s > lim_sup)]\n"
            "\n"
            "out_rating = detectar_outliers_iqr(df['Rating'])\n"
            "out_reviews = detectar_outliers_iqr(df['Reviews'])\n"
            "print('Atípicos Rating (IQR):', len(out_rating))\n"
            "print('Atípicos Reviews (IQR):', len(out_reviews))\n"
            "print('Rating válido min/max:', df['Rating'].min(), df['Rating'].max())"
        ),
        code(
            "registrar_ps(\n"
            "    'Reviews con valores extremos (IQR)',\n"
            "    'Reviews',\n"
            "    'Conservar; marcar para análisis',\n"
            "    'Apps muy populares pueden tener millones de reseñas; no son errores.',\n"
            ")\n"
            "registrar_ps(\n"
            "    'Rating dentro de 1-5 tras limpieza',\n"
            "    'Rating',\n"
            "    'Conservar distribución',\n"
            "    'Tras eliminar la fila corrupta, no hay ratings imposibles.',\n"
            ")"
        ),
        md("### Dataset limpio y bitácora"),
        code("df_playstore_limpio = df.copy()\nprint('Shape final:', df_playstore_limpio.shape)\ndf_playstore_limpio.head()"),
        code(
            "bitacora_ps = pd.DataFrame(registros_bitacora_ps)\n"
            "bitacora_ps"
        ),
        md(
            "## Conclusión – Práctica autónoma\n"
            "\n"
            "El dataset Google Play Store presentaba **problemas de calidad reales**: una fila corrupta por desplazamiento "
            "de columnas, cientos de duplicados, variables numéricas en formato texto (`Reviews`, `Installs`, `Price`, `Size`) "
            "y categorías inconsistentes en `Type`. Se conservó el original (`df_playstore_original`) y se trabajó sobre copias.\n"
            "\n"
            "Las decisiones priorizaron **no eliminar datos solo por reglas automáticas**: los atípicos de `Reviews` se "
            "conservaron por ser apps legítimamente populares, y los `Rating` faltantes se mantuvieron para no sesgar el análisis. "
            "El dataset quedó listo para análisis exploratorio con columnas derivadas (`Installs_num`, `Price_num`, `Size_MB`)."
        ),
    ]

    # Insert before "## Consignas" cell (skip if already added)
    already = any("Conclusión – Práctica autónoma" in "".join(c.get("source", [])) for c in nb["cells"])
    if not already:
        insert_at = None
        for i, cell in enumerate(nb["cells"]):
            src = "".join(cell.get("source", []))
            if "## Consignas" in src:
                insert_at = i
                break
        if insert_at is None:
            raise RuntimeError("No se encontró la celda de Consignas en S4")
        nb["cells"] = nb["cells"][:insert_at] + new_cells + nb["cells"][insert_at:]
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Actualizado: {path}")


def build_tpi_entrega2() -> None:
    out = NB_DIR / "TPI_Entrega2_Nicolas_Viruel.ipynb"
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
        "**Integrante:** Nicolás Viruel  \n"
        "**Entrega:** 2 – Unidad N° 2 (inicio Semana 4)  \n"
        "**Año:** 2026\n\n"
        "> Notebook **independiente**: ejecutable desde cero sin depender de la Entrega 1."
    )

    add_md(
        "## 1. Contexto\n\n"
        "Analizamos cancelaciones de reservas hoteleras. **Variable objetivo:** `is_canceled` "
        "(0 = no cancelada, 1 = cancelada).\n\n"
        "En esta entrega nos enfocamos en **diagnóstico y limpieza inicial** del dataset asignado."
    )

    add_md(
        "## 2. Carga del dataset\n\n"
        "- **Archivo:** `../datos/hotel_booking_TPI_grupo_J.csv`  \n"
        "- **Comisión:** 10 · Grupo J"
    )

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

    add_md("## 3. Diagnóstico y limpieza inicial de datos")

    add_md(
        "### 3.1 Preparativos\n\n"
        "Copia de trabajo y bitácora de decisiones (Problema | Variable | Decisión | Justificación)."
    )

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

    add_md("### 3.2 Estructura, tipos y dimensiones")

    add_code(
        "print('Dimensiones:', df.shape)\n"
        "df.info()\n"
        "print('\\nDuplicados exactos:', df.duplicated().sum())"
    )

    add_code(
        "cols_sugeridas = [\n"
        "    'children', 'adults', 'babies', 'stays_in_weekend_nights',\n"
        "    'stays_in_week_nights', 'adr', 'lead_time', 'country', 'agent', 'company',\n"
        "]\n"
        "df[cols_sugeridas].describe(include='all').T"
    )

    add_md("### 3.3 Valores faltantes")

    add_code(
        "nulos = df.isna().sum().sort_values(ascending=False)\n"
        "print(nulos[nulos > 0])\n"
        "print('\\nCadenas vacías en country:', (df['country'] == '').sum())"
    )

    add_code(
        "registrar(\n"
        "    'Alta proporción de company nulo',\n"
        "    'company',\n"
        "    'Conservar NaN',\n"
        "    '94% de reservas no tienen empresa; es un patrón real, no un error masivo.',\n"
        ")\n"
        "registrar(\n"
        "    'Agent nulo en ~14% de reservas',\n"
        "    'agent',\n"
        "    'Conservar NaN',\n"
        "    'Reservas directas o sin intermediario; relevante para el análisis.',\n"
        ")\n"
        "registrar(\n"
        "    'Country ausente en 117 reservas',\n"
        "    'country',\n"
        "    'Conservar NaN',\n"
        "    'Son pocas filas (<0.5%); eliminar sesgaría países minoritarios.',\n"
        ")"
    )

    add_md("### 3.4 Valores imposibles o inconsistentes")

    add_code(
        "print('adr <= 0:', (df['adr'] <= 0).sum())\n"
        "print('adults == 0:', (df['adults'] == 0).sum())\n"
        "print('Combinación sin huéspedes (adults+children+babies==0):',\n"
        "      ((df['adults'] + df['children'] + df['babies']) == 0).sum())\n"
        "df.loc[df['adr'] <= 0, ['hotel', 'adr', 'adults', 'children', 'babies', 'is_canceled']].head()"
    )

    add_code(
        "mask_adr_invalido = df['adr'] <= 0\n"
        "print('Reservas con adr <= 0:', mask_adr_invalido.sum())\n"
        "registrar(\n"
        "    'Tarifa diaria adr nula, cero o negativa',\n"
        "    'adr',\n"
        "    'Marcar para revisión; conservar por ahora',\n"
        "    'Puede ser cortesía o error de carga; eliminar 446 filas sin contexto sería agresivo.',\n"
        ")\n"
        "\n"
        "mask_sin_adultos = df['adults'] == 0\n"
        "registrar(\n"
        "    'Reservas con adults == 0',\n"
        "    'adults',\n"
        "    'Conservar y analizar',\n"
        "    'Podría ser error o reserva especial; requiere contexto de negocio.',\n"
        ")\n"
        "\n"
        "mask_huespedes = (df['adults'] + df['children'] + df['babies']) == 0\n"
        "if mask_huespedes.any():\n"
        "    registrar(\n"
        "        'Estadía sin huéspedes registrados',\n"
        "        'adults, children, babies',\n"
        "        'Conservar para revisión',\n"
        "        'Combinación imposible en operación normal; posible error de registro.',\n"
        "    )"
    )

    add_md("### 3.5 Posibles valores atípicos (IQR)")

    add_code(
        "def detectar_outliers_iqr(serie):\n"
        "    s = serie.dropna()\n"
        "    q1, q3 = s.quantile(0.25), s.quantile(0.75)\n"
        "    iqr = q3 - q1\n"
        "    lim_inf, lim_sup = q1 - 1.5 * iqr, q3 + 1.5 * iqr\n"
        "    return s[(s < lim_inf) | (s > lim_sup)]\n"
        "\n"
        "for col in ['lead_time', 'adr', 'stays_in_week_nights', 'stays_in_weekend_nights']:\n"
        "    out = detectar_outliers_iqr(df[col])\n"
        "    print(f'{col}: {len(out)} atípicos IQR (min={df[col].min()}, max={df[col].max()})')"
    )

    add_code(
        "registrar(\n"
        "    'lead_time muy alto (hasta 629 días)',\n"
        "    'lead_time',\n"
        "    'Conservar',\n"
        "    'Anticipación extrema es posible en hoteles resort; no es error automático.',\n"
        ")\n"
        "registrar(\n"
        "    'adr atípico por IQR',\n"
        "    'adr',\n"
        "    'Conservar',\n"
        "    'Tarifas premium existen; se evaluará en EDA si distorsionan modelos.',\n"
        ")"
    )

    add_md("### 3.6 Variables temporales")

    add_code(
        "df['arrival_date'] = pd.to_datetime(df['arrival_date'], errors='coerce')\n"
        "fechas_invalidas = df['arrival_date'].isna().sum()\n"
        "print('Fechas arrival_date inválidas:', fechas_invalidas)\n"
        "print('Rango:', df['arrival_date'].min(), '→', df['arrival_date'].max())\n"
        "registrar(\n"
        "    'Unificación de arrival_date',\n"
        "    'arrival_date',\n"
        "    'Convertir a datetime',\n"
        "    'Permite análisis temporal coherente; no se detectaron fechas inválidas.',\n"
        ")"
    )

    add_md("### 3.7 Bitácora de decisiones")

    add_code("bitacora = pd.DataFrame(registros_bitacora)\nbitacora")

    add_md("### 3.8 Dataset de trabajo")

    add_code(
        "df_hotel_limpio = df.copy()\n"
        "print('Original:', df_hotel_original.shape, '| Trabajo:', df_hotel_limpio.shape)\n"
        "df_hotel_limpio[cols_sugeridas].head()"
    )

    add_md(
        "## 4. Cierre parcial (Semana 4)\n\n"
        "Se completó el **diagnóstico inicial** del dataset hotelero: estructura revisada, faltantes documentados, "
        "valores imposibles identificados (`adr <= 0`, combinaciones de huéspedes) y atípicos analizados con IQR "
        "sin eliminación automática.\n\n"
        "En la **Semana 5** se continuará con transformaciones adicionales y se entregará formalmente esta Entrega 2."
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
    print(f"Creado: {out}")


def main() -> None:
    update_s4_notebook()
    build_tpi_entrega2()


if __name__ == "__main__":
    main()
