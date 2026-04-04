# Project Status & Next Steps (Group 7)

Course: COSC 4368 (Tue/Thu 2:30-4:00p, SEC 103)  
Professor: Christoph F. Eick  
Group 7: Tommy Truong, Nehaa Balaji, Charles McCallum, Rindy Tuy, Linh Lam, Alejandro Cortes

## 1) Project Goal

Build a system that solves Sudoku-style problems by modeling Sudoku as a Constraint Satisfaction Problem (CSP), starting with a correct baseline and then improving/benchmarking it.

Core idea:
- Represent board state and variable domains.
- Enforce constraints (row/column/3x3 uniqueness).
- Use search (backtracking) with pruning.
- Track metrics for analysis/report visuals.

## 2) What is already done (Current State)

The baseline solver is complete and runnable.

Implemented now:
- `src/board.py`
  - 9x9 board representation
  - puzzle file loading (`0` or `.` = empty)
  - helper methods (`row_values`, `col_values`, `box_values`, domain calculation)
  - board pretty-print output
- `src/constraints.py`
  - row/column/box duplicate checks
  - move-level validation (`is_move_valid`)
  - board-level validity check (`is_board_valid`)
- `src/solver.py`
  - recursive backtracking search
  - switchable variable selection: Naive (first empty) or MRV (smallest domain)
  - metrics tracking: `nodes_expanded`, `backtracks`, `elapsed_seconds`
- `src/main.py`
  - CLI entrypoint for solving puzzle files
  - optional JSON metrics output
- `data/`
  - 9 puzzles across 4 difficulty tiers (easy, medium, hard, evil)
  - named with numeric prefix so they sort easiest-to-hardest
- `analysis/benchmark.py`
  - runs all puzzles with both Naive and MRV strategies
  - per-puzzle timeout (default 5s), prints comparison table, saves JSON
- `analysis/visualizer.py`
  - plots metrics JSON files for report charts

Verified run:
- `python3 -m src.main data/1_easy_01.txt`
- `python3 -m analysis.benchmark`
- Result: all puzzles solved with MRV; Naive times out on hard/evil.


## 3) CLI Commands

From `sudoku_solver/`:

- Solve a puzzle:
  - `python3 -m src.main data/1_easy_01.txt`
- Solve + save metrics:
  - `python3 -m src.main data/3_hard_01.txt --metrics-out analysis/hard_metrics.json`
- Run full benchmark (Naive vs MRV):
  - `python3 -m analysis.benchmark --out analysis/benchmark_results.json`
- Plot comparison:
  - `python3 analysis/visualizer.py analysis/easy_metrics.json analysis/hard_metrics.json --out analysis/metrics_plot.png`

## 4) Definition of Done

Minimum acceptable final submission:
- Correct solver for provided Sudoku puzzles.
- Clear CSP/backtracking explanation.
- Metrics from multiple puzzle difficulties.
- At least one comparison/analysis figure.
- Clean report
