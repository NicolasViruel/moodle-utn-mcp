"""Genera gantt-u4.png para el TP Unidad 4 (matplotlib)."""
from __future__ import annotations

from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
except ImportError:
    raise SystemExit("Instalá matplotlib: pip install matplotlib")

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "gantt-u4.png"

# (nombre, inicio, duración, crítico)
TASKS = [
    ("A", 0, 3, True),
    ("B", 3, 4, True),
    ("C", 7, 5, True),
    ("D", 3, 2, False),
    ("E", 12, 4, True),
    ("F", 16, 3, True),
]
MILESTONES = [(3, "H1"), (12, "H2"), (19, "H3")]


def main() -> None:
    fig, ax = plt.subplots(figsize=(12, 4))
    colors = {True: "#c0392b", False: "#3498db"}
    for i, (name, start, dur, crit) in enumerate(TASKS):
        ax.barh(
            i,
            dur,
            left=start,
            height=0.5,
            color=colors[crit],
            edgecolor="black",
        )
        ax.text(start + dur / 2, i, name, ha="center", va="center", color="white", fontweight="bold")

    for day, label in MILESTONES:
        ax.axvline(day, color="green", linestyle="--", linewidth=1.2, alpha=0.8)
        ax.text(day, len(TASKS) - 0.2, label, color="green", fontsize=9, ha="center")

    ax.set_yticks(range(len(TASKS)))
    ax.set_yticklabels([t[0] for t in TASKS])
    ax.set_xlabel("Día")
    ax.set_xlim(0, 19)
    ax.set_xticks(range(0, 20))
    ax.set_title("Gantt – Módulo software (Unidad 4 GDS)")
    ax.invert_yaxis()
    ax.grid(axis="x", alpha=0.3)
    crit_patch = mpatches.Patch(color=colors[True], label="Camino crítico")
    holg_patch = mpatches.Patch(color=colors[False], label="Con holgura")
    ax.legend(handles=[crit_patch, holg_patch], loc="lower right")
    fig.tight_layout()
    fig.savefig(OUT, dpi=150)
    print(f"Generado: {OUT}")


if __name__ == "__main__":
    main()
