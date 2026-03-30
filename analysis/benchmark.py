from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.board import Board
from src.solver import BacktrackingSolver

TIMEOUT_SECONDS = 5


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark Sudoku solver across puzzles.")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data"),
        help="Directory containing puzzle .txt files.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=TIMEOUT_SECONDS,
        help=f"Max seconds per solve attempt (default {TIMEOUT_SECONDS}).",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Optional path to save benchmark results as JSON.",
    )
    return parser.parse_args()


def run_benchmark(puzzle_path: Path, use_mrv: bool, timeout: int) -> dict:
    board = Board.from_file(puzzle_path)
    solver = BacktrackingSolver(use_mrv=use_mrv, timeout=timeout)
    solved = solver.solve(board)

    return {
        "solved": solved,
        "timed_out": solver.metrics.timed_out,
        "nodes_expanded": solver.metrics.nodes_expanded,
        "backtracks": solver.metrics.backtracks,
        "elapsed_seconds": solver.metrics.elapsed_seconds,
    }


def main() -> None:
    args = parse_args()
    puzzles = sorted(args.data_dir.glob("*.txt"))

    if not puzzles:
        print(f"No puzzle files found in {args.data_dir}")
        return

    results = []

    header = f"{'Puzzle':<18} {'Strategy':<14} {'Result':<12} {'Nodes':>8} {'Backtracks':>12} {'Time (s)':>10}"
    print(header)
    print("-" * len(header))

    for puzzle_path in puzzles:
        for use_mrv in [False, True]:
            strategy = "MRV" if use_mrv else "Naive"
            metrics = run_benchmark(puzzle_path, use_mrv, args.timeout)

            if metrics["timed_out"]:
                result = "TIMEOUT"
            elif metrics["solved"]:
                result = "Solved"
            else:
                result = "No soln"

            print(
                f"{puzzle_path.stem:<18} {strategy:<14} "
                f"{result:<12} "
                f"{metrics['nodes_expanded']:>8} "
                f"{metrics['backtracks']:>12} "
                f"{metrics['elapsed_seconds']:>10.4f}"
            )

            results.append({
                "puzzle": puzzle_path.stem,
                "strategy": strategy,
                **metrics,
            })

    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(results, indent=2))
        print(f"\nResults written to {args.out}")


if __name__ == "__main__":
    main()
