import argparse
import numpy as np
from gym import Env
from typing import Sequence

from aasma import Agent
from aasma.utils import compare_results
from aasma.traffic_junction import TrafficJunction

from single_random_agent import RandomAgent


def run_multi_agent(environment: Env, agents: Sequence[Agent], n_episodes: int) -> np.ndarray:

    results = np.zeros(n_episodes)

    for episode in range(n_episodes):

        steps = 0
        terminals = [False for _ in range(len(agents))]
        observations = environment.reset()

        while not all(terminals):
            steps += 1
            for observations, agent in zip(observations, agents):
                agent.see(observations)
            actions = [agent.action() for agent in agents]
            next_observations, rewards, terminals, info = environment.step(actions)
            environment.render()
            observations = next_observations
        results[episode] = steps

        environment.close()

    return results


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("--episodes", type=int, default=100)
    opt = parser.parse_args()

    # 1 - Setup the environment
    environment = TrafficJunction(grid_shape=(14, 14), step_cost=-0.01, n_max=8, collision_reward=-10, arrive_prob=0.5)

    # 2 - Setup the teams
    teams = {}
    teams["Random Team"] = [RandomAgent(environment.action_space[i].n) for i in range(environment.n_agents)]

    # 3 - Evaluate teams
    results = {}
    for team, agents in teams.items():
        result = run_multi_agent(environment, agents, opt.episodes)
        results[team] = result

    # 4 - Compare results
    compare_results(
        results,
        title="Random Team on 'Traffic Junction' Environment",
        colors=["orange"]
    )

