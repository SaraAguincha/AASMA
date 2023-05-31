import numpy as np
from aasma import Agent

N_ACTIONS = 2
GAS, BREAK = range(N_ACTIONS)


class ConventionAgent(Agent):

    """
    A baseline agent for the TrafficJunction environment.
    The greedy agent always tries to advance to reach its destination faster,
    but follows the convention of giving priority to the car if it's on his right.
    """

    def __init__(self, agent_id, n_agents):
        super(ConventionAgent, self).__init__(f"Convention Agent")
        self.agent_id = agent_id
        self.n_agents = n_agents
        self.n_actions = N_ACTIONS
        

    def action(self) -> int:        
        
        # middle cell of a 5x5 grid, and position on the list of coordinates
        agent_position = self.observation[2][2][4:6]
        
        agent_route = self.observation[2][2][6:]
        
        # get all the positions nearby agents that it can observe, except himself
        near_agents = self.get_near_agents(self.observation, self.n_agents, agent_position)      

        # action = self.get_action(agent_position, near_agents)
        
        return GAS
        

    # ################# #
    # Auxiliary Methods #
    # ################# #
    
    def get_near_agents(self,observation, n_agents, agent_position):
        """
        TODO - add description for observation
        
        Given the agent observation (currently a grid of 3x3, it returns
        a array of the positions of the near agents.

        Args:
            observation (array): _description_
            n_agents (int): it represents how many agents are in the simulation

        Returns:
            list: List of arrays, each array has a nearby agent position
        """
        near_agents = []
        
        # Goes through the whole observation row by row, checking each cell for nearby agents
        for row in self.observation:
            for cell in row:
                # checks if its not the agent itself
                if 1 in cell and not np.array_equiv(cell[4:6], agent_position):
                    near_agents.append(cell[4:6])
        
        return near_agents
        
        
    def get_action(self, agent_position, near_agents):
        """
        With the arguments given, returns the action the
        agent should take based on its observation
        
        TODO - should it take into account the direction the other car wants to go?

        Args:
            agent_position (list): has the coordinates of the agent
            near_agents (list): list of lists, each has the coordinates of nearby agents

        Returns:
            int: action that the agent will take
        """
        
        # in case there are no agents nearby, agent moves
        if near_agents:
            for agent in near_agents:
                
                if agent[0] > agent_position[0]:
                    
                    if agent[1] <= agent_position[1]:
                        return BREAK
                    else:
                        return GAS
                
                else:
                    if agent[1] >= agent_position[1]:
                        return GAS
                    else:
                        return BREAK
        return GAS