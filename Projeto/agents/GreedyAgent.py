from aasma import Agent
import numpy as np

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
        self.waiting_time = 0
        self.has_entered_junction = False
        

    def action(self) -> int:  
        max_time = None
        # just to have the metric of waiting time
        agent_position = self.observation[2][2][self.n_agents:self.n_agents + 2]
        
        if self.__is_in_junction(agent_position):
            self.has_entered_junction = True
        
        if not self.has_entered_junction:
            if list(agent_position) and list(agent_position) != [0, 0]:
                self.waiting_time += 1
        else:
            max_time = self.waiting_time
            self.waiting_time = 0
      
        return GAS, max_time
    
    # ################# #
    # Auxiliary Methods #
    # ################# #
    
    def __is_in_junction(self, agent_position):

        if np.array_equiv([6, 7], agent_position) \
                or np.array_equiv([6, 6], agent_position) \
                or np.array_equiv([7, 6], agent_position) \
                or np.array_equiv([7, 7], agent_position):
            return True
        return False
        