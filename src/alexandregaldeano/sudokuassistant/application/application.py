import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from alexandregaldeano.sudokuassistant.core.sudoku import Sudoku
from alexandregaldeano.sudokuassistant.core.sudoku_assistance_level import SudokuAssistanceLevel
from alexandregaldeano.sudokuassistant.core.sudoku_cell import SudokuCell
from alexandregaldeano.sudokuassistant.core.sudoku_cell_type import SudokuCellType


class Application:
    def __init__(self, sudoku: Sudoku | None = None):
        self.sudoku = sudoku or Sudoku()
        self.selected_cell = (0, 0)
        self.user_mode = True
        self.possibility_edition_mode = False
        self.assistance_level = SudokuAssistanceLevel.NONE
        [self.figure, self.axes] = plt.subplots()
        self.style_by_cell_type = {
            SudokuCellType.ERROR: {
                "color": "red",
                "weight": "bold",
            },
            SudokuCellType.BASE: {
                "color": "black",
                "weight": "bold",
            },
            SudokuCellType.USER: {
                "color": "black",
            },
            SudokuCellType.AUTO_LEVEL_1: {
                "color": "lightblue",
            },
            SudokuCellType.AUTO_LEVEL_2: {
                "color": "blue",
            }
        }

    def update_cell(self, row_index: int, column_index: int, value: int):
        if value not in {1, 2, 3, 4, 5, 6, 7, 8, 9}:
            return
        if not self.possibility_edition_mode:
            self.sudoku.update_cell(row_index, column_index, value,
                                    SudokuCellType.USER if self.user_mode else SudokuCellType.BASE)
            return
        self.sudoku.remove_possibility(row_index, column_index, value)

    def reset(self):
        self.sudoku.reset_to_base()

    def run(self):
        self.draw_grid()
        plt.show()

    @property
    def assistance_level(self):
        return self.sudoku.assistance_level

    @assistance_level.setter
    def assistance_level(self, value: SudokuAssistanceLevel):
        self.sudoku.assistance_level = value
        self.sudoku.apply_assistance()

    def draw_grid(self):
        self.axes.clear()

        self._draw_grid_lines()

        for cell in self.sudoku.values:
            self._draw_cell(cell)

        self._highlight_selected_cell()

        # Update the titles
        plt.suptitle(f"{'Solved' if self.sudoku.solved else 'Not solved'} — Steps {self.sudoku.steps}")

        # Update the axes
        self.axes.set_xlim(0, 9)
        self.axes.set_ylim(0, 9)
        self.axes.invert_yaxis()
        self.axes.xaxis.tick_top()
        self.axes.set_xticks([])
        self.axes.set_yticks([])
        xlabel = "User edition" if self.user_mode else "Base edition"
        xlabel += "\n"
        xlabel += "Possibilities edition" if self.possibility_edition_mode else "Value edition"
        xlabel += "\n"
        xlabel += f"Assistance level {self.assistance_level.name.lower()}"
        self.axes.set_xlabel(xlabel)
        self.axes.yaxis.set_label_position("right")
        ylabel = "\n".join([f"{digit}: {count}" for digit, count in self.sudoku.remaining_digits.items()])
        self.axes.set_ylabel(ylabel, rotation=0, labelpad=20)
        plt.draw()

    def _draw_grid_lines(self):
        for line_index in range(10):
            line_width = 2 if line_index % 3 == 0 else 0.5
            self.axes.plot([line_index, line_index], [0, 9], "k", linewidth=line_width)
            self.axes.plot([0, 9], [line_index, line_index], "k", linewidth=line_width)

    def _draw_cell(self, cell: SudokuCell):
        text = None
        if cell.cell_type == SudokuCellType.ERROR:
            text = "E"
        elif cell.value:
            text = str(cell.value)
        if text:
            style = self.style_by_cell_type[cell.cell_type]
            self.axes.text(
                cell.column_index + 0.5,
                cell.row_index + 0.5,
                text,
                va="center",
                ha="center",
                fontsize=16,
                **style
            )
            return
        if self.assistance_level < SudokuAssistanceLevel.LOW:
            return
        for possibility_index, possibility in enumerate(sorted(cell.possibilities)):
            self.axes.text(
                cell.column_index + 0.3 * (possibility_index % 3) + 0.1,
                cell.row_index + 0.3 * (possibility_index // 3) + 0.2,
                str(possibility),
                va="center",
                ha="center",
                fontsize=10,
                color="gray",
            )

    def _highlight_selected_cell(self):
        self.axes.add_patch(
            Rectangle(
                (self.selected_cell[1], self.selected_cell[0]),
                1, 1, edgecolor="red", facecolor="none"
            )
        )

    @classmethod
    def from_template_file(cls, filepath: str, shuffle: bool) -> "Application":
        with open(filepath) as file:
            template = file.read()
        return Application(Sudoku.from_template(template, shuffle))
