from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.board import Board
from src.solver import BacktrackingSolver


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Solve a Sudoku puzzle with backtracking.")
    parser.add_argument("puzzle", type=Path, help="Path to a text file with a 9x9 puzzle.")
    parser.add_argument(
        "--metrics-out",
        type=Path,
        default=None,
        help="Optional path to save metrics JSON.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    board = Board.from_file(args.puzzle)

    solver = BacktrackingSolver()
    solved = solver.solve(board)

    print("Input puzzle:")
    print(Board.from_file(args.puzzle))
    print("\nSolved:" if solved else "\nNo solution found.")
    print(board)

    metrics = {
        "nodes_expanded": solver.metrics.nodes_expanded,
        "backtracks": solver.metrics.backtracks,
        "elapsed_seconds": solver.metrics.elapsed_seconds,
    }
    print("\nMetrics:")
    print(json.dumps(metrics, indent=2))

    if args.metrics_out is not None:
        args.metrics_out.parent.mkdir(parents=True, exist_ok=True)
        args.metrics_out.write_text(json.dumps(metrics, indent=2))
        print(f"\nMetrics written to {args.metrics_out}")


if __name__ == "__main__":
    main()
