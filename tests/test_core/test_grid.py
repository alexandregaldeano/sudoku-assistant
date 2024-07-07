from unittest import TestCase

from alexandregaldeano.sudokuassistant.core.grid import Grid


class GridTest(TestCase):
    def setUp(self):
        self.grid: Grid[int | None] = Grid(2, 3, default_factory=lambda r, c: 2 * r + c + 1)

    def test_default(self):
        self.assertEqual(self.grid._values, [[1, 2], [3, 4], [5, 6]])

    def test_dimensions(self):
        self.assertEqual(self.grid.width, 2)
        self.assertEqual(self.grid.height, 3)

    def test_indices(self):
        self.assertEqual(list(self.grid.row_indices), [0, 1, 2])
        self.assertEqual(list(self.grid.column_indices), [0, 1])

    def test_rows(self):
        self.assertEqual(self.grid.rows, [[1, 2], [3, 4], [5, 6]])

    def test_columns(self):
        self.assertEqual(self.grid.columns, [[1, 3, 5], [2, 4, 6]])

    def test_values(self):
        self.assertEqual(self.grid.values, [1, 2, 3, 4, 5, 6])

    def test_getitem(self):
        self.assertEqual(self.grid[0, 0], 1)
        self.assertEqual(self.grid[0, 1], 2)
        self.assertEqual(self.grid[1, 0], 3)
        self.assertEqual(self.grid[1, 1], 4)
        self.assertEqual(self.grid[2, 0], 5)
        self.assertEqual(self.grid[2, 1], 6)

        with self.assertRaises(IndexError):
            self.grid[0, 2]
        with self.assertRaises(IndexError):
            self.grid[3, 0]

    def test_setitem(self):
        self.grid[0, 0] = -1
        self.grid[0, 1] = -2
        self.grid[1, 0] = -3
        self.grid[1, 1] = -4
        self.grid[2, 0] = -5
        self.grid[2, 1] = -6

        self.assertEqual(self.grid._values, [[-1, -2], [-3, -4], [-5, -6]])

        with self.assertRaises(IndexError):
            self.grid[0, 2] = -1
        with self.assertRaises(IndexError):
            self.grid[3, 0] = -2

    def test_get_row(self):
        self.assertEqual(self.grid.get_row(0), [1, 2])
        self.assertEqual(self.grid.get_row(1), [3, 4])
        self.assertEqual(self.grid.get_row(2), [5, 6])

    def test_get_column(self):
        self.grid._values = [[1, 2], [3, 4], [5, 6]]
        self.assertEqual(self.grid.get_column(0), [1, 3, 5])
        self.assertEqual(self.grid.get_column(1), [2, 4, 6])
