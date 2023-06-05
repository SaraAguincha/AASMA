import numpy as np
from aasma import Agent
from enum import Enum

N_ACTIONS = 2
GAS, BREAK = range(N_ACTIONS)


# TOP, RIGHT, DOWN, LEFT = [6, 8], [8, 7], [7, 5], [5, 6]

class Ways(Enum):
    TOP = [6, 8]
    DOWN = [7, 5]
    LEFT = [5, 6]
    RIGHT = [8, 7]
    # Ordered counter-clockwise directions
    DIRECTION = [TOP, LEFT, DOWN, RIGHT]

class Junction_Pos(Enum):
    TOP_LEFT = [6, 7]
    BOTTOM_LEFT = [6, 6]
    BOTTOM_RIGHT = [7, 6]
    TOP_RIGHT = [7, 7]
    # Ordered counter-clockwise directions
    DIRECTION = [TOP_LEFT, BOTTOM_LEFT, BOTTOM_RIGHT, TOP_RIGHT]

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
        # action_v1 = self.get_action_v1(agent_position, near_agents)

        #action_v2 = self.get_action_v2(agent_position, agent_route, near_agents)

        action_v3 = self.get_action_v3(agent_position, agent_route, near_agents)

        return action_v3

    # ################# #
    # Auxiliary Methods #
    # ################# #

    def get_near_agents(self, observation, n_agents, agent_position):
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

    # hardcoded see if its in the junction
    def is_in_junction(self, agent_position):

        if np.array_equiv([6, 7], agent_position) \
                or np.array_equiv([6, 6], agent_position) \
                or np.array_equiv([7, 6], agent_position) \
                or np.array_equiv([7, 7], agent_position):
            return True
        return False

    # hardcoded positions to define where they are in junction (not called in junction)
    def junction_position(self, agent_position):

        if agent_position[0] == 6 or agent_position[0] == 7:
            return "VERTICAL"

        return "HORIZONTAL"

    def pre_junction(self, agent_position):
        if np.array_equiv(Ways.TOP.value, agent_position):
            return Ways.TOP.value

        elif np.array_equiv(Ways.RIGHT.value, agent_position):
            return Ways.RIGHT.value

        elif np.array_equiv(Ways.DOWN.value, agent_position):
            return Ways.DOWN.value

        elif np.array_equiv(Ways.LEFT.value, agent_position):
            return Ways.LEFT.value
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
                        index = Ways.DIRECTION.value.index(agent_pos)
                        # Checks if near agent is in the right
                        if near_agent_pos == Ways.DIRECTION.value[(index + 1) % 3]:
                            return BREAK

                        # TODO improve this dumb verifications
                        # if agent_pos == RIGHT and near_agent_pos == TOP:
                        #     return BREAK
                        #
                        # elif agent_pos == DOWN and near_agent_pos == RIGHT:
                        #     return BREAK
                        #
                        # elif agent_pos == LEFT and near_agent_pos == DOWN:
                        #     return BREAK

        return GAS

    def get_action_v2(self, agent_position, agent_route, near_agents):
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

        # if agent will turn right has priority and will advance
        if agent_pos and not (agent_route[1] == 1):
            if near_agents:
                for agent in near_agents:
                    # in case there is an agent in the junction and is not turning right
                    if self.is_in_junction(agent[0]) and not (agent[1][1] == 1):
                        return BREAK

                    # in case the agent is in one of the 4 positions
                    near_agent_pos = self.pre_junction(agent[0])
                    if near_agent_pos:
                        index = Ways.DIRECTION.value.index(agent_pos)
                        # Checks if near agent is in the right
                        if near_agent_pos == Ways.DIRECTION.value[(index + 1) % 3]:
                            return BREAK

                        # # TODO improve this dumb verifications
                        # if agent_pos == Ways.RIGHT.value and near_agent_pos == Ways.TOP.value:
                        #     return BREAK
                        #
                        # elif agent_pos == Ways.DOWN.value and near_agent_pos == Ways.RIGHT.value:
                        #     return BREAK
                        #
                        # elif agent_pos == Ways.LEFT.value and near_agent_pos == Ways.DOWN.value:
                        #     return BREAK

        return GAS

    def get_action_v3(self, agent_position, agent_route, near_agents):
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

        # if agent will turn right has priority and will advance
        if agent_pos and not (agent_route[1] == 1):
            if near_agents:
                for agent in near_agents:
                    index = Ways.DIRECTION.value.index(agent_pos)
                    # in case there is an agent in the junction and is not turning right
                    if self.is_in_junction(agent[0])\
                            and not (agent[1][1] == 1)\
                            and not (np.array_equiv(agent[0], Junction_Pos.DIRECTION.value[(index + 2) % 3])):
                        return BREAK

                    # if self.is_in_junction(agent[0]) and not (agent[1][1] == 1):
                    #     if np.array_equiv(agent[0], Junction_Pos.DIRECTION.value[(index + 2) % 3]):
                    #         print("HERE!")

                    # in case the agent is in one of the 4 positions
                    near_agent_pos = self.pre_junction(agent[0])
                    if near_agent_pos:
                        # Checks if near agent is in the right
                        if near_agent_pos == Ways.DIRECTION.value[(index + 1) % 3]:
                            return BREAK

                        # # TODO improve this dumb verifications
                        # if agent_pos == Ways.RIGHT.value and near_agent_pos == Ways.TOP.value:
                        #     return BREAK
                        #
                        # elif agent_pos == Ways.DOWN.value and near_agent_pos == Ways.RIGHT.value:
                        #     return BREAK
                        #
                        # elif agent_pos == Ways.LEFT.value and near_agent_pos == Ways.DOWN.value:
                        #     return BREAK

        return GAS
