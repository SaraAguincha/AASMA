import numpy as np
from aasma import Agent

N_ACTIONS = 2
GAS, BREAK = range(N_ACTIONS)

class CommunicatingAgent(Agent):
    """
        A baseline agent for the TrafficJunction environment.
        The greedy agent always tries to advance to reach its destination faster,
        but follows the convention of giving priority to the car if it's on his right.
    """

    def __init__(self, agent_id, n_agents):
        super(CommunicatingAgent, self).__init__(f"CommunicatingAgent Agent")
        self.agent_id = agent_id
        self.n_agents = n_agents
        self.n_actions = N_ACTIONS