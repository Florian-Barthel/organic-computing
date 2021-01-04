from tkinter import Frame, Label, CENTER
import random
import sys

import logic
import constants as c
from constants import Direction


def gen():
    return random.randint(0, c.GRID_LEN - 1)


class GameGrid(Frame):
    def __init__(self, grid_len=0):
        Frame.__init__(self)

        if grid_len == 0 and len(sys.argv) > 1:  # use first command arg as
            # int for grid length
            c.GRID_LEN = int(sys.argv[1])
        elif grid_len > 0:
            c.GRID_LEN = int(grid_len)

        print("Grid size: " + str(c.GRID_LEN))

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

        self.grid_cells = []
        self.init_grid()
        self.matrix = logic.new_game(c.GRID_LEN)
        self.history_matrixs = []
        self.update_grid_cells()

        # self.mainloop()

    # CONTROL
    def reset(self):
        print("Resetting game")
        self.grid_forget()
        self.__init__()

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
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="",
                                                    bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number),
                                                    bg=c.BACKGROUND_COLOR_DICT[
                                                        new_number],
                                                    fg=c.CELL_COLOR_DICT[
                                                        new_number])
        self.update_idletasks()

    def key_down(self, event):
        key = repr(event.char)
        self.process_input(key)

    def process_input(self, key):
        if key == c.KEY_BACK and len(self.history_matrixs) > 1:
            self.matrix = self.history_matrixs.pop()
            self.update_grid_cells()
            print('back on step total step:', len(self.history_matrixs))
        elif key in self.commands:
            self.matrix, done = self.commands[key](self.matrix)
            if done:
                self.matrix = logic.add_two(self.matrix)
                # record last move
                self.history_matrixs.append(self.matrix)
                self.update_grid_cells()
                if logic.game_state(self.matrix) == 'win':  # change cell
                    # indices to work with 2x2 grids
                    self.grid_cells[0][0].configure(text="You",
                                                    bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[0][1].configure(text="Win!",
                                                    bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                if logic.game_state(self.matrix) == 'lose':
                    self.grid_cells[0][0].configure(text="You",
                                                    bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[0][1].configure(text="Lose!",
                                                    bg=c.BACKGROUND_COLOR_CELL_EMPTY)
        elif key == c.KEY_ESC:  # ESC for testing purposes
            self.reset()

    def generate_next(self):
        index = (gen(), gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (gen(), gen())
        self.matrix[index[0]][index[1]] = 2

    # CONTROL
    def move(self, direction: Direction):
        if direction == Direction.LEFT:
            self.process_input(c.KEY_LEFT)
        elif direction == Direction.RIGHT:
            self.process_input(c.KEY_RIGHT)
        elif direction == Direction.UP:
            self.process_input(c.KEY_UP)
        elif direction == Direction.DOWN:
            self.process_input(c.KEY_DOWN)

    # OBSERVE
    def state(self):
        gamestate = self.matrix

        max_val = 0  # get highest number for score
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if self.matrix[i][j] > max_val:
                    max_val = self.matrix[i][j]

        is_over = logic.game_state(self.matrix) != 'not over'

        return gamestate, max_val, is_over
