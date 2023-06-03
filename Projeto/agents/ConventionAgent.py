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
        
        # self.__in_junction = False
        

    def action(self) -> int:        
        
        # middle cell of a 5x5 grid, and position on the list of coordinates
        agent_position = self.observation[2][2][self.n_agents:self.n_agents + 2]
        
        agent_route = self.observation[2][2][self.n_agents + 2:]
        
        # get all the positions nearby agents that it can observe, except himself
        near_agents = self.get_near_agents(self.observation, self.n_agents, agent_position)   


        if self.is_in_junction(agent_position):
            self.__in_junction = True

        #print(self.junction_position(agent_position))

        #action = self.get_action(agent_position, agent_route, near_agents)
        
        
        action_stop_junction = self.get_action_junction_related(agent_position, agent_route, near_agents)

        
        return action_stop_junction
        

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
                if 1 in cell and not np.array_equiv(cell[4:6], agent_position):
                    near_agents.append([cell[4:6], cell[6:]])
        
        return near_agents
        
        
        
        
    def get_action(self, agent_position, route, near_agents):
        """
        With the arguments given, returns the action the
        agent should take based on its observation
        
        TODO - should it take into account the direction the other car wants to go?

        Args:
            agent_position (array): has the coordinates of the agent
            near_agents (list): list of lists, each has the coordinates of nearby agents

        Returns:
            int: action that the agent will take
        """
        
        # currently it is giving priority to the car coming through the north, if all of them arrive at the same time
        # in the future it should prioritize the one with more traffic
        
        # agent[0] is agent position, agent[1] is agent route
        
        
        # if agent is turning right it has priority
        if route[1] == 1:
            return GAS
        
        
        agent_x, agent_y = agent_position   # agent current coordinates
        agent_loc = self.junction_position(agent_position)

        
        if self.pre_junction(agent_position):
            if near_agents:
                for agent in near_agents:
                    if agent_loc == "HORIZONTAL":
                # means we are before junction coming from the right and there is a car on our right
                        if agent_x > agent[0][0]:
                            if agent_y < agent[0][1]:
                                return BREAK
                            #elif agent_x + 1 == agent[0][0]:
                            #    continue
                        
                        else:
                            if agent_y < agent[0][1]:
                                return BREAK
                            
                
                # since communication is still not working, for now the north will not give rights
                    else:
                        if agent_x < agent[0][0] and agent_y < agent[0][1]:
                            return BREAK
        return GAS
    
    
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
        
        if np.array_equiv(TOP, agent_position) \
            or np.array_equiv(RIGHT, agent_position) \
            or np.array_equiv(DOWN, agent_position) \
            or np.array_equiv(LEFT, agent_position):
            
            return True
        return False
    
    
    
    
    
    
    ## TODO, future test in agents. Stops if one agent is in the junction
    def get_action_junction_related(self, agent_position, route, near_agents):
        """
        With the arguments given, stops if someone in junction
        
        TODO - should it take into account the direction the other car wants to go?

        Args:
            agent_position (array): has the coordinates of the agent
            near_agents (list): list of lists, each has the coordinates of nearby agents

        Returns:
            int: action that the agent will take
        """
        
        # currently it is giving priority to the car coming through the north, if all of them arrive at the same time
        # in the future it should prioritize the one with more traffic
        
        # agent[0] is agent position, agent[1] is agent route
        
        
        # if agent is turning right it has priority
        
        
        
        agent_x, agent_y = agent_position   # agent current coordinates
        agent_loc = self.junction_position(agent_position)

        
        if self.pre_junction(agent_position):
            if near_agents:
                for agent in near_agents:
                    
                    if self.is_in_junction(agent):
                        return BREAK
                    
                    if self.pre_junction(agent):
                        continue
                    
                    if agent_loc == "HORIZONTAL":
                # means we are before junction coming from the right and there is a car on our right
                        if agent_x > agent[0][0]:
                            if agent_y < agent[0][1]:
                                return BREAK
                            #elif agent_x + 1 == agent[0][0]:
                            #    continue
                        
                        else:
                            if agent_y < agent[0][1]:
                                return BREAK
                            
                
                # since communication is still not working, for now the north will not give rights
                    else:
                        if agent_x < agent[0][0] and agent_y < agent[0][1]:
                            return BREAK
                        
                
        return GAS