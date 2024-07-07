from enum import IntEnum


class SudokuCellType(IntEnum):
    ERROR = -1
    BASE = 0
    USER = 1
    AUTO_LEVEL_1 = 2
    AUTO_LEVEL_2 = 3
