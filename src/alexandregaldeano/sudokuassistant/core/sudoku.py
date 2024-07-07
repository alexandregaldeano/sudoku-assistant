import logging
import random
from typing import List, Tuple

import numpy as np

from .grid import Grid
from .sudoku_assistance_level import SudokuAssistanceLevel
from .sudoku_cell import SudokuCell
from .sudoku_cell_type import SudokuCellType

logger = logging.getLogger(__name__)


class Sudoku(Grid[SudokuCell]):
    def __init__(
        self,
        grid: Grid[int | None] = Grid(9, 9, lambda r, c: None),
        assistance_level: SudokuAssistanceLevel = SudokuAssistanceLevel.NONE):
        super().__init__(9, 9, default_factory=lambda r, c: self._default_cell_factory(r, c, grid))
        self._blocks = [self._compute_block(block_index) for block_index in self.block_indices]
        self.assistance_level = assistance_level
        self.remaining_digits = { digit: 9 for digit in range(1, 10) } 
        self.steps = 0
        self.solved = False
        self.reset_to_base()

    @staticmethod
    def _get_unique_valid_possibilities(cells: List[SudokuCell]) -> List[Tuple[SudokuCell, int]]:
        unique_valid_possibilities: List[Tuple[SudokuCell, int]] = []
        for value in range(1, 10):
            valid_cells: List[SudokuCell] = []
            for cell in cells:
                possibilities = list(cell.possibilities)
                if value in possibilities:
                    valid_cells.append(cell)
            if len(valid_cells) == 1:
                [cell] = valid_cells
                unique_valid_possibilities.append((cell, value))
        return unique_valid_possibilities

    @classmethod
    def _default_cell_factory(cls, row_index: int, column_index: int, grid: Grid[int | None]):
        value = grid[row_index, column_index]
        cell_type = SudokuCellType.BASE if value is not None else None
        return SudokuCell((row_index, column_index), value=value, cell_type=cell_type)

    @classmethod
    def from_values(cls, sudoku_values: List[int]) -> "Sudoku":
        if len(sudoku_values) != 81:
            raise ValueError(f"Invalid values list given, should have 81 elements, {len(sudoku_values)} given")
        invalid_values = set(sudoku_values) - {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
        if invalid_values:
            raise ValueError(
                f"Invalid values list given, contains the following unexpected elements: {sorted(invalid_values)}")
        grid = Grid(9, 9, lambda r, c: sudoku_values[9 * r + c] or None)
        return Sudoku(grid)

    @classmethod
    def from_template(cls, template: str, shuffle: bool) -> "Sudoku":
        template_values = np.array([
            [template_value for template_value in template_line]
            for template_line in template.split("\n") if template_line
        ])
        if not shuffle:
            template_values = template_values.flatten().tolist()
            values = [int(template_value) for template_value in template_values]
            return cls.from_values(values)
        if random.random() < 0.5:
            template_values = np.transpose(template_values)
        flip_random = random.random()
        if flip_random < 1 / 3:
            template_values = np.flipud(template_values)
        elif flip_random < 2 / 3:
            template_values = np.fliplr(template_values)
        template_values = np.rot90(template_values, int(4 * random.random()))
        template_values = template_values.flatten().tolist()
        mapping = list(range(1, 10))
        random.shuffle(mapping)
        mapping = [0, *mapping]
        values = [mapping[int(template_value)] for template_value in template_values]
        return cls.from_values(values)

    def __setitem__(self, key, value):
        raise NotImplementedError("Direct update disabled, use update_cell method instead")

    @property
    def block_indices(self):
        return {0, 1, 2, 3, 4, 5, 6, 7, 8}

    @property
    def blocks(self):
        return self._blocks.copy()

    def _compute_block(self, block_index: int) -> Grid[SudokuCell]:
        block_x = block_index // 3
        block_y = block_index % 3
        return Grid(3, 3, lambda r, c: self[r + block_x * 3, c + block_y * 3])

    def get_block(self, block_index: int) -> Grid[SudokuCell]:
        return self._blocks[block_index]

    def reset_to_base(self):
        for cell in self.values:
            if cell.cell_type != SudokuCellType.BASE:
                cell.reset()
        self.remaining_digits = { digit: 9 for digit in range(1, 10) }
        for cell in self.values:
            if cell.cell_type == SudokuCellType.BASE:
                value = cell.value
                cell.value = None
                cell.possibilities = {1, 2, 3, 4, 5, 6, 7, 8, 9}
                self._update_cell(cell.row_index, cell.column_index, value, SudokuCellType.BASE)
        self.steps = 0
        self.solved = False
        self.apply_assistance()

    def update_cell(self, row_index: int, column_index: int, value: int, cell_type: SudokuCellType):
        self._update_cell(row_index, column_index, value, cell_type)
        self.apply_assistance()

    def _update_cell(self, row_index: int, column_index: int, value: int, cell_type: SudokuCellType):
        cell = self[row_index, column_index]
        if cell.value != value and value not in cell.possibilities:
            return
        self.steps += 1
        if not self.solved and cell.value != value:
            self.remaining_digits[value] -= 1
            self.solved = all(remaining == 0 for remaining in self.remaining_digits.values())
        cell.value = value
        cell.cell_type = cell_type
        cell.possibilities.clear()
        for affected_cell in [
            *self.get_row(row_index),
            *self.get_column(column_index),
            *self.get_block(cell.block_index).values,
        ]:
            affected_cell.remove_possibility(value)
            
    def remove_possibility(self, row_index: int, column_index: int, value: int):
        if self[row_index, column_index].remove_possibility(value):
            self.steps += 1
        self.apply_assistance()
            
    def apply_assistance(self):
        while self._apply_assistance():
            logger.info("Assistance made changes, rerunning...")

    def _apply_assistance(self) -> bool:
        any_change = False
        if self.assistance_level >= SudokuAssistanceLevel.MEDIUM:
            while self._apply_unique_possibilities():
                any_change = True
        if self.assistance_level >= SudokuAssistanceLevel.HIGH:
            while self._apply_unique_valid_possibility():
                any_change = True
        return any_change

    def _apply_unique_possibilities(self) -> bool:
        cells_to_update: List[SudokuCell] = [cell for cell in self.values if len(cell.possibilities) == 1]
        for cell in cells_to_update:
            value = next(iter(cell.possibilities))
            self._update_cell(cell.row_index, cell.column_index, value, SudokuCellType.AUTO_LEVEL_1)
        return len(cells_to_update) > 0

    def _apply_unique_valid_possibility(self) -> bool:
        # List of cell and value to apply
        updates_to_apply: List[Tuple[SudokuCell, int]] = []
        cells_list_to_check = [
            *self.rows,
            *self.columns,
            *[block.values for block in self.blocks],
        ]
        for cells in cells_list_to_check:
            unique_valid_possibilities = self._get_unique_valid_possibilities(cells)
            updates_to_apply.extend(unique_valid_possibilities)
        for cell, value in updates_to_apply:
            self._update_cell(cell.row_index, cell.column_index, value, SudokuCellType.AUTO_LEVEL_2)
        return len(updates_to_apply) > 0

    def __str__(self) -> str:
        rows = self.rows
        sudoku_string = "┌───────────┬───────────┬───────────┐\n"
        sudoku_string += "\n".join([self._row_to_string(row) for row in rows[0:3]]) + "\n"
        sudoku_string += "├───────────┼───────────┼───────────┤\n"
        sudoku_string += "\n".join([self._row_to_string(row) for row in rows[3:6]]) + "\n"
        sudoku_string += "├───────────┼───────────┼───────────┤\n"
        sudoku_string += "\n".join([self._row_to_string(row) for row in rows[6:9]]) + "\n"
        sudoku_string += "└───────────┴───────────┴───────────┘\n"
        return sudoku_string

    def _row_to_string(self, row: List[SudokuCell]) -> str:
        return (
            f"│  {row[0].value or ' '}  {row[1].value or ' '}  {row[2].value or ' '}  "
            f"│  {row[3].value or ' '}  {row[4].value or ' '}  {row[5].value or ' '}  "
            f"│  {row[6].value or ' '}  {row[7].value or ' '}  {row[8].value or ' '}  │"
        )
