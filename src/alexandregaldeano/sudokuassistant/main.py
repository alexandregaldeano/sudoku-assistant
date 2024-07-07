import logging
import sys

from alexandregaldeano.sudokuassistant.application.application import Application
from alexandregaldeano.sudokuassistant.core.sudoku_assistance_level import SudokuAssistanceLevel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)

# Click event handler
def on_click(event):
    global application

    if not event.inaxes:
        return
    x, y = int(event.xdata), int(event.ydata)
    application.selected_cell = (y, x)
    application.draw_grid()


# Key press event handler
def on_key(event):
    global application
    row_index, column_index = application.selected_cell

    if event.key == "up":
        application.selected_cell = (max(0, row_index - 1), column_index)
    elif event.key == "down":
        application.selected_cell = (min(8, row_index + 1), column_index)
    elif event.key == "left":
        application.selected_cell = (row_index, max(0, column_index - 1))
    elif event.key == "right":
        application.selected_cell = (row_index, min(8, column_index + 1))
    elif event.key == "tab":
        application.user_mode = not application.user_mode
    elif event.key == "p":
        application.possibility_edition_mode = not application.possibility_edition_mode
    elif event.key.isdigit():
        application.update_cell(row_index, column_index, int(event.key))
    elif event.key == "a":
        application.assistance_level = SudokuAssistanceLevel((application.assistance_level + 1) % 4)
    elif event.key == "r":
        application.reset()
    application.draw_grid()


if __name__ == "__main__":
    template_filepath = sys.argv[1]
    shuffle = bool(int(sys.argv[2]))
    application = Application.from_template_file(template_filepath, shuffle)
    # Connect the event handlers
    application.figure.canvas.mpl_connect('button_press_event', on_click)
    application.figure.canvas.mpl_connect("key_press_event", on_key)
    application.run()
