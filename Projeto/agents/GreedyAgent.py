from aasma import Agent

N_ACTIONS = 2
GAS, BREAK = range(N_ACTIONS)


class GreedyAgent(Agent):

    """
    A baseline agent for the TrafficJunction environment.
    The greedy agent always advances if the next cell is vacant
    in order to reach its destination faster.
    """

    def __init__(self, agent_id, n_agents):
        super(GreedyAgent, self).__init__(f"Greedy Agent")
        self.agent_id = agent_id
        self.n_agents = n_agents
        self.n_actions = N_ACTIONS
        

    def action(self) -> int:        
        return GAS
        