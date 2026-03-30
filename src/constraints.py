from __future__ import annotations

from src.board import Board


def has_duplicates(values: list[int]) -> bool:
    items = [v for v in values if v != 0]
    return len(items) != len(set(items))


def is_row_valid(board: Board, row: int) -> bool:
    return not has_duplicates(list(board.row_values(row)))


def is_col_valid(board: Board, col: int) -> bool:
    return not has_duplicates(list(board.col_values(col)))


def is_box_valid(board: Board, row: int, col: int) -> bool:
    return not has_duplicates(list(board.box_values(row, col)))


def is_move_valid(board: Board, row: int, col: int, value: int) -> bool:
    current = board.grid[row][col]
    board.grid[row][col] = value
    valid = is_row_valid(board, row) and is_col_valid(board, col) and is_box_valid(board, row, col)
    board.grid[row][col] = current
    return valid


def is_board_valid(board: Board) -> bool:
    for i in range(9):
        if not is_row_valid(board, i) or not is_col_valid(board, i):
            return False
    for row in (0, 3, 6):
        for col in (0, 3, 6):
            if not is_box_valid(board, row, col):
                return False
    return True
