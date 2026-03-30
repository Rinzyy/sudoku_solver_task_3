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
  - next-variable selection using smallest current domain (MRV-style)
  - metrics tracking: `nodes_expanded`, `backtracks`, `elapsed_seconds`
- `src/main.py`
  - CLI entrypoint for solving puzzle files
  - optional JSON metrics output
- `data/`
  - `test_easy.txt`, `test_hard.txt`
- `analysis/visualizer.py`
  - plots metrics JSON files for report charts

Verified run:
- `python3 -m src.main data/test_easy.txt`
- Result: solved successfully.

## 3) What is NOT done yet (Open Work)

Recommended next steps:
- Run/record metrics on multiple puzzles (easy + hard + additional puzzles).
- Add comparison modes (example: plain backtracking vs MRV + additional pruning).
- Build a small experiment pipeline to produce clean tables/charts for the report.
- Write final report sections (method, experiments, results, discussion).

## 4) CLI Commands

From `sudoku_solver/`:

- Solve easy:
  - `python3 -m src.main data/test_easy.txt`
- Solve hard + save metrics:
  - `python3 -m src.main data/test_hard.txt --metrics-out analysis/hard_metrics.json`
- Plot comparison:
  - `python3 analysis/visualizer.py analysis/easy_metrics.json analysis/hard_metrics.json --out analysis/metrics_plot.png`

## 5) Definition of Done

Minimum acceptable final submission:
- Correct solver for provided Sudoku puzzles.
- Clear CSP/backtracking explanation.
- Metrics from multiple puzzle difficulties.
- At least one comparison/analysis figure.
- Clean report
