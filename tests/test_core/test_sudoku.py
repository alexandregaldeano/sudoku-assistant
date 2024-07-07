from unittest import TestCase, mock
from unittest.mock import MagicMock

from alexandregaldeano.sudokuassistant.core.sudoku import Sudoku
from alexandregaldeano.sudokuassistant.core.sudoku_cell_type import SudokuCellType


class SudokuTest(TestCase):
    def setUp(self):
        self.sudoku = Sudoku.from_values([
            0, 0, 1, 3, 0, 2, 0, 0, 0,
            0, 0, 3, 0, 0, 7, 0, 4, 5,
            0, 0, 7, 0, 0, 0, 0, 0, 9,
            0, 0, 6, 5, 0, 0, 0, 7, 0,
            2, 0, 0, 0, 0, 0, 0, 0, 1,
            0, 9, 0, 0, 0, 1, 4, 0, 0,
            5, 0, 0, 0, 0, 0, 9, 0, 0,
            6, 1, 0, 2, 0, 0, 8, 0, 0,
            0, 0, 0, 9, 0, 8, 5, 0, 0,
        ])

    def test_from_values(self):
        self.assertEqual(self.sudoku[0, 0].value, None)
        self.assertEqual(self.sudoku[0, 1].value, None)
        self.assertEqual(self.sudoku[0, 2].value, 1)
        self.assertEqual(self.sudoku[0, 3].value, 3)
        self.assertEqual(self.sudoku[0, 4].value, None)
        self.assertEqual(self.sudoku[0, 5].value, 2)
        self.assertEqual(self.sudoku[0, 6].value, None)
        self.assertEqual(self.sudoku[0, 7].value, None)
        self.assertEqual(self.sudoku[0, 8].value, None)

        self.assertEqual(self.sudoku[1, 0].value, None)
        self.assertEqual(self.sudoku[1, 1].value, None)
        self.assertEqual(self.sudoku[1, 2].value, 3)
        self.assertEqual(self.sudoku[1, 3].value, None)
        self.assertEqual(self.sudoku[1, 4].value, None)
        self.assertEqual(self.sudoku[1, 5].value, 7)
        self.assertEqual(self.sudoku[1, 6].value, None)
        self.assertEqual(self.sudoku[1, 7].value, 4)
        self.assertEqual(self.sudoku[1, 8].value, 5)

        self.assertEqual(self.sudoku[2, 0].value, None)
        self.assertEqual(self.sudoku[2, 1].value, None)
        self.assertEqual(self.sudoku[2, 2].value, 7)
        self.assertEqual(self.sudoku[2, 3].value, None)
        self.assertEqual(self.sudoku[2, 4].value, None)
        self.assertEqual(self.sudoku[2, 5].value, None)
        self.assertEqual(self.sudoku[2, 6].value, None)
        self.assertEqual(self.sudoku[2, 7].value, None)
        self.assertEqual(self.sudoku[2, 8].value, 9)

        self.assertEqual(self.sudoku[3, 0].value, None)
        self.assertEqual(self.sudoku[3, 1].value, None)
        self.assertEqual(self.sudoku[3, 2].value, 6)
        self.assertEqual(self.sudoku[3, 3].value, 5)
        self.assertEqual(self.sudoku[3, 4].value, None)
        self.assertEqual(self.sudoku[3, 5].value, None)
        self.assertEqual(self.sudoku[3, 6].value, None)
        self.assertEqual(self.sudoku[3, 7].value, 7)
        self.assertEqual(self.sudoku[3, 8].value, None)

        self.assertEqual(self.sudoku[4, 0].value, 2)
        self.assertEqual(self.sudoku[4, 1].value, None)
        self.assertEqual(self.sudoku[4, 2].value, None)
        self.assertEqual(self.sudoku[4, 3].value, None)
        self.assertEqual(self.sudoku[4, 4].value, None)
        self.assertEqual(self.sudoku[4, 5].value, None)
        self.assertEqual(self.sudoku[4, 6].value, None)
        self.assertEqual(self.sudoku[4, 7].value, None)
        self.assertEqual(self.sudoku[4, 8].value, 1)

        self.assertEqual(self.sudoku[5, 0].value, None)
        self.assertEqual(self.sudoku[5, 1].value, 9)
        self.assertEqual(self.sudoku[5, 2].value, None)
        self.assertEqual(self.sudoku[5, 3].value, None)
        self.assertEqual(self.sudoku[5, 4].value, None)
        self.assertEqual(self.sudoku[5, 5].value, 1)
        self.assertEqual(self.sudoku[5, 6].value, 4)
        self.assertEqual(self.sudoku[5, 7].value, None)
        self.assertEqual(self.sudoku[5, 8].value, None)

        self.assertEqual(self.sudoku[6, 0].value, 5)
        self.assertEqual(self.sudoku[6, 1].value, None)
        self.assertEqual(self.sudoku[6, 2].value, None)
        self.assertEqual(self.sudoku[6, 3].value, None)
        self.assertEqual(self.sudoku[6, 4].value, None)
        self.assertEqual(self.sudoku[6, 5].value, None)
        self.assertEqual(self.sudoku[6, 6].value, 9)
        self.assertEqual(self.sudoku[6, 7].value, None)
        self.assertEqual(self.sudoku[6, 8].value, None)

        self.assertEqual(self.sudoku[7, 0].value, 6)
        self.assertEqual(self.sudoku[7, 1].value, 1)
        self.assertEqual(self.sudoku[7, 2].value, None)
        self.assertEqual(self.sudoku[7, 3].value, 2)
        self.assertEqual(self.sudoku[7, 4].value, None)
        self.assertEqual(self.sudoku[7, 5].value, None)
        self.assertEqual(self.sudoku[7, 6].value, 8)
        self.assertEqual(self.sudoku[7, 7].value, None)
        self.assertEqual(self.sudoku[7, 8].value, None)

        self.assertEqual(self.sudoku[8, 0].value, None)
        self.assertEqual(self.sudoku[8, 1].value, None)
        self.assertEqual(self.sudoku[8, 2].value, None)
        self.assertEqual(self.sudoku[8, 3].value, 9)
        self.assertEqual(self.sudoku[8, 4].value, None)
        self.assertEqual(self.sudoku[8, 5].value, 8)
        self.assertEqual(self.sudoku[8, 6].value, 5)
        self.assertEqual(self.sudoku[8, 7].value, None)
        self.assertEqual(self.sudoku[8, 8].value, None)

        for cell in self.sudoku.values:
            if cell.value is not None:
                self.assertEqual(cell.cell_type, SudokuCellType.BASE)
            else:
                self.assertIsNone(cell.cell_type)

    def test_from_values_invalid(self):
        with self.assertRaisesRegex(ValueError, "Invalid values list given, should have 81 elements, 82 given"):
            Sudoku.from_values([
                0, 0, 1, 3, 0, 2, 0, 0, 0,
                0, 0, 3, 0, 0, 7, 0, 4, 5,
                0, 0, 7, 0, 0, 0, 0, 0, 9,
                0, 0, 6, 5, 0, 0, 0, 7, 0,
                2, 0, 0, 0, 0, 0, 0, 0, 1,
                0, 9, 0, 0, 0, 1, 4, 0, 0,
                5, 0, 0, 0, 0, 0, 9, 0, 0,
                6, 1, 0, 2, 0, 0, 8, 0, 0,
                0, 0, 0, 9, 0, 8, 5, 0, 0, 0,
            ])
        with self.assertRaisesRegex(ValueError, "Invalid values list given, contains the following unexpected elements: \[-1, 10\]"):
            Sudoku.from_values([
                0, 0, 1, 3, 0, 2, 0, 0, -1,
                0, 0, 3, 0, 0, 7, 0, 4, 5,
                0, 0, 7, 0, 0, 0, 0, 0, 9,
                0, 0, 6, 5, 0, 0, 0, 7, 0,
                2, 0, 0, 0, 0, 0, 0, 0, 1,
                0, 9, 0, 0, 0, 10, 4, 0, 0,
                5, 0, 0, 0, 0, 0, 9, 0, 0,
                6, 1, 0, 2, 0, 0, 8, 0, 0,
                0, 0, 0, 9, 0, 8, 5, 0, 0,
            ])

    def test_to_string(self):
        self.assertEqual(
            self.sudoku.__str__(),
            (
                "┌───────────┬───────────┬───────────┐\n"
                "│        1  │  3     2  │           │\n"
                "│        3  │        7  │     4  5  │\n"
                "│        7  │           │        9  │\n"
                "├───────────┼───────────┼───────────┤\n"
                "│        6  │  5        │     7     │\n"
                "│  2        │           │        1  │\n"
                "│     9     │        1  │  4        │\n"
                "├───────────┼───────────┼───────────┤\n"
                "│  5        │           │  9        │\n"
                "│  6  1     │  2        │  8        │\n"
                "│           │  9     8  │  5        │\n"
                "└───────────┴───────────┴───────────┘\n"
            ),
        )

    def test_setitem(self):
        with self.assertRaisesRegex(NotImplementedError, "Direct update disabled, use update_cell method instead"):
            self.sudoku[0, 0] = 1

    def test_block_indices(self):
        self.assertEqual(self.sudoku.block_indices, {0, 1, 2, 3, 4, 5, 6, 7, 8})

    def test_compute_blocks(self):
        blocks = self.sudoku.blocks
        self.assertEqual(len(blocks), 9)
        for block in blocks:
            self.assertEqual(block.width, 3)
            self.assertEqual(block.height, 3)

        self.assertEqual(blocks[0][0, 0].value, None)
        self.assertEqual(blocks[0][0, 1].value, None)
        self.assertEqual(blocks[0][0, 2].value, 1)
        self.assertEqual(blocks[0][1, 0].value, None)
        self.assertEqual(blocks[0][1, 1].value, None)
        self.assertEqual(blocks[0][1, 2].value, 3)
        self.assertEqual(blocks[0][2, 0].value, None)
        self.assertEqual(blocks[0][2, 1].value, None)
        self.assertEqual(blocks[0][2, 2].value, 7)

        self.assertEqual(blocks[1][0, 0].value, 3)
        self.assertEqual(blocks[1][0, 1].value, None)
        self.assertEqual(blocks[1][0, 2].value, 2)
        self.assertEqual(blocks[1][1, 0].value, None)
        self.assertEqual(blocks[1][1, 1].value, None)
        self.assertEqual(blocks[1][1, 2].value, 7)
        self.assertEqual(blocks[1][2, 0].value, None)
        self.assertEqual(blocks[1][2, 1].value, None)
        self.assertEqual(blocks[1][2, 2].value, None)

        self.assertEqual(blocks[2][0, 0].value, None)
        self.assertEqual(blocks[2][0, 1].value, None)
        self.assertEqual(blocks[2][0, 2].value, None)
        self.assertEqual(blocks[2][1, 0].value, None)
        self.assertEqual(blocks[2][1, 1].value, 4)
        self.assertEqual(blocks[2][1, 2].value, 5)
        self.assertEqual(blocks[2][2, 0].value, None)
        self.assertEqual(blocks[2][2, 1].value, None)
        self.assertEqual(blocks[2][2, 2].value, 9)

        self.assertEqual(blocks[3][0, 0].value, None)
        self.assertEqual(blocks[3][0, 1].value, None)
        self.assertEqual(blocks[3][0, 2].value, 6)
        self.assertEqual(blocks[3][1, 0].value, 2)
        self.assertEqual(blocks[3][1, 1].value, None)
        self.assertEqual(blocks[3][1, 2].value, None)
        self.assertEqual(blocks[3][2, 0].value, None)
        self.assertEqual(blocks[3][2, 1].value, 9)
        self.assertEqual(blocks[3][2, 2].value, None)

        self.assertEqual(blocks[4][0, 0].value, 5)
        self.assertEqual(blocks[4][0, 1].value, None)
        self.assertEqual(blocks[4][0, 2].value, None)
        self.assertEqual(blocks[4][1, 0].value, None)
        self.assertEqual(blocks[4][1, 1].value, None)
        self.assertEqual(blocks[4][1, 2].value, None)
        self.assertEqual(blocks[4][2, 0].value, None)
        self.assertEqual(blocks[4][2, 1].value, None)
        self.assertEqual(blocks[4][2, 2].value, 1)

        self.assertEqual(blocks[5][0, 0].value, None)
        self.assertEqual(blocks[5][0, 1].value, 7)
        self.assertEqual(blocks[5][0, 2].value, None)
        self.assertEqual(blocks[5][1, 0].value, None)
        self.assertEqual(blocks[5][1, 1].value, None)
        self.assertEqual(blocks[5][1, 2].value, 1)
        self.assertEqual(blocks[5][2, 0].value, 4)
        self.assertEqual(blocks[5][2, 1].value, None)
        self.assertEqual(blocks[5][2, 2].value, None)

        self.assertEqual(blocks[6][0, 0].value, 5)
        self.assertEqual(blocks[6][0, 1].value, None)
        self.assertEqual(blocks[6][0, 2].value, None)
        self.assertEqual(blocks[6][1, 0].value, 6)
        self.assertEqual(blocks[6][1, 1].value, 1)
        self.assertEqual(blocks[6][1, 2].value, None)
        self.assertEqual(blocks[6][2, 0].value, None)
        self.assertEqual(blocks[6][2, 1].value, None)
        self.assertEqual(blocks[6][2, 2].value, None)

        self.assertEqual(blocks[7][0, 0].value, None)
        self.assertEqual(blocks[7][0, 1].value, None)
        self.assertEqual(blocks[7][0, 2].value, None)
        self.assertEqual(blocks[7][1, 0].value, 2)
        self.assertEqual(blocks[7][1, 1].value, None)
        self.assertEqual(blocks[7][1, 2].value, None)
        self.assertEqual(blocks[7][2, 0].value, 9)
        self.assertEqual(blocks[7][2, 1].value, None)
        self.assertEqual(blocks[7][2, 2].value, 8)

        self.assertEqual(blocks[8][0, 0].value, 9)
        self.assertEqual(blocks[8][0, 1].value, None)
        self.assertEqual(blocks[8][0, 2].value, None)
        self.assertEqual(blocks[8][1, 0].value, 8)
        self.assertEqual(blocks[8][1, 1].value, None)
        self.assertEqual(blocks[8][1, 2].value, None)
        self.assertEqual(blocks[8][2, 0].value, 5)
        self.assertEqual(blocks[8][2, 1].value, None)
        self.assertEqual(blocks[8][2, 2].value, None)

    def test_get_block(self):
        self.assertEqual(self.sudoku.get_block(0), self.sudoku.blocks[0])

    def test_reset_to_base(self):
        cells = self.sudoku.values
        base_cells = [cell for cell in cells if cell.cell_type == SudokuCellType.BASE]
        base_values = [cell.value for cell in base_cells]

        non_base_cells = [cell for cell in cells if cell.cell_type != SudokuCellType.BASE]
        non_base_cells_possibilities = [cell.possibilities.copy() for cell in non_base_cells]
        # We modify the non-base cells
        for index, cell in enumerate(non_base_cells[:len(non_base_cells) // 2]):
            cell.value = 1 + index % 9
            cell.cell_type = SudokuCellType.USER
        for index, cell in enumerate(non_base_cells[len(non_base_cells) // 2:]):
            cell.possibilities = {1 + index % 9}
            cell.cell_type = SudokuCellType.AUTO_LEVEL_1

        self.sudoku.reset_to_base()

        # We check that base cells are unaffected
        self.assertEqual([cell.value for cell in base_cells], base_values)
        for cell in base_cells:
            self.assertEqual(cell.cell_type, SudokuCellType.BASE)

        # We check that non-base cells are reset
        for cell in non_base_cells:
            self.assertIsNone(cell.value)
            self.assertIsNone(cell.cell_type)
        self.assertEqual([cell.possibilities for cell in non_base_cells], non_base_cells_possibilities)

    @mock.patch("alexandregaldeano.sudokuassistant.core.sudoku.Sudoku.apply_assistance")
    @mock.patch("alexandregaldeano.sudokuassistant.core.sudoku.Sudoku._update_cell")
    def test_update_cell(self, mock_update_cell: MagicMock, mock_apply_assistance: MagicMock):
        self.sudoku.update_cell(1, 2, 3, SudokuCellType.USER)

        mock_update_cell.assert_called_once_with(1, 2, 3, SudokuCellType.USER)
        mock_apply_assistance.assert_called_once()

    def test_update_cell_implementation(self):
        cell = self.sudoku[1, 2]
        affected_cells = {
            *self.sudoku.get_row(cell.row_index),
            *self.sudoku.get_column(cell.column_index),
            *self.sudoku.get_block(cell.block_index).values,
        }
        unaffected_cells = list(set(self.sudoku.values) - affected_cells)
        unaffected_cells_values = [cell.value for cell in unaffected_cells]
        unaffected_cells_possibilities = [cell.possibilities.copy() for cell in unaffected_cells]
        self.sudoku._update_cell(cell.row_index, cell.column_index, 3, SudokuCellType.USER)

        self.assertEqual(cell.value, 3)
        self.assertEqual(cell.cell_type, SudokuCellType.USER)
        self.assertEqual(cell.possibilities, set())

        for affected_cell in affected_cells:
            self.assertNotIn(3, affected_cell.possibilities)

        for index, unaffected_cell in enumerate(unaffected_cells):
            self.assertEqual(unaffected_cell.value, unaffected_cells_values[index])
            self.assertEqual(unaffected_cell.possibilities, unaffected_cells_possibilities[index])

    def test_update_cell_implementation_none_possible_value(self):
        cell = self.sudoku[2, 1]
        self.assertNotIn(7, cell.possibilities)
        cells_values = [cell.value for cell in self.sudoku.values]
        cells_possibilities = [cell.possibilities.copy() for cell in self.sudoku.values]
        cells_types = [cell.cell_type for cell in self.sudoku.values]
        self.sudoku._update_cell(cell.row_index, cell.column_index, 7, SudokuCellType.BASE)

        self.assertEqual([cell.value for cell in self.sudoku.values], cells_values)
        self.assertEqual([cell.possibilities for cell in self.sudoku.values], cells_possibilities)
        self.assertEqual([cell.cell_type for cell in self.sudoku.values], cells_types)

    def test_update_cell_implementation_override_type(self):
        cell = self.sudoku[1, 2]
        self.sudoku._update_cell(cell.row_index, cell.column_index, 3, SudokuCellType.USER)
        self.assertEqual(cell.value, 3)
        self.assertEqual(cell.cell_type, SudokuCellType.USER)

    def test_apply_unique_possibilities(self):
        self.sudoku._apply_unique_possibilities()
        cell = self.sudoku[7, 7]
        self.assertEqual(cell.value, 3)
        self.assertEqual(cell.cell_type, SudokuCellType.AUTO_LEVEL_1)

    def test_from_template(self):
        template = (
            "509400000\n"
            "003000690\n"
            "010000005\n"
            "050180000\n"
            "300050007\n"
            "000096050\n"
            "900000070\n"
            "038000500\n"
            "000007103\n"
        )
        sudoku = Sudoku.from_template(template)