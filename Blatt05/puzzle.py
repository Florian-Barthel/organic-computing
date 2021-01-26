from tkinter import Frame, Label, CENTER
import random
import sys
from collections import namedtuple

import logic
import constants as c

# from constants import Direction

visual = False


def gen():
    return random.randint(0, c.GRID_LEN - 1)


class GameGrid(Frame):
    def __init__(self, grid_len=0):
        Frame.__init__(self)

        self.grid_len = grid_len
        if grid_len == 0 and len(sys.argv) > 1:  # use first command arg as
            # int for grid length
            c.GRID_LEN = int(sys.argv[1])
        elif grid_len > 0:
            c.GRID_LEN = int(grid_len)

        # print("Grid size: " + str(c.GRID_LEN))

        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)

        self.commands = {c.KEY_UP: logic.up, c.KEY_DOWN: logic.down,
                         c.KEY_LEFT: logic.left, c.KEY_RIGHT: logic.right,
                         c.KEY_UP_ALT: logic.up, c.KEY_DOWN_ALT: logic.down,
                         c.KEY_LEFT_ALT: logic.left,
                         c.KEY_RIGHT_ALT: logic.right,
                         c.KEY_H: logic.left, c.KEY_L: logic.right,
                         c.KEY_K: logic.up, c.KEY_J: logic.down}

        self.auto_commands = {'up': logic.up,
                              'down': logic.down,
                              'left': logic.left,
                              'right': logic.right
                              }

        self.grid_cells = []
        if visual:
            self.init_grid()
        self.matrix = logic.new_game(c.GRID_LEN)
        self.history_matrixs = []
        self.update_grid_cells()
        self.score = 0

        # self.mainloop()

    # CONTROL
    def reset(self):
        if visual:
            self.init_grid()
        self.matrix = logic.new_game(self.grid_len)
        self.score = 0

    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME,
                           width=c.SIZE, height=c.SIZE)
        background.grid()

        for i in range(c.GRID_LEN):
            grid_row = []
            for j in range(c.GRID_LEN):
                cell = Frame(background, bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                             width=c.SIZE / c.GRID_LEN,
                             height=c.SIZE / c.GRID_LEN)
                cell.grid(row=i, column=j, padx=c.GRID_PADDING,
                          pady=c.GRID_PADDING)
                t = Label(master=cell, text="",
                          bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                          justify=CENTER, font=c.FONT, width=5, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        if not visual:
            return
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(
                        text="",
                        bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number),
                                                    bg=c.BACKGROUND_COLOR_DICT[
                                                        new_number],
                                                    fg=c.CELL_COLOR_DICT[
                                                        new_number])
        # self.update_idletasks()

    def key_down(self, event):
        pass
        # not needed anymore for non-GUI usage

    def generate_next(self):
        index = (gen(), gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (gen(), gen())
        self.matrix[index[0]][index[1]] = 2

    # CONTROL
    def move(self, direction):
        self.matrix, done, increase_score = self.auto_commands[direction](
            self.matrix)
        self.score += increase_score
        if done:
            self.matrix = logic.add_two(self.matrix)
            self.update_grid_cells()

    # OBSERVE
    def state(self):
        game_state = self.matrix

        max_val = 0  # get highest number for score
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if self.matrix[i][j] > max_val:
                    max_val = self.matrix[i][j]

        is_over = logic.game_state(self.matrix) != 'not over'

        return_tuple = namedtuple("return_tuple", ["game_state", "max_val",
                                                   "score", "is_over"])

        return return_tuple(game_state, max_val, self.score, is_over)
