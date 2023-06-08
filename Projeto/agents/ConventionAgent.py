import numpy as np
from aasma import Agent
from enum import Enum

N_ACTIONS = 2
GAS, BREAK = range(N_ACTIONS)


class Pre_Junction(Enum):
    TOP = [5, 6]
    LEFT = [7, 5]
    DOWN = [8, 7]
    RIGHT = [6, 8]
    # Ordered counter-clockwise directions
    DIRECTION = [TOP, LEFT, DOWN, RIGHT]

class Junction_Pos(Enum):
    TOP_LEFT = [6, 6]
    BOTTOM_LEFT = [7, 6]
    BOTTOM_RIGHT = [7, 7]
    TOP_RIGHT = [6, 7]
    # Ordered counter-clockwise directions
    DIRECTION = [TOP_LEFT, BOTTOM_LEFT, BOTTOM_RIGHT, TOP_RIGHT]

class Movement(Enum):
    DOWNWARDS = "Downwards"
    LEFTWARDS = "Leftwards"
    UPWARDS = "Upwards"
    RIGHTWARDS = "Rightwards"
    # Ordered counter-clockwise directions
    DIRECTION = [DOWNWARDS, LEFTWARDS, UPWARDS, RIGHTWARDS]

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
        self.visited_positions = []
        self.moving_direction = ""
        self.pre_junction_pos = []


    def action(self) -> int:

        # middle cell of a 5x5 grid, and position on the list of coordinates
        agent_position = self.observation[2][2][self.n_agents:self.n_agents + 2]

        agent_route = self.observation[2][2][self.n_agents + 2:]

        # get all the positions nearby agents that it can observe, except himself
        near_agents = self.__get_near_agents(agent_position)

        # stops at the intersection, gives priority to the right, if a car is in the junction stops
        # currently top has priority and always advances if no car is in the junction

        self.__update_moving_direction(agent_position, agent_route)

        action = self.__get_action(agent_position, near_agents)

        #action_v2 = self.get_action_v2(agent_position, agent_route, near_agents)

        return action

    # ################# #
    # Auxiliary Methods #
    # ################# #

    def __get_near_agents(self, agent_position):
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
                # checks if it's not the agent itself
                if 1 in cell and not np.array_equiv(cell[self.n_agents:self.n_agents + 2], agent_position):
                    near_agents.append([cell[self.n_agents:self.n_agents + 2], cell[self.n_agents + 2:]])

        return near_agents

    # hardcoded see if its in the junction
    def __is_in_junction(self, agent_position):

        if np.array_equiv([6, 7], agent_position) \
                or np.array_equiv([6, 6], agent_position) \
                or np.array_equiv([7, 6], agent_position) \
                or np.array_equiv([7, 7], agent_position):
            return True
        return False

    def __pre_junction(self, agent_position):
        if np.array_equiv(Pre_Junction.TOP.value, agent_position):
            return Pre_Junction.TOP.value

        elif np.array_equiv(Pre_Junction.RIGHT.value, agent_position):
            return Pre_Junction.RIGHT.value

        elif np.array_equiv(Pre_Junction.DOWN.value, agent_position):
            return Pre_Junction.DOWN.value

        elif np.array_equiv(Pre_Junction.LEFT.value, agent_position):
            return Pre_Junction.LEFT.value
        return []

    def __update_moving_direction(self, agent_position, agent_route):
        if self.__is_in_junction(agent_position) and (list(agent_position) not in self.visited_positions):
            self.visited_positions += [list(agent_position)]

        if list(agent_position) in Junction_Pos.DIRECTION.value:
            # Forward
            if agent_route[0] == 1:
                # Turns 0 in counter-clockwise direction (stays the same direction)
                pass
            # Right
            elif agent_route[1] == 1:
                # Turns 1 in counter-clockwise direction (turns right)
                index = Pre_Junction.DIRECTION.value.index(self.pre_junction_pos)
                self.moving_direction = Movement.DIRECTION.value[(index + 1) % 4]
            # Left
            elif agent_route[2] == 1:
                # This means it's time to turn
                if len(self.visited_positions) == 2:
                    # Turns 3 in counter-clockwise direction (turns left)
                    index = Pre_Junction.DIRECTION.value.index(self.pre_junction_pos)
                    self.moving_direction = Movement.DIRECTION.value[(index + 3) % 4]
                else:
                    # Turns 0 in counter-clockwise direction (stays the same direction)
                    pass
        elif agent_position[1] == 6:
            self.moving_direction = Movement.DOWNWARDS.value
        elif agent_position[1] == 7:
            self.moving_direction = Movement.UPWARDS.value
        elif agent_position[0] == 7:
            self.moving_direction = Movement.RIGHTWARDS.value
        elif agent_position[0] == 6:
            self.moving_direction = Movement.LEFTWARDS.value
        #print(f"Agent {self.agent_id} is turning {agent_route}, moving {self.moving_direction}, next position {self.get_next_position(agent_position)} ")

    def __get_next_position(self, agent_position, moving_direction):
        if moving_direction == Movement.DOWNWARDS.value:
            return agent_position[0] + 1, agent_position[1]
        elif moving_direction == Movement.UPWARDS.value:
            return agent_position[0] - 1, agent_position[1]
        elif moving_direction == Movement.RIGHTWARDS.value:
            return agent_position[0], agent_position[1] + 1
        elif moving_direction == Movement.LEFTWARDS.value:
            return agent_position[0], agent_position[1] - 1
        return []

    def __get_action(self, agent_position, near_agents):
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
        is_pre_junction = self.__pre_junction(agent_position)
        if is_pre_junction:
            self.pre_junction_pos = is_pre_junction
        agent_next_position = self.__get_next_position(agent_position)

        # If agent is in the junction, keep moving
        if self.__is_in_junction(agent_position):
            return GAS

        # If there are agents nearby might need to stop
        if near_agents:
            # If it hasn't yet reached the entrance of the junction
            if not is_pre_junction:
                for near_agent in near_agents:
                    if np.array_equiv(near_agent[0], agent_next_position):
                        # print(f"Agent {self.agent_id} in {agent_position} didn't want to crash with Agent {near_agent[0]} in position")
                        return BREAK
            # If it has already reached the entrance of the junction
            else:
                if near_agents:
                    for near_agent in near_agents:
                        index = Pre_Junction.DIRECTION.value.index(is_pre_junction)
                        # If there is another agent in the junction
                        if self.__is_in_junction(near_agent[0]):
                            return BREAK

                        near_agent_pos = self.__pre_junction(near_agent[0])
                        # If another agent is in the entrance of the junction - obtains yield properties
                        if near_agent_pos:
                            # Checks if near agent is in the top - top is hardcoded as max priority
                            if not (Pre_Junction.DIRECTION.value[index] == Pre_Junction.TOP.value) and near_agent_pos == Pre_Junction.DIRECTION.value[(index + 1) % 4]:
                                return BREAK
                            # If top is max priority, left must yield to everyone
                            if Pre_Junction.DIRECTION.value[index] == Pre_Junction.LEFT.value:
                                return BREAK
        return GAS
