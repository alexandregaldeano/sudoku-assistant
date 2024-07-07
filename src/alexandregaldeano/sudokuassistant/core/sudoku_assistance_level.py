from enum import IntEnum


class SudokuAssistanceLevel(IntEnum):
    NONE = 0
    LOW = 1  # Only displays the list of possibilities for each cell
    MEDIUM = 2  # Sets the value of cells with unique possibilities
    HIGH = 3  # Sets the value of cells if the value can only be in the cell
