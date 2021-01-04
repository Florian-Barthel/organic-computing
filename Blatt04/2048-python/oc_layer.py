from puzzle import GameGrid
from constants import Direction

from random import randint


def simulate_game(grid_size):
    game_grid = GameGrid(grid_size)

    for x in range(100):
        direction = Direction(randint(1, 4))
        game_grid.move(direction)

        state = game_grid.state()
        if state[2] or x == 99:
            print("Game scored " + str(state[1]) + " points within " + str(
                x) + " iterations!\n")
            break


simulate_game(2)
simulate_game(3)
simulate_game(4)
