from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

Grid = list[list[int]]


@dataclass(slots=True)
class Board:
    grid: Grid

    @classmethod
    def from_file(cls, file_path: str | Path) -> "Board":
        lines = [line.strip() for line in Path(file_path).read_text().splitlines() if line.strip()]
        if len(lines) != 9:
            raise ValueError("Puzzle must have exactly 9 non-empty lines.")

        grid: Grid = []
        for line in lines:
            if len(line) != 9:
                raise ValueError("Each puzzle line must contain exactly 9 characters.")
            row = []
            for char in line:
                if char in {".", "0"}:
                    row.append(0)
                elif char.isdigit() and "1" <= char <= "9":
                    row.append(int(char))
                else:
                    raise ValueError("Puzzle characters must be 0, ., or 1-9.")
            grid.append(row)
        return cls(grid=grid)

    def copy(self) -> "Board":
        return Board([row[:] for row in self.grid])

    def is_complete(self) -> bool:
        return all(value != 0 for row in self.grid for value in row)

    def find_empty(self) -> Optional[tuple[int, int]]:
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] == 0:
                    return r, c
        return None

    def row_values(self, row: int) -> Iterable[int]:
        return self.grid[row]

    def col_values(self, col: int) -> Iterable[int]:
        for row in range(9):
            yield self.grid[row][col]

    def box_values(self, row: int, col: int) -> Iterable[int]:
        start_r = (row // 3) * 3
        start_c = (col // 3) * 3
        for r in range(start_r, start_r + 3):
            for c in range(start_c, start_c + 3):
                yield self.grid[r][c]

    def domain_for(self, row: int, col: int) -> set[int]:
        if self.grid[row][col] != 0:
            return set()
        used = set(self.row_values(row)) | set(self.col_values(col)) | set(self.box_values(row, col))
        return {num for num in range(1, 10) if num not in used}

    def pretty(self) -> str:
        chunks = []
        for r, row in enumerate(self.grid):
            values = [str(v) if v != 0 else "." for v in row]
            chunks.append(" ".join(values[0:3]) + " | " + " ".join(values[3:6]) + " | " + " ".join(values[6:9]))
            if r in {2, 5}:
                chunks.append("-" * 21)
        return "\n".join(chunks)

    def __str__(self) -> str:
        return self.pretty()
