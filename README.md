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
│   ├── test_easy.txt
│   └── test_hard.txt
├── analysis/
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
python -m src.main data/test_easy.txt --metrics-out analysis/easy_metrics.json
python -m src.main data/test_hard.txt --metrics-out analysis/hard_metrics.json
```

## Generate Metrics Plot

```bash
python analysis/visualizer.py analysis/easy_metrics.json analysis/hard_metrics.json --out analysis/metrics_plot.png
```

## Notes

- Use `0` or `.` for empty cells in puzzle files.
- Solver tracks `nodes_expanded`, `backtracks`, and `elapsed_seconds`.
- Validation logic is isolated in `src/constraints.py` so teammates can iterate independently.
