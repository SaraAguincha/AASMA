import numpy as np
from aasma import Agent

class RandomAgent(Agent):
    """
    A baseline agent for the TrafficJunction environment.
    The Random agent randomly decides if it will advance, or stop.
    """

    def __init__(self, n_actions: int):
        super(RandomAgent, self).__init__("Random Agent")
        self.n_actions = n_actions

    def action(self) -> int:        
        return np.random.randint(self.n_actions), 0