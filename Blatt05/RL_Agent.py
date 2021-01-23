from puzzle import GameGrid
from constants import Direction

from random import randint, random
import matplotlib.pyplot as plt


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

    def update_q(self, s, a, max_q_next, reward):
        self.q[s][a] += self.learning_rate * (reward + self.discount_rate *
                                              max_q_next - self.q[s][a])

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
                self.init_q_decisions += 1

            state_i = self.states.index(current_state)
            next_action = self.q[state_i].index(max(self.q[state_i]))

            if random() < self.greediness:
                next_action = randint(0, 3)

            next_action = int(next_action)

            self.greediness -= (self.greediness - 0.1) * 0.0001

            self.game_grid.move(Direction(next_action + 1))
            state_after = self.game_grid.state()
            reward = state_after.score - state.score

            new_state = [s for s in self.states if state_after.game_state == s]
            if not new_state:
                self.q.append([0, 0, 0, 0])
                self.states.append(state_after.game_state)
                new_state = state_after.game_state
            else:
                new_state = new_state[0]

            iterations += 1

            if state_after.is_over:
                self.end_score = state_after.score
                self.q[self.states.index(new_state)][next_action] = 0
                break
            else:
                max_q_next = max(self.q[self.states.index(new_state)])
                self.update_q(self.states.index(current_state), next_action,
                              max_q_next, reward)

            self.learning_rate -= (self.learning_rate - 0.1) * 0.0001

        self.game_grid.master.destroy()
        del self.game_grid


def run_agent(gs, l, d, g, q, s, i):
    agent = RLAgent(gs)
    agent.learning_rate = l
    agent.discount_rate = d
    agent.greediness = g
    agent.q = q
    agent.states = s
    agent.run_episode()

    print("Episode #" + str(i+1) + ": e=" + str(agent.greediness) + ", "
           "a=" + str(agent.learning_rate) + ", q-size=" + str(len(agent.q))
           + ", score=" + str(agent.end_score))
    return agent


num_episodes = 10000
score_total = 0
results = []
init_q_results = []
uninit_q_results = []

a = run_agent(2, 0.8, 0.5, 0.8, [], [], 0)
results.append(a.end_score)
q_result_total = a.init_q_decisions + a.uninit_q_decisions
init_q_results.append(a.init_q_decisions / q_result_total)
uninit_q_results.append((a.uninit_q_decisions / q_result_total))

for i in range(num_episodes - 1):
    prev_score = a.end_score
    a = run_agent(2, a.learning_rate, a.discount_rate, a.greediness,
                  a.q, a.states, i + 1)
    results.append(a.end_score)
    q_result_total = a.init_q_decisions + a.uninit_q_decisions
    init_q_results.append(a.init_q_decisions / q_result_total)
    uninit_q_results.append((a.uninit_q_decisions / q_result_total))
    i2 = i + 2
    if i >= 100:
        results[i2 - 1] = (sum(results[-100:]) / 100)
        init_q_results[i2 - 1] = (sum(init_q_results[-100:]) / 100)
        uninit_q_results[i2 - 1] = (sum(uninit_q_results[-100:]) / 100)
    else:
        results[i2 - 1] = (sum(results[-i2:]) / i2)
        init_q_results[i2 - 1] = (sum(init_q_results[-i2:]) / i2)
        uninit_q_results[i2 - 1] = (sum(uninit_q_results[-i2:]) / i2)

score_total = sum(results)
avg_score = score_total / num_episodes
print("Average of " + str(num_episodes) + " episodes: " + str(avg_score))
print(a.q)
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
