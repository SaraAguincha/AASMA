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

        action = self.get_action(agent_position, near_agents)
        return action
        

    # ################# #
    # Auxiliary Methods #
    # ################# #
    
    def get_near_agents(self,observation, n_agents):
        """
        TODO - add description for observation
        
        Given the agent observation (currently a grid of 3x3, it returns
        a list of the positions of the near agents.

        Args:
            observation (list): _description_
            n_agents (int): it represents how many agents are in the simulation

        Returns:
            list: List of lists, each sublist has a nearby agent position
        """
        near_agents = []
        
        # While that goes through the whole observation. When there is a 1 in the first n_agents + 5 elements
        # it means that there is an agent there. Also verifies if it's not itself
        i = 0
        while i < len(self.observation):
            if 1 in self.observation[i :i + n_agents + 5] and not(4 * (n_agents + 5) <= i <= 5 * (n_agents + 5)):
                near_agents.append(list(self.observation[i + n_agents : i + n_agents + 2]))
                i += n_agents + 5
                
            i += n_agents + 5
           
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
                
                if agent[0] >= agent_position[0]:
                    
                    if agent[1] <= agent_position[1]:
                        return BREAK
                    else:
                        return GAS
                
                else:
                    if agent[1] >= agent_position[1]:
                        return BREAK
                    else:
                        return GAS
        return GAS