from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot Naive vs MRV comparison from benchmark_results.json"
    )
    parser.add_argument(
        "benchmark_file",
        type=Path,
        help="Path to benchmark_results.json",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("analysis/benchmark_plot.png"),
        help="Base output image path",
    )
    return parser.parse_args()


def load_and_group(path: Path):
    data = json.loads(path.read_text())

    grouped = {}

    for entry in data:
        puzzle = entry["puzzle"]
        strategy = entry["strategy"]

        if puzzle not in grouped:
            grouped[puzzle] = {}

        grouped[puzzle][strategy] = entry

    return grouped


def split_by_difficulty(grouped):
    """
    Splits puzzles into difficulty groups based on first number:
    1 = easy, 2 = medium, 3 = hard, 4 = evil
    """
    difficulty_map = {
        "1": "easy",
        "2": "medium",
        "3": "hard",
        "4": "evil",
    }

    split = {
        "easy": {},
        "medium": {},
        "hard": {},
        "evil": {},
    }

    for puzzle, data in grouped.items():
        difficulty_key = puzzle.split("_")[0]  # "1", "2", etc.
        difficulty = difficulty_map.get(difficulty_key)

        if difficulty:
            split[difficulty][puzzle] = data

    return split


def extract_metrics(grouped):
    labels = []

    naive_nodes, mrv_nodes = [], []
    naive_backtracks, mrv_backtracks = [], []
    naive_times, mrv_times = [], []

    for puzzle in sorted(grouped.keys()):
        strategies = grouped[puzzle]

        if "Naive" not in strategies or "MRV" not in strategies:
            continue

        naive = strategies["Naive"]
        mrv = strategies["MRV"]

        labels.append(puzzle)

        naive_nodes.append(naive["nodes_expanded"])
        mrv_nodes.append(mrv["nodes_expanded"])

        naive_backtracks.append(naive["backtracks"])
        mrv_backtracks.append(mrv["backtracks"])

        naive_times.append(naive["elapsed_seconds"])
        mrv_times.append(mrv["elapsed_seconds"])

    return (
        labels,
        naive_nodes, mrv_nodes,
        naive_backtracks, mrv_backtracks,
        naive_times, mrv_times
    )


def plot_comparison(
    labels,
    naive_nodes, mrv_nodes,
    naive_backtracks, mrv_backtracks,
    naive_times, mrv_times,
    out: Path,
    title_suffix: str = ""
):
    x = list(range(len(labels)))
    width = 0.4

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # --- Nodes Expanded ---
    axes[0].bar([i - width/2 for i in x], naive_nodes, width, label="Naive")
    axes[0].bar([i + width/2 for i in x], mrv_nodes, width, label="MRV")
    axes[0].set_title(f"Nodes Expanded ({title_suffix})")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(labels, rotation=30)
    axes[0].legend()

    # --- Backtracks ---
    axes[1].bar([i - width/2 for i in x], naive_backtracks, width, label="Naive")
    axes[1].bar([i + width/2 for i in x], mrv_backtracks, width, label="MRV")
    axes[1].set_title(f"Backtracks ({title_suffix})")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels, rotation=30)
    axes[1].legend()

    # --- Time ---
    axes[2].bar([i - width/2 for i in x], naive_times, width, label="Naive")
    axes[2].bar([i + width/2 for i in x], mrv_times, width, label="MRV")
    axes[2].set_title(f"Elapsed Time ({title_suffix})")
    axes[2].set_xticks(x)
    axes[2].set_xticklabels(labels, rotation=30)
    axes[2].legend()

    fig.tight_layout()

    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)

    print(f"Saved plot to {out}")


def main():
    args = parse_args()

    grouped = load_and_group(args.benchmark_file)
    split = split_by_difficulty(grouped)

    base = args.out

    for difficulty, puzzles in split.items():
        if not puzzles:
            continue

        (
            labels,
            naive_nodes, mrv_nodes,
            naive_backtracks, mrv_backtracks,
            naive_times, mrv_times
        ) = extract_metrics(puzzles)

        out_path = base.with_name(f"{base.stem}_{difficulty}{base.suffix}")

        plot_comparison(
            labels,
            naive_nodes, mrv_nodes,
            naive_backtracks, mrv_backtracks,
            naive_times, mrv_times,
            out_path,
            title_suffix=difficulty.capitalize()
        )


if __name__ == "__main__":
    main()