import numpy as np
from aasma import Agent

N_ACTIONS = 2
GAS, BREAK = range(N_ACTIONS)

TOP, RIGHT, DOWN, LEFT = [6,8], [8,7], [7,5], [5,6]


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
        agent_position = self.observation[2][2][self.n_agents:self.n_agents + 2]
        
        agent_route = self.observation[2][2][self.n_agents + 2:]
        
        # get all the positions nearby agents that it can observe, except himself
        near_agents = self.get_near_agents(self.observation, self.n_agents, agent_position)   

        # stops at the intersection, gives priority to the right, if a car is in the junction stops
        # currently top has priority and always advances if no car is in the junction
        action_v1 = self.get_action_v1(agent_position, near_agents)
        
        return action_v1
        

    # ################# #
    # Auxiliary Methods #
    # ################# #
    
    def get_near_agents(self,observation, n_agents, agent_position):
        """
        TODO - add description for observation
        
        Given the agent observation (currently a grid of 5x5, it returns
        a array of the positions of the near agents, and their current route.

        Args:
            observation (array): _description_
            n_agents (int): it represents how many agents are in the simulation

        Returns:
            list: List of arrays, each array has a nearby agent position and their respective route
        """
        near_agents = []
        
        # Goes through the whole observation row by row, checking each cell for nearby agents
        for row in self.observation:
            for cell in row:
                # checks if its not the agent itself
                if 1 in cell and not np.array_equiv(cell[self.n_agents:self.n_agents + 2], agent_position):
                    near_agents.append([cell[self.n_agents:self.n_agents + 2], cell[self.n_agents + 2:]])
        
        return near_agents
        
        
        
        
    # def get_action(self, agent_position, route, near_agents):
    #     """
    #     With the arguments given, returns the action the
    #     agent should take based on its observation
        
    #     TODO - should it take into account the direction the other car wants to go?

    #     Args:
    #         agent_position (array): has the coordinates of the agent
    #         near_agents (list): list of lists, each has the coordinates of nearby agents

    #     Returns:
    #         int: action that the agent will take
    #     """
        
    #     # currently it is giving priority to the car coming through the north, if all of them arrive at the same time
    #     # in the future it should prioritize the one with more traffic
        
    #     # agent[0] is agent position, agent[1] is agent route
        
        
    #     # if agent is turning right it has priority
    #     if route[1] == 1:
    #         return GAS
        
        
    #     agent_x, agent_y = agent_position   # agent current coordinates
    #     agent_loc = self.junction_position(agent_position)


        
    #     if self.pre_junction(agent_position):
    #         if near_agents:
    #             for agent in near_agents:
    #                 if agent_loc == "HORIZONTAL":
    #             # means we are before junction coming from the right and there is a car on our right
    #                     if agent_x > agent[0][0]:
    #                         if agent_y < agent[0][1]:
    #                             return BREAK
    #                         #elif agent_x + 1 == agent[0][0]:
    #                         #    continue
                        
    #                     else:
    #                         if agent_y < agent[0][1]:
    #                             return BREAK
                            
                
    #             # since communication is still not working, for now the north will not give rights
    #                 else:
    #                     if agent_x < agent[0][0] and agent_y < agent[0][1]:
    #                         return BREAK
    #     return GAS
    
    
    # hardcoded see if its in the junction
    def is_in_junction(self, agent_position):
        
        if np.array_equiv([6,7], agent_position) \
            or np.array_equiv([6,6], agent_position) \
            or np.array_equiv([7,6], agent_position) \
            or np.array_equiv([7,7], agent_position):
            
            return True
        return False
    
    
    
    
    
    # hardcoded positions to define where they are in junction (not called in junction)
    def junction_position(self, agent_position):
        
        if agent_position[0] == 6 or agent_position[0] == 7:
            return "VERTICAL"
        
        return "HORIZONTAL"
    
    
    def pre_junction(self, agent_position):
        if np.array_equiv(TOP, agent_position):
            return TOP
        
        elif np.array_equiv(RIGHT, agent_position):
            return RIGHT
        
        elif np.array_equiv(DOWN, agent_position):
            return DOWN
        
        elif np.array_equiv(LEFT, agent_position):
            return LEFT
        return []
    
    
    
    
    
    
    ## TODO. Stops if one agent is in the junction, uses right of way
    # TODO, improve, TOP has always priority
    def get_action_v1(self, agent_position, near_agents):
        """
        With the arguments given, returns the action it should take. 
            - Stops if other car is in junction
            - Uses right of way rule
            - TOP has priority (to despute when all 4 are at the junction at the same time), improved when communication exists

        Args:
            agent_position (array): has the coordinates of the agent
            near_agents (list): list of lists, each has the coordinates of nearby agents

        Returns:
            int: action that the agent will take
        """
        
        # agent[0] is agent position, agent[1] is agent route
                
        # agent_pos will have only the list with positions if is in one of the 4 pre_junction_position        
        agent_pos = self.pre_junction(agent_position)

        if agent_pos:
            if near_agents:
                for agent in near_agents:
                    
                    # in case there is an agent in the junction
                    if self.is_in_junction(agent[0]):
                        return BREAK
                    
                    # in case the agent is in one of the 4 positions
                    near_agent_pos = self.pre_junction(agent[0])
                    if near_agent_pos:
                        
                        # TODO improve this dumb verifications
                        if agent_pos == RIGHT and near_agent_pos == TOP:
                            return BREAK
                        
                        elif agent_pos == DOWN and near_agent_pos == RIGHT:
                            return BREAK
                        
                        elif agent_pos == LEFT and near_agent_pos == DOWN:
                            return BREAK
                
        return GAS