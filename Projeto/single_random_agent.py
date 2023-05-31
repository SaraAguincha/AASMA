import argparse
import numpy as np
from gym import Env

from aasma import Agent
from aasma.utils import compare_results
from aasma.wrappers import SingleAgentWrapper
from aasma.traffic_junction import TrafficJunction


def run_single_agent(environment: Env, agent: Agent, n_episodes: int) -> np.ndarray:

    results = np.zeros(n_episodes)

    for episode in range(n_episodes):

        steps = 0
        terminal = False
        observation = environment.reset()
        while not terminal:
            steps += 1
            agent.see(observation)
            action = agent.action()
            next_obs, reward, terminal, info = environment.step(action)
            environment.render()
            observation = next_obs

        environment.close()

        results[episode] = steps

    return results


class RandomAgent(Agent):

    def __init__(self, n_actions: int):
        super(RandomAgent, self).__init__("Random Agent")
        self.n_actions = n_actions

    def action(self) -> int:
        return np.random.randint(self.n_actions)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=10)
    opt = parser.parse_args()

    # 1 - Setup environment
    environment = TrafficJunction(grid_shape=(14, 14), step_cost=-0.01, n_max=1, collision_reward=-10, arrive_prob=0.5)
    environment = SingleAgentWrapper(environment, agent_id=0)

    # 2 - Setup agent
    agent = RandomAgent(environment.action_space.n)

    # 3 - Evaluate agent
    results = {
        agent.name: run_single_agent(environment, agent, opt.episodes)
    }

    # 4 - Compare results
    compare_results(results, title="Random Agent on 'Traffic Junction' Environment", colors=["orange"])