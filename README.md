# Sudoku Solver

A modular Sudoku solving project using constraint validation + backtracking search, with built-in metrics for analysis and report visuals.

## Project Structure

```text
sudoku_solver/
├── src/
│   ├── __init__.py
│   ├── board.py
│   ├── constraints.py
│   ├── solver.py
│   └── main.py
├── data/
│   ├── 1_easy_01.txt ... 1_easy_03.txt
│   ├── 2_medium_01.txt ... 2_medium_02.txt
│   ├── 3_hard_01.txt ... 3_hard_03.txt
│   └── 4_evil_01.txt
├── analysis/
│   ├── benchmark.py
│   └── visualizer.py
├── requirements.txt
└── README.md
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run Solver

```bash
python -m src.main data/1_easy_01.txt
python -m src.main data/3_hard_01.txt --metrics-out analysis/hard_metrics.json
```

## Run Benchmark (Naive vs MRV across all puzzles)

```bash
python -m analysis.benchmark --out analysis/benchmark_results.json
```

## Generate Metrics Plot

```bash
python analysis/visualizer.py analysis/easy_metrics.json analysis/hard_metrics.json --out analysis/metrics_plot.png
```

## Notes

- Use `0` or `.` for empty cells in puzzle files.
- Solver tracks `nodes_expanded`, `backtracks`, and `elapsed_seconds`.
- Solver supports Naive (first-empty) and MRV (minimum remaining values) variable selection via `use_mrv` flag.
- Benchmark compares both strategies with a configurable timeout (`--timeout`, default 5s).
- Validation logic is isolated in `src/constraints.py` so teammates can iterate independently.
