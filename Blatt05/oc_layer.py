from puzzle import GameGrid
from constants import Direction

from random import randint
import matplotlib.pyplot as plt


def simulate_game(grid_size):
    game_grid = GameGrid(grid_size)
    scores = []
    num_games = 100

    for x in range(num_games):
        iterations = 0
        while True:
            direction = Direction(randint(1, 4))
            game_grid.move(direction)
            iterations += 1

            state = game_grid.state()
            if state.is_over:
                print("Game #" + str(x + 1) + " scored " + str(state.max_val) +
                      " max value within " + str(iterations) + " iterations!")
                scores.append(state.max_val)
                break

        game_grid.reset()

    game_grid.master.destroy()
    del game_grid

    avg = sum(scores) / num_games
    print("Avg. score: " + str(avg))

    plt.plot(scores)
    plt.ylabel("Max. value")
    plt.xlabel("Game")
    plt.title(str(grid_size) + "x" + str(grid_size) + " game")
    plt.show()


simulate_game(2)
simulate_game(3)
simulate_game(4)
