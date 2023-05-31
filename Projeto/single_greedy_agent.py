import math
import random
import argparse
import numpy as np
#from scipy.spatial.distance import cityblock

from aasma import Agent
from aasma.utils import compare_results
from aasma.wrappers import SingleAgentWrapper
from aasma.traffic_junction import TrafficJunction

from single_random_agent import run_single_agent, RandomAgent

N_ACTIONS = 2
GAS, BREAK = range(N_ACTIONS)


class GreedyAgent(Agent):

    """
    A baseline agent for the TrafficJunction environment.
    The greedy agent always tries to avance to reach its destination faster.
    """

    def __init__(self, agent_id, n_agents):
        super(GreedyAgent, self).__init__(f"Greedy Agent")
        self.agent_id = agent_id
        self.n_agents = n_agents
        self.n_actions = N_ACTIONS
        

    def action(self) -> int:        
        agent_position = self.observation[4 * (self.n_agents + 5) + 1:4 * (self.n_agents + 5) + 3]  # middle cell from the 3x3 grid
        
        # not sure if necessary but it works, and its simpler to 'see' the position
        # 13 is: grid_size - 1
        agent_position = [round(i * 13) for i in agent_position]

        near_agents = self.get_near_agents(self.observation, self.n_agents)      
        # yet again not, necessary
        i = 0
        for agent in near_agents:
            near_agents[i] = [round(i * 13) for i in agent]
            i += 1


        # TODO - still does nothing, but already has its position and the neighbors


        action = 0
        return action
        

    # ################# #
    # Auxiliary Methods #
    # ################# #
    
    def get_near_agents(self,observation, n_agents):
        """
        Given the observation (currently (3x3)), it returns
        a list of the positions of the near agents.
        """
        near_agents = []
        # above the agent
        
        i = 0
        while i < len(self.observation):
            print(self.observation[i :i + n_agents + 5])
            if 1 in self.observation[i :i + n_agents + 5] and not(4 * (n_agents + 5) <= i <= 5 * (n_agents + 5)):
                
                near_agents.append(list(self.observation[i + n_agents : i + n_agents + 2]))
                i += n_agents + 5
            i += n_agents + 5
        return near_agents
        
        

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("--episodes", type=int, default=30)
    opt = parser.parse_args()

    # 1 - Setup environment
    environment = TrafficJunction(grid_shape=(14, 14), step_cost=-0.01, n_max=1, collision_reward=-10, arrive_prob=0.5)
    environment = SingleAgentWrapper(environment, agent_id=0)

    # 2 - Setup agents
    agents = [
        #RandomAgent(environment.action_space.n),
        GreedyAgent(agent_id=0, n_agents=1)
    ]

    # 3 - Evaluate agents
    results = {}
    for agent in agents:
        result = run_single_agent(environment, agent, opt.episodes)
        results[agent.name] = result

    # 4 - Compare results
    compare_results(results, title="Agents on 'Traffic Junction' Environment", colors=["orange", "green"])

