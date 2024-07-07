from unittest import TestCase

from alexandregaldeano.sudokuassistant.core.sudoku_cell import SudokuCell
from alexandregaldeano.sudokuassistant.core.sudoku_cell_type import SudokuCellType


class SudokuCellTest(TestCase):
    def setUp(self):
        self.cell = SudokuCell((5, 6))

    def test_defaults(self):
        self.assertIsNone(self.cell.value)
        self.assertEqual(self.cell.possibilities, {1, 2, 3, 4, 5, 6, 7, 8, 9})
        self.assertIsNone(self.cell.cell_type)

    def test_set_invalid_value(self):
        with self.assertRaisesRegex(ValueError, "Invalid value: 10"):
            self.cell.value = 10
        with self.assertRaisesRegex(ValueError, "Invalid value: test"):
            self.cell.value = "test"
            
    def test_block_coordinates(self):
        self.assertEqual(self.cell.row_index, 5)
        self.assertEqual(self.cell.column_index, 6)
        self.assertEqual(self.cell.block_index, 5)

    def test_remove_possibility(self):
        self.cell.remove_possibility(42)
        self.assertEqual(self.cell.possibilities, {1, 2, 3, 4, 5, 6, 7, 8, 9})

        self.cell.remove_possibility(1)
        self.assertEqual(self.cell.possibilities, {2, 3, 4, 5, 6, 7, 8, 9})

        self.cell.remove_possibility(5)
        self.assertEqual(self.cell.possibilities, {2, 3, 4, 6, 7, 8, 9})

        self.cell.remove_possibility(9)
        self.assertEqual(self.cell.possibilities, {2, 3, 4, 6, 7, 8})

        self.cell.remove_possibility(2)
        self.assertEqual(self.cell.possibilities, {3, 4, 6, 7, 8})

        self.cell.remove_possibility(8)
        self.assertEqual(self.cell.possibilities, {3, 4, 6, 7})

        self.cell.remove_possibility(3)
        self.cell.remove_possibility(4)
        self.cell.remove_possibility(6)
        self.cell.remove_possibility(7)
        self.assertEqual(self.cell.possibilities, set())
        self.assertEqual(self.cell.cell_type, SudokuCellType.ERROR)

    def test_reset(self):
        self.cell.value = 5
        self.cell.possibilities = {1, 2, 3}
        self.cell.cell_type = SudokuCellType.BASE

        self.cell.reset()

        self.assertIsNone(self.cell.value)
        self.assertEqual(self.cell.possibilities, {1, 2, 3, 4, 5, 6, 7, 8, 9})
        self.assertIsNone(self.cell.cell_type)
