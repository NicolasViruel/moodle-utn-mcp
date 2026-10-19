"""Genera TPI Entrega 5 (primer modelo predictivo) – IAD Semana 12."""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NB_DIR = ROOT / "notebooks"
DATA_DIR = ROOT / "datos"
TPI_DIR = ROOT / "tpi"
HOTEL_CANDIDATES = [
    ROOT.parent / "semana-9" / "datos" / "hotel_booking_TPI_grupo_J.csv",
    ROOT.parent / "semana-6" / "datos" / "hotel_booking_TPI_grupo_J.csv",
    ROOT.parent / "semana-5" / "datos" / "hotel_booking_TPI_grupo_J.csv",
]


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
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3"},
        },
        "cells": cells,
    }
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Escrito: {path}")


def build_tpi_entrega5() -> None:
    cells: list = []

    def add_md(t: str) -> None:
        cells.append(md(t))

    def add_code(t: str) -> None:
        cells.append(code(t))

    add_md(
        "# Trabajo Práctico Integrador – Entrega 5\n\n"
        "**Materia:** Introducción al Análisis de Datos  \n"
        "**Tema:** Cancelación de reservas hoteleras  \n"
        "**Comisión:** 10 (Grupo J)  \n"
        "**Integrante:** Viruel, Nicolás  \n"
        "**Entrega:** 5 – Primer modelo predictivo e interpretación inicial  \n"
        "**Recorrido:** SQL (DuckDB) + Python  \n"
        "**Dataset:** `hotel_booking_TPI_grupo_J.csv`  \n"
        "**Variable objetivo:** `is_canceled`  \n"
        "**Año:** 2026\n\n"
        "> Notebook **independiente y reproducible** desde cero. "
        "Sigue el patrón de la práctica de Semana 12: "
        "seleccionar datos → preparar X e y → dividir entrenamiento/prueba → "
        "entrenar → predecir → interpretar. "
        "**No** se evalúa el modelo con métricas formales (Unidad N° 6)."
    )

    add_md(
        "## 1. Objetivo de esta entrega\n\n"
        "El hotel necesita **anticipar**, al momento de registrar una reserva, "
        "si esa reserva será cancelada antes del check-in. "
        "El problema es de **clasificación supervisada**: la etiqueta "
        "`is_canceled` ya está en el dataset (`1` = cancelada, `0` = no cancelada).\n\n"
        "En esta entrega se construye un **primer modelo sencillo** "
        "(árbol de decisión de profundidad limitada), se observan predicciones "
        "frente al resultado real y se interpretan utilidades y limitaciones. "
        "El foco no es obtener el mejor modelo posible."
    )

    add_md("## 2. Entorno, carga del dataset y registro en DuckDB")

    add_code(
        "import importlib.util\n"
        "import subprocess\n"
        "import sys\n"
        "from pathlib import Path\n"
        "\n"
        "for package in ['duckdb', 'pandas', 'scikit-learn']:\n"
        "    module = 'sklearn' if package == 'scikit-learn' else package\n"
        "    if importlib.util.find_spec(module) is None:\n"
        "        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', package])\n"
        "\n"
        "import duckdb\n"
        "import pandas as pd\n"
        "from IPython.display import display\n"
        "from sklearn.model_selection import train_test_split\n"
        "from sklearn.tree import DecisionTreeClassifier, export_text\n"
        "\n"
        "CANDIDATES = [\n"
        "    Path('../datos') / 'hotel_booking_TPI_grupo_J.csv',\n"
        "    Path('datos') / 'hotel_booking_TPI_grupo_J.csv',\n"
        "    Path('hotel_booking_TPI_grupo_J.csv'),\n"
        "]\n"
        "CSV_PATH = next((p for p in CANDIDATES if p.exists()), None)\n"
        "if CSV_PATH is None:\n"
        "    raise FileNotFoundError(\n"
        "        'No se encontró hotel_booking_TPI_grupo_J.csv. '\n"
        "        'Colocá el CSV en ../datos, ./datos o junto al notebook.'\n"
        "    )\n"
        "\n"
        "con = duckdb.connect(database=':memory:')\n"
        "con.execute(\n"
        "    '''\n"
        "    CREATE OR REPLACE TABLE reservas AS\n"
        "    SELECT * FROM read_csv_auto(?, header=true)\n"
        "    ''',\n"
        "    [str(CSV_PATH.resolve())],\n"
        ")\n"
        "n_filas = con.execute('SELECT COUNT(*) FROM reservas').fetchone()[0]\n"
        "n_cols = con.execute('SELECT COUNT(*) FROM (DESCRIBE reservas)').fetchone()[0]\n"
        "print(f'CSV: {CSV_PATH.resolve()}')\n"
        "print(f'Filas cargadas en DuckDB: {n_filas:,} · columnas: {n_cols}')"
    )

    add_md(
        "## 3. Paso 1 · Preparar los datos para el modelo\n\n"
        "### 3.1 Variable objetivo y predictores\n\n"
        "La unidad de análisis es **una reserva hotelera** (una fila). "
        "La etiqueta `y` es `is_canceled`.\n\n"
        "Se usan **siete predictores** alineados con la planificación de Semana 11 "
        "y con los hallazgos del EDA (Entrega 4). "
        "`total_nights` se deriva en SQL como "
        "`stays_in_weekend_nights + stays_in_week_nights`.\n\n"
        "| Predictor | Por qué entra |\n"
        "|-----------|----------------|\n"
        "| `lead_time` | En el EDA, la mediana de anticipación fue más alta en las canceladas. |\n"
        "| `hotel` | Tasas distintas entre City Hotel y Resort Hotel. |\n"
        "| `deposit_type` | Se pacta al reservar; en este subset las tasas difieren fuerte (`Non Refund` vs `No Deposit`). |\n"
        "| `market_segment` | Segmentos con tasas y volumen suficientes. |\n"
        "| `total_nights` | Duración pedida, conocida al registrar; candidata en el EDA. |\n"
        "| `previous_cancellations` | Historial previo, si el hotel ya lo tiene. |\n"
        "| `customer_type` | Tipo de cliente identificado al tomar la reserva. |\n\n"
        "Criterio de control: **¿el hotel ya conocería este dato cuando recibe la reserva?** "
        "Si el valor se genera o se actualiza después, no entra."
    )

    add_md(
        "### 3.2 Variables que no se usan (fuga o falta de señal)\n\n"
        "- **`booking_id`:** identificador de la reserva. No describe un patrón repetible.\n"
        "- **`assigned_room_type`:** puede asignarse o cambiarse **después** del registro. "
        "Al alta el dato disponible es `reserved_room_type`. Usar la habitación finalmente "
        "asignada sería **fuga de información** (*data leakage*).\n"
        "- **`booking_changes`:** cuenta cambios posteriores. Ese valor no está cerrado "
        "cuando acaba de registrarse la reserva.\n"
        "- **`is_canceled`:** es la respuesta que se quiere anticipar; no puede ser predictora.\n"
        "- **`agent` / `company`:** muchos nulos en el subset; no se usan en este primer modelo."
    )

    add_code(
        "df = con.sql('''\n"
        "SELECT\n"
        "    is_canceled AS objetivo,\n"
        "    lead_time,\n"
        "    hotel,\n"
        "    deposit_type,\n"
        "    market_segment,\n"
        "    stays_in_weekend_nights + stays_in_week_nights AS total_nights,\n"
        "    previous_cancellations,\n"
        "    customer_type\n"
        "FROM reservas\n"
        "''').df()\n"
        "\n"
        "con.register('modelo_df', df)\n"
        "print('Filas para el modelo:', len(df))\n"
        "print('Columnas:', list(df.columns))\n"
        "df.head()"
    )

    add_md(
        "### 3.3 Valores faltantes y variables categóricas\n\n"
        "Antes de entrenar hay que revisar nulos y el tipo de cada predictor. "
        "Las categóricas (`hotel`, `deposit_type`, `market_segment`, `customer_type`) "
        "se convertirán a dummies **después** de partir train/test, usando solo "
        "las categorías del entrenamiento."
    )

    add_code(
        "nulos = con.sql('''\n"
        "SELECT\n"
        "    COUNT(*) AS filas,\n"
        "    SUM(CASE WHEN objetivo IS NULL THEN 1 ELSE 0 END) AS nulos_objetivo,\n"
        "    SUM(CASE WHEN lead_time IS NULL THEN 1 ELSE 0 END) AS nulos_lead_time,\n"
        "    SUM(CASE WHEN hotel IS NULL THEN 1 ELSE 0 END) AS nulos_hotel,\n"
        "    SUM(CASE WHEN deposit_type IS NULL THEN 1 ELSE 0 END) AS nulos_deposit,\n"
        "    SUM(CASE WHEN market_segment IS NULL THEN 1 ELSE 0 END) AS nulos_segment,\n"
        "    SUM(CASE WHEN total_nights IS NULL THEN 1 ELSE 0 END) AS nulos_nights,\n"
        "    SUM(CASE WHEN previous_cancellations IS NULL THEN 1 ELSE 0 END) AS nulos_prev_cancel,\n"
        "    SUM(CASE WHEN customer_type IS NULL THEN 1 ELSE 0 END) AS nulos_customer\n"
        "FROM modelo_df\n"
        "''').df()\n"
        "display(nulos)\n"
        "\n"
        "print('\\nTipos:')\n"
        "print(df.dtypes)\n"
        "print('\\nBalance de la etiqueta:')\n"
        "print(df['objetivo'].value_counts().sort_index())"
    )

    add_md(
        "## 4. Paso 2 · Partición entrenamiento / prueba\n\n"
        "- `test_size = 0.30` y `random_state = 42` para que la partición sea **reproducible**.\n"
        "- `stratify=y` conserva la proporción de canceladas en ambos conjuntos.\n"
        "- Si hubiera nulos numéricos, se completarían con la **mediana del entrenamiento** "
        "y se aplicaría el mismo valor al conjunto de prueba. Usar la mediana del dataset "
        "completo sería fuga de información.\n"
        "- Las dummies se arman con las categorías de **train**; el test se reindexa "
        "a esas columnas (`fill_value=0`) para alinear el esquema."
    )

    add_code(
        "y = df['objetivo'].astype(int)\n"
        "X = df.drop(columns='objetivo')\n"
        "\n"
        "CATS = ['hotel', 'deposit_type', 'market_segment', 'customer_type']\n"
        "NUMS = ['lead_time', 'total_nights', 'previous_cancellations']\n"
        "\n"
        "X_train, X_test, y_train, y_test = train_test_split(\n"
        "    X, y,\n"
        "    test_size=0.30,\n"
        "    random_state=42,\n"
        "    stratify=y,\n"
        ")\n"
        "\n"
        "X_train = X_train.copy()\n"
        "X_test = X_test.copy()\n"
        "\n"
        "# Imputación numérica solo con estadísticas de entrenamiento (aunque en este\n"
        "# subset los predictores elegidos no tienen nulos: queda el procedimiento).\n"
        "medianas_train = X_train[NUMS].median()\n"
        "X_train[NUMS] = X_train[NUMS].fillna(medianas_train)\n"
        "X_test[NUMS] = X_test[NUMS].fillna(medianas_train)\n"
        "\n"
        "X_train = pd.get_dummies(X_train, columns=CATS, drop_first=False)\n"
        "X_test = pd.get_dummies(X_test, columns=CATS, drop_first=False)\n"
        "X_test = X_test.reindex(columns=X_train.columns, fill_value=0)\n"
        "\n"
        "print('X_train:', X_train.shape, '| y_train:', y_train.shape)\n"
        "print('X_test :', X_test.shape, '| y_test :', y_test.shape)\n"
        "print('Canceladas en train:', int(y_train.sum()), f'({y_train.mean():.1%})')\n"
        "print('Canceladas en test :', int(y_test.sum()), f'({y_test.mean():.1%})')\n"
        "print('Columnas después de dummies:')\n"
        "print(list(X_train.columns))"
    )

    add_md(
        "## 5. Paso 3 · Entrenar un árbol de decisión sencillo\n\n"
        "Se usa `DecisionTreeClassifier` con `max_depth=3` y `random_state=42`, "
        "igual que en la práctica de Semana 12. La profundidad limitada facilita "
        "leer las reglas; no busca el máximo ajuste."
    )

    add_code(
        "modelo = DecisionTreeClassifier(max_depth=3, random_state=42)\n"
        "modelo.fit(X_train, y_train)\n"
        "\n"
        "predicciones = modelo.predict(X_test)\n"
        "probabilidad = modelo.predict_proba(X_test)[:, 1]\n"
        "\n"
        "print('Modelo entrenado.')\n"
        "print('\\nReglas del árbol (profundidad 3):')\n"
        "print(export_text(modelo, feature_names=list(X_train.columns), decimals=2))"
    )

    add_md(
        "## 6. Paso 4 · Observar predicciones frente al resultado real\n\n"
        "Se comparan **12 casos de prueba**. La probabilidad estimada no es una verdad "
        "ni una orden de acción: indica cuánto se inclina el modelo por la clase 1. "
        "Valores cercanos a 0,5 marcan predicciones menos definidas.\n\n"
        "Todavía **no** se reportan accuracy, precision, recall ni F1."
    )

    add_code(
        "resultados = X_test.copy()\n"
        "resultados['resultado_real'] = y_test.to_numpy()\n"
        "resultados['prediccion'] = predicciones\n"
        "resultados['probabilidad_clase_1'] = probabilidad.round(3)\n"
        "resultados['coincide'] = resultados['resultado_real'] == resultados['prediccion']\n"
        "resultados['distancia_a_0_5'] = (resultados['probabilidad_clase_1'] - 0.5).abs()\n"
        "\n"
        "con.register('predicciones', resultados.reset_index(drop=True))\n"
        "\n"
        "muestra = con.sql('''\n"
        "SELECT\n"
        "    resultado_real,\n"
        "    prediccion,\n"
        "    probabilidad_clase_1,\n"
        "    coincide,\n"
        "    CASE\n"
        "        WHEN probabilidad_clase_1 < 0.30 THEN 'Probabilidad baja'\n"
        "        WHEN probabilidad_clase_1 > 0.70 THEN 'Probabilidad alta'\n"
        "        ELSE 'Caso incierto'\n"
        "    END AS lectura_inicial\n"
        "FROM predicciones\n"
        "ORDER BY distancia_a_0_5 ASC\n"
        "LIMIT 12\n"
        "''').df()\n"
        "display(muestra)"
    )

    add_code(
        "extremos = con.sql('''\n"
        "(SELECT resultado_real, prediccion, probabilidad_clase_1, coincide\n"
        " FROM predicciones ORDER BY probabilidad_clase_1 ASC LIMIT 4)\n"
        "UNION ALL\n"
        "(SELECT resultado_real, prediccion, probabilidad_clase_1, coincide\n"
        " FROM predicciones ORDER BY probabilidad_clase_1 DESC LIMIT 4)\n"
        "''').df()\n"
        "print('Casos con probabilidad más baja y más alta:')\n"
        "display(extremos)\n"
        "\n"
        "desacuerdos = con.sql('''\n"
        "SELECT resultado_real, prediccion, COUNT(*) AS cantidad\n"
        "FROM predicciones\n"
        "GROUP BY resultado_real, prediccion\n"
        "ORDER BY resultado_real, prediccion\n"
        "''').df()\n"
        "print('\\nConteo descriptivo real vs predicción (sin métricas de evaluación):')\n"
        "display(desacuerdos)"
    )

    add_md(
        "## 7. Paso 5 · Interpretación, utilidad y limitaciones\n\n"
        "### 7.1 Qué representa `y` y qué hace el modelo\n\n"
        "`y` (`objetivo`) vale **1** si la reserva fue cancelada y **0** si se concretó. "
        "El árbol asigna a cada reserva de prueba una **categoría predicha** y una "
        "**probabilidad** de clase 1. La categoría es un recorte de esa probabilidad "
        "(umbral 0,5 por defecto); la probabilidad muestra cuán definido está el recorte.\n\n"
        "Las variables categóricas se transformaron a dummies porque el árbol de "
        "`scikit-learn` trabaja con entradas numéricas. Sin esa conversión el entrenamiento "
        "no sería válido con este estimador.\n\n"
        "### 7.2 Lectura de los casos observados\n\n"
        "En la muestra ordenada por cercanía a 0,5 aparecen reservas **inciertas**: "
        "el modelo no se inclina con fuerza. Actuar ahí (por ejemplo, ofrecer un beneficio "
        "de retención o bloquear un overbooking) exigiría más contexto: costo de "
        "equivocarse, política comercial y datos que el modelo no ve "
        "(motivo de viaje, cambios de tarifa, contacto posterior).\n\n"
        "La primera regla del árbol separa `deposit_type_Non Refund`. En este subset "
        "esa categoría tiene una tasa de cancelación cercana al 100 %, así que el "
        "modelo predice clase 1 ahí. Es una **asociación muy fuerte**, no una prueba "
        "de que el depósito no reembolsable **cause** la cancelación: puede mezclarse "
        "con canal, tipo de cliente o con la forma en que se registran esas reservas. "
        "Actuar forzando depósitos no reembolsables a partir de esta rama sería un "
        "salto causal injustificado.\n\n"
        "Fuera de `Non Refund`, el árbol de profundidad 3 tiende a predecir clase 0 "
        "(no cancelada), coherente con que esa es la mayoría del dataset (~63 %). "
        "Por eso aparecen desacuerdos: reservas `No Deposit` que sí se cancelaron "
        "quedan clasificadas como 0. El desacuerdo no indica que el procedimiento "
        "esté mal ejecutado; muestra que un árbol pequeño deja casos fuera.\n\n"
        "### 7.3 Utilidad inicial para el hotel\n\n"
        "El modelo puede servir como **señal temprana** al registrar la reserva: "
        "priorizar seguimiento en casos de alta probabilidad y no tratar igual a "
        "todas las reservas. Todavía **no** justifica una política automática "
        "(cobrar depósitos, rechazar segmentos, overbooking) sin revisar costos, "
        "capacidad operativa y sesgos.\n\n"
        "### 7.4 Limitaciones (al menos dos)\n\n"
        "1. **Información que el dataset no registra.** El CSV no incluye, entre otras "
        "cosas, el motivo de la estadía, quejas, cambios de precio posteriores, "
        "competencia local ni el contacto del huésped después de reservar. "
        "Esas omisiones limitan tanto la predicción como cualquier acción.\n"
        "2. **Contexto histórico y cambio de política.** El modelo se entrenó con "
        "reservas de este subset (comisión 10, Grupo J). Si el hotel cambia tarifas, "
        "depósitos o canales, o si entra un período distinto, las reglas pueden "
        "dejar de servir. Los datos históricos no garantizan el mismo patrón a futuro.\n"
        "3. **Errores con costos distintos.** Predecir cancelación cuando la reserva "
        "se iba a concretar (falsa alarma) no cuesta lo mismo que no detectar una "
        "cancelación real (pérdida de ocupación o de ingreso). Esta entrega no elige "
        "un umbral ni evalúa esos costos.\n"
        "4. **Árbol pequeño y sin evaluación formal.** `max_depth=3` facilita la lectura "
        "y, fuera de `Non Refund`, se queda en la clase mayoritaria. No se reportan "
        "métricas: observar aciertos puntuales **no** equivale a validar el modelo "
        "(Unidad N° 6).\n"
        "5. **Asociación, no causa.** Que `Non Refund` prediga bien cancelación en este "
        "CSV no autoriza a usarlo como palanca comercial. Cambiar la política de "
        "depósitos podría alterar el mix de clientes y el patrón dejaría de valer."
    )

    add_md(
        "## 8. Cierre\n\n"
        "Se recorrió el procedimiento mínimo de la Entrega 5 sobre "
        "`hotel_booking_TPI_grupo_J.csv` (comisión 10, Grupo J):\n\n"
        "1. Predictores disponibles al registrar la reserva; se excluyeron variables "
        "con riesgo de fuga (`assigned_room_type`, `booking_changes`) y el identificador.\n"
        "2. Partición train/test reproducible; imputación y dummies **solo** con "
        "información de entrenamiento.\n"
        "3. Árbol de decisión de profundidad 3.\n"
        "4. Predicciones en prueba, comparadas con el resultado real.\n"
        "5. Interpretación, utilidad inicial y limitaciones.\n\n"
        "La evaluación formal con métricas queda para la **Unidad N° 6**."
    )

    add_code("con.close()\nprint('Conexión DuckDB cerrada.')")

    NB_DIR.mkdir(parents=True, exist_ok=True)
    write_nb(NB_DIR / "Viruel_Nicolas_10_Entrega5.ipynb", cells)


def copy_dataset() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    NB_DIR.mkdir(parents=True, exist_ok=True)
    TPI_DIR.mkdir(parents=True, exist_ok=True)
    src = next((p for p in HOTEL_CANDIDATES if p.exists()), None)
    if src is None:
        raise FileNotFoundError("No se encontró hotel_booking_TPI_grupo_J.csv en semanas previas.")
    dest = DATA_DIR / src.name
    shutil.copy2(src, dest)
    print(f"Copiado: {dest}")


def main() -> None:
    copy_dataset()
    build_tpi_entrega5()


if __name__ == "__main__":
    main()
