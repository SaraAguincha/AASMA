import argparse
import numpy as np
from gym import Env
from typing import Sequence
from statistics import mean

from aasma import Agent
from aasma.utils import compare_all_results, compare_results_and_collisions
from aasma.traffic_junction import TrafficJunction
from agents.CommunicationHandler import CommunicationHandler

from agents.RandomAgent import RandomAgent
from agents.GreedyAgent import GreedyAgent
from agents.ConventionAgent import ConventionAgent
from agents.CommunicatingAgent import CommunicatingAgent
from agents.WaitingAgent import WaitingAgent


def run_multi_agent(environment: Env, agents: Sequence[Agent], n_episodes: int, render: bool, random: bool) -> np.ndarray:

    results = np.zeros(n_episodes)
    collisions = np.zeros(n_episodes)
    waitingSteps = np.zeros(n_episodes)

    communication_handler.update_agents(list(agents))

    for episode in range(n_episodes):
        steps = 0
        terminals = [False for _ in range(len(agents))]
        observations = environment.reset()
        
        Timers = []
        while not all(terminals):
            actions = []
            steps += 1
            for observations, agent in zip(observations, agents):
                agent.see(observations)
                agent.update_moving_direction()
            communication_handler.update_agents(list(agents))
            
            if not random:
                for agent in agents:
                    action, TimeStep = agent.action()
                    if TimeStep != None and TimeStep != 0:
                        Timers += [TimeStep]
                    actions += [action]
            else:
                for agent in agents:
                    action, TimeStep = agent.action()
                    actions += [action]
            next_observations, rewards, terminals, info = environment.step(actions)
            collisions[episode] += info['step_collisions']
            
            if render:
                environment.render()
            observations = next_observations
        results[episode] = steps
        if not random:
            waitingSteps[episode] += mean(Timers)

        for agent in agents:
            agent.reset_visited()
            agent.reset_waiting_time()
            agent.reset_has_entered_junction()

        environment.close()

    return results, collisions, waitingSteps


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("--episodes", type=int, default=20)
    parser.add_argument("--agents", type=int, default=10)
    parser.add_argument("--maxsteps", type=int, default=100)
    parser.add_argument("--render", action='store_true')
    parser.add_argument("--random", "-r", action='store_true')
    parser.add_argument("--greedy", "-g", action='store_true')
    parser.add_argument("--conventional", "-con", action='store_true')
    parser.add_argument("--communicating", "-com", action='store_true')
    parser.add_argument("--waiting", "-w", action='store_true')
    parser.add_argument("--all", "-a", action='store_true')

    opt = parser.parse_args()

    if opt.all:
        opt.random = True
        opt.greedy = True
        opt.conventional = True
        opt.communicating = True
        opt.waiting = True

    # 1 - Setup the environment
    environment = TrafficJunction(grid_shape=(14, 14), step_cost=-0.01, n_max=opt.agents, collision_reward=-10, arrive_prob=0.5, max_steps=opt.maxsteps)
    communication_handler = CommunicationHandler()

    # 2 - Set up the teams
    teams = {}
    if opt.random:
        teams["Random Team"] = [RandomAgent(environment.action_space[i].n) for i in range(environment.n_agents)]
    if opt.greedy: teams["Greedy Team"] = []
    if opt.conventional: teams["Convention Team"] = []
    if opt.communicating: teams["Communicating Team"] = []
    if opt.waiting: teams["Waiting Team"] = []

    for i in range(1, opt.agents + 1):
        if opt.greedy: teams["Greedy Team"].append(GreedyAgent(agent_id=i, n_agents=opt.agents))
        if opt.conventional: teams["Convention Team"].append(ConventionAgent(agent_id=i, n_agents=opt.agents))
        if opt.communicating: teams["Communicating Team"].append(CommunicatingAgent(agent_id=i, n_agents=opt.agents, communication_handler=communication_handler))
        if opt.waiting: teams["Waiting Team"].append(WaitingAgent(agent_id=i, n_agents=opt.agents, communication_handler=communication_handler))

    # 3 - Evaluate teams
    results = {}
    collisions = {}
    waitingTime = {}
    for team, agents in teams.items():
        result, collision, wait = run_multi_agent(environment, agents, opt.episodes, opt.render, opt.random)
        results[team] = result
        collisions[team] = collision
        waitingTime[team] = wait

    # 4 - Compare results
    if opt.random:
        compare_results_and_collisions(
            results,
            collisions,
            title="Results on 'Traffic Junction' Environment",
            colors=["orange", "blue", "green", "red"]
        )
    else:
        compare_all_results(
            results, 
            collisions, 
            waitingTime,
            title="Results on 'Traffic Junction' Environment",
            colors=["orange", "blue", "green", "red"]
        )
