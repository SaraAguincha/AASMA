import argparse
import numpy as np
from gym import Env
from typing import Sequence

from aasma import Agent
from aasma.utils import compare_results
from aasma.traffic_junction import TrafficJunction

from agents.RandomAgent import RandomAgent
from agents.GreedyAgent import GreedyAgent
from agents.ConventionAgent import ConventionAgent


def run_multi_agent(environment: Env, agents: Sequence[Agent], n_episodes: int, render: bool) -> np.ndarray:

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
            if render:
                environment.render()
            observations = next_observations
        results[episode] = steps

        environment.close()

    return results


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("--episodes", type=int, default=20)
    parser.add_argument("--agents", type=int, default=10)
    parser.add_argument("--render", action='store_true')
    parser.add_argument("--random", action='store_false')
    parser.add_argument("--greedy", action='store_false')
    parser.add_argument("--conventional", action='store_false')

    opt = parser.parse_args()

    # 1 - Setup the environment
    environment = TrafficJunction(grid_shape=(14, 14), step_cost=-0.01, n_max=opt.agents, collision_reward=-10, arrive_prob=0.5)

    # 2 - Setup the teams
    teams = {}
    if opt.random:
        teams["Random Team"] = [RandomAgent(environment.action_space[i].n) for i in range(environment.n_agents)]
    if opt.greedy: teams["Greedy Team"] = []
    if opt.conventional: teams["Convention Team"] = []

    for i in range(opt.agents):
        if opt.greedy: teams["Greedy Team"].append(GreedyAgent(agent_id=i, n_agents=opt.agents))
        if opt.conventional: teams["Convention Team"].append(ConventionAgent(agent_id=i, n_agents=opt.agents))

    # 3 - Evaluate teams
    results = {}
    for team, agents in teams.items():
        result = run_multi_agent(environment, agents, opt.episodes, opt.render)
        results[team] = result

    # 4 - Compare results
    compare_results(
        results,
        title="Results on 'Traffic Junction' Environment",
        colors=["orange", "blue", "green"]
    )

