from aasma import Agent
from agents import CommunicatingAgent
import numpy as np


class CommunicationHandler:

    def __init__(self):
        self.agents = None

    def update_agents(self, agents: list[CommunicatingAgent]):
        self.agents = agents

    def request_moving_direction(self, agent_position):
        receiving_agent = None
        for agent in self.agents:
            if np.array_equiv(agent_position, agent.get_agent_position()):
                receiving_agent = agent
                break
        if receiving_agent:
            return receiving_agent.get_moving_direction()

    def send_waiting_time(self, agent_position, waiting_time, axis):
        receiving_agent = None
        for agent in self.agents:
            if np.array_equiv(agent_position, agent.get_agent_position()):
                receiving_agent = agent
                break
        if receiving_agent:
            receiving_agent.receive_waiting_time(waiting_time, axis)
