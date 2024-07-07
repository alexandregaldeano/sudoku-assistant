from .grid import GridLocation
from .sudoku_cell_type import SudokuCellType


class SudokuCell:
    def __init__(self, location: GridLocation, value: int | None = None, cell_type: SudokuCellType | None = None):
        self.value = value
        self._row_index = location[0]
        self._column_index = location[1]
        self._block_index = (location[0] // 3) * 3 + location[1] // 3
        self.possibilities = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.cell_type = cell_type

    @property
    def value(self) -> int | None:
        return self._value

    @value.setter
    def value(self, value: int | None):
        if value not in {None, 1, 2, 3, 4, 5, 6, 7, 8, 9}:
            raise ValueError(f"Invalid value: {value}")
        self._value = value

    @property
    def row_index(self) -> int:
        return self._row_index
    
    @property
    def column_index(self) -> int:
        return self._column_index

    @property
    def block_index(self) -> int:
        return self._block_index

    def remove_possibility(self, value: int) -> bool:
        if value not in self.possibilities:
            return False
        self.possibilities.remove(value)
        if len(self.possibilities) > 0:
            return True
        self.cell_type = SudokuCellType.ERROR
        return True

    def reset(self):
        self.value = None
        self.possibilities = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.cell_type = None
