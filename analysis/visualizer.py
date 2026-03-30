from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plot Sudoku solver metrics.")
    parser.add_argument(
        "metrics_files",
        nargs="+",
        type=Path,
        help="One or more JSON metrics files produced by src/main.py",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("analysis/metrics_plot.png"),
        help="Output image path for the chart.",
    )
    return parser.parse_args()


def load_metrics(paths: list[Path]) -> tuple[list[str], list[int], list[int], list[float]]:
    labels = []
    nodes = []
    backtracks = []
    times = []

    for path in paths:
        data = json.loads(path.read_text())
        labels.append(path.stem)
        nodes.append(int(data.get("nodes_expanded", 0)))
        backtracks.append(int(data.get("backtracks", 0)))
        times.append(float(data.get("elapsed_seconds", 0.0)))

    return labels, nodes, backtracks, times


def plot_metrics(labels: list[str], nodes: list[int], backtracks: list[int], times: list[float], out: Path) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))

    axes[0].bar(labels, nodes)
    axes[0].set_title("Nodes Expanded")
    axes[0].tick_params(axis="x", rotation=30)

    axes[1].bar(labels, backtracks)
    axes[1].set_title("Backtracks")
    axes[1].tick_params(axis="x", rotation=30)

    axes[2].bar(labels, times)
    axes[2].set_title("Elapsed Seconds")
    axes[2].tick_params(axis="x", rotation=30)

    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)
    print(f"Saved plot to {out}")


def main() -> None:
    args = parse_args()
    labels, nodes, backtracks, times = load_metrics(args.metrics_files)
    plot_metrics(labels, nodes, backtracks, times, args.out)


if __name__ == "__main__":
    main()
