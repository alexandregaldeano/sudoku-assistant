from typing import Tuple, TypeVar, Generic, List, Callable

T = TypeVar('T')

type GridLocation = Tuple[int, int]  # (row_index, column_index)
type GridFactory[T] = Callable[[int, int], T]  # (row_index, column_index) -> T


class Grid(Generic[T]):
    def __init__(self, width: int, height: int, default_factory: GridFactory[T]):
        self._width = width
        self._height = height
        self._values: List[List[T]] = [
            [
                default_factory(row, column)
                for column in range(width)
            ]
            for row in range(height)
        ]

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def row_indices(self):
        return range(self._height)

    @property
    def rows(self):
        return [self.get_row(row_index) for row_index in self.row_indices]

    @property
    def column_indices(self):
        return range(self._width)

    @property
    def columns(self):
        return [self.get_column(column_index) for column_index in self.column_indices]
    @property
    def values(self) -> List[T]:
        return [
            self[row_index, column_index]
            for row_index in self.row_indices
            for column_index in self.column_indices
        ]

    def __getitem__(self, key: GridLocation) -> T:
        row, column = key
        return self._values[row][column]

    def __setitem__(self, key: GridLocation, value: T):
        row, column = key
        self._values[row][column] = value

    def get_row(self, row_index: int) -> List[T]:
        return [self[row_index, column_index] for column_index in self.column_indices]

    def get_column(self, column_index: int) -> List[T]:
        return [self[row_index, column_index] for row_index in self.row_indices]
