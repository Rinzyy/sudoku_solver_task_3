from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

from src.board import Board
from src.constraints import is_board_valid, is_move_valid


@dataclass(slots=True)
class SolverMetrics:
    nodes_expanded: int = 0
    backtracks: int = 0
    elapsed_seconds: float = 0.0


class BacktrackingSolver:
    def __init__(self) -> None:
        self.metrics = SolverMetrics()

    def solve(self, board: Board) -> bool:
        if not is_board_valid(board):
            return False

        start = perf_counter()
        solved = self._search(board)
        self.metrics.elapsed_seconds = perf_counter() - start
        return solved

    def _search(self, board: Board) -> bool:
        self.metrics.nodes_expanded += 1

        next_cell = self._select_unassigned_variable(board)
        if next_cell is None:
            return True

        row, col = next_cell
        for value in sorted(board.domain_for(row, col)):
            if not is_move_valid(board, row, col, value):
                continue

            board.grid[row][col] = value
            if self._search(board):
                return True
            board.grid[row][col] = 0

        self.metrics.backtracks += 1
        return False

    @staticmethod
    def _select_unassigned_variable(board: Board) -> tuple[int, int] | None:
        best_cell = None
        best_domain_size = 10

        for r in range(9):
            for c in range(9):
                if board.grid[r][c] != 0:
                    continue
                domain_size = len(board.domain_for(r, c))
                if domain_size < best_domain_size:
                    best_domain_size = domain_size
                    best_cell = (r, c)
                    if domain_size == 1:
                        return best_cell
        return best_cell
