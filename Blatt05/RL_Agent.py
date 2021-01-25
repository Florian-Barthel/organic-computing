from puzzle import GameGrid
from constants import Direction

from random import randint, random
import matplotlib.pyplot as plt
import numpy as np


class RLAgent:

    def __init__(self, grid_len=0):
        self.game_grid = GameGrid(grid_len)

        self.learning_rate = 0.9  # alpha
        self.discount_rate = 0.1  # gamma
        self.greediness = 0.9  # epsilon
        self.q = []
        self.states = []
        self.end_score = 0
        self.uninit_q_decisions = 0
        self.init_q_decisions = 0

    def update_q(self, s, action, max_q_next, reward):
        self.q[s][action] += self.learning_rate * (reward +
                                                   self.discount_rate *
                                                   max_q_next - self.q[s][
                                                       action])

    def get_sym_equal(self, state):
        flipped_lr = np.fliplr(state).tolist()
        flipped_ud = np.flipud(state).tolist()
        for i_s in range(len(self.states)):
            s = self.states[i_s]
            if s == flipped_lr or s == flipped_ud:
                return i_s, s == flipped_lr
        return None, None

    def get_rot_equal(self, state):
        rot90_x1 = np.rot90(state, k=1).tolist()
        rot90_x2 = np.rot90(state, k=2).tolist()
        rot90_x3 = np.rot90(state, k=3).tolist()
        for i_s in range(len(self.states)):
            s = self.states[i_s]
            if s == rot90_x1:
                return i_s, 1
            elif s == rot90_x2:
                return i_s, 2
            elif s == rot90_x3:
                return i_s, 3
        return None, None

    def is_state_known(self, state):
        if state in self.states:
            return True
        elif self.get_sym_equal(state) != (None, None):
            return True
        elif self.get_rot_equal(state) != (None, None):
            return True
        else:
            return False

    def get_q_rot_sym(self, state):
        if state in self.states:
            return self.q[self.states.index(state)]

        s_sym, lr = self.get_sym_equal(state)
        if s_sym is not None:
            q_s = self.q[s_sym]
            if lr:  # left-right symmetry
                return [q_s[1], q_s[0], q_s[3], q_s[2]]
            else:  # up-down symmetry
                return [q_s[2], q_s[3], q_s[0], q_s[1]]

        s_rot, k = self.get_rot_equal(state)
        if s_rot is not None:
            q_s = self.q[s_rot]
            if k == 1:  # rotated 90° once
                return [q_s[1], q_s[3], q_s[0], q_s[2]]
            elif k == 2:  # rotated 90° twice
                return [q_s[3], q_s[2], q_s[1], q_s[0]]
            elif k == 3:  # rotated 90° 3 times
                return [q_s[2], q_s[0], q_s[3], q_s[1]]

        return None

    def run_episode(self):
        iterations = 0

        while True:
            state = self.game_grid.state()

            current_state = [s for s in self.states if state.game_state == s]
            if not current_state:
                self.q.append([0, 0, 0, 0])
                self.states.append(state.game_state)
                current_state = state.game_state
                self.uninit_q_decisions += 1
            else:
                current_state = current_state[0]
                if self.q[self.states.index(current_state)] == [0, 0, 0, 0]:
                    self.uninit_q_decisions += 1
                else:
                    self.init_q_decisions += 1

            state_i = self.states.index(current_state)
            next_action = self.q[state_i].index(max(self.q[state_i]))

            if random() < self.greediness:
                next_action = randint(0, 3)

            next_action = int(next_action)

            if self.greediness > 0.010:
                self.greediness -= (self.greediness - 0.01) * 0.00005

            self.game_grid.move(Direction(next_action + 1))
            state_after = self.game_grid.state()
            reward = state_after.score - state.score

            exists = self.is_state_known(state_after.game_state)
            new_state = state_after.game_state
            if not exists:
                self.q.append([0, 0, 0, 0])
                self.states.append(state_after.game_state)
                new_state = state_after.game_state

            iterations += 1

            if state_after.is_over:
                self.end_score = state_after.score
                self.get_q_rot_sym(new_state)[next_action] = 0
                break
            else:
                max_q_next = max(self.get_q_rot_sym(new_state))
                self.update_q(self.states.index(current_state), next_action,
                              max_q_next, reward)

            if self.learning_rate > 0.100:
                self.learning_rate -= (self.learning_rate - 0.1) * 0.0001

        self.game_grid.master.destroy()
        del self.game_grid


def run_agent(gs, learn, d, g, q, s, index):
    agent = RLAgent(gs)
    agent.learning_rate = learn
    agent.discount_rate = d
    agent.greediness = g
    agent.q = q
    agent.states = s
    agent.run_episode()

    print("Episode #" + str(index + 1) + ": e=" + str(agent.greediness) +
          ", a=" + str(agent.learning_rate) + ", q-size=" + str(len(agent.q))
          + ", score=" + str(agent.end_score))
    return agent


grid_size = 2
num_episodes = 10000
score_total = 0
results = []
init_q_results = []
uninit_q_results = []

a = run_agent(grid_size, 0.8, 0.5, 0.8, [], [], 0)
results.append(a.end_score)
q_result_total = a.init_q_decisions + a.uninit_q_decisions
init_q_results.append(a.init_q_decisions / q_result_total)
uninit_q_results.append((a.uninit_q_decisions / q_result_total))

for i in range(num_episodes - 1):
    prev_score = a.end_score
    a = run_agent(grid_size, a.learning_rate, a.discount_rate, a.greediness,
                  a.q, a.states, i + 1)
    results.append(a.end_score)
    q_result_total = a.init_q_decisions + a.uninit_q_decisions
    init_q_results.append(a.init_q_decisions / q_result_total)
    uninit_q_results.append((a.uninit_q_decisions / q_result_total))
    i2 = i + 2
    if i >= 100:
        results[i2 - 1] = (sum(results[-99:]) / 99)
        init_q_results[i2 - 1] = (sum(init_q_results[-99:]) / 99)
        uninit_q_results[i2 - 1] = (sum(uninit_q_results[-99:]) / 99)
    else:
        results[i2 - 1] = (sum(results[-i2:]) / i2)
        init_q_results[i2 - 1] = (sum(init_q_results[-i2:]) / i2)
        uninit_q_results[i2 - 1] = (sum(uninit_q_results[-i2:]) / i2)

score_total = sum(results)
avg_score = score_total / num_episodes
print("Average of " + str(num_episodes) + " episodes: " + str(avg_score))

# Just here for task 1.6
# for i in range(len(a.q)):
#     if sum(a.states[i][0]) > 4 or sum(a.states[i][1]) > 4 or\
#             4 in a.states[i][0] or 4 in a.states[i][1]:
#         continue
#     print(str(a.states[i]) + " -> " + str(a.q[i][0]) + " " + str(a.q[i][1]) +
#           " " + str(a.q[i][2]) + " " + str(a.q[i][3]))

plt.plot(results)
plt.ylabel("Score")
plt.xlabel("Episode")
plt.title("RL Agent")
plt.show()

plt.plot(init_q_results, label="Initialized")
plt.plot(uninit_q_results, label="Uninitialized")
plt.ylabel("(Un)Initialized fraction of decisions")
plt.xlabel("Episode")
plt.title("RL Agent")
plt.legend(loc="best")
plt.show()
