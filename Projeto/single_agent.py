import argparse
import numpy as np
from gym import Env

from aasma import Agent
from aasma.utils import compare_results
from aasma.wrappers import SingleAgentWrapper
from aasma.traffic_junction import TrafficJunction

from agents.RandomAgent import RandomAgent
from agents.GreedyAgent import GreedyAgent


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


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=10)
    opt = parser.parse_args()

    # 1 - Setup environment
    environment = TrafficJunction(grid_shape=(14, 14), step_cost=-0.01, n_max=1, collision_reward=-10, arrive_prob=0.5)
    environment = SingleAgentWrapper(environment, agent_id=0)

    # 2 - Setup agent
    agents = [
        RandomAgent(environment.action_space.n),
        GreedyAgent(agent_id=0, n_agents=1)
    ]

    # 3 - Evaluate agent
    results = {}
    for agent in agents:
        result = run_single_agent(environment, agent, opt.episodes)
        results[agent.name] = result

    # 4 - Compare results
    compare_results(results, title="Single Agents on 'Traffic Junction' Environment", colors=["orange", "Blue"])