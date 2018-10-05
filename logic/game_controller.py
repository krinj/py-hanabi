# -*- coding: utf-8 -*-

"""
<ENTER DESCRIPTION HERE>
"""
from typing import List

from logic.command import Command
from logic.command_add_tokens import CommandAddTokens
from logic.command_next_player import CommandNextPlayer
from py_hanabi.agent import Agent
from py_hanabi.card import Card
from py_hanabi.state import State

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class GameController:

    def __init__(self):

        self.agents: List[Agent] = []
        for i in range(4):
            self.agents.append(Agent(i))

        self.state: State = State()
        self.history: List[Command] = []
        deck = Card.generate_deck()
        self.state.reset(len(self.agents), deck, 8, 3)

        self.history.append(Command())
        self.command_index: int = 0

        for i in range(10):
            self.play()

    @property
    def latest_command_index(self) -> int:
        return len(self.history) - 1

    def step(self):
        command = CommandAddTokens()
        self.history.append(command)

    def add_command(self, command: Command):
        self.history.append(command)
        self.set_command_index(self.latest_command_index)

    def play(self):
        """ Execute a turn in the game. """

        # First, step to the latest command.
        self.set_command_index(self.latest_command_index)
        self.add_command(CommandNextPlayer())

        agent = self.agents[self.state.player_index]
        commands = agent.play_command(self.state)

        for c in commands:
            self.add_command(c)

        # print("Round\n")
        # agent = self.agents[self.state.player_index]
        # action = agent.play(self.state)
        # self._execute_action(action)
        # print(f"Playable Cards: {self.state.playable_cards}")
        # print(f"Player {self.state.player_index} Hand: {self.state.get_player_hand(self.state.player_index)}")
        # print(f"Action: {action}")
        # print(f"Deck Size: {len(self.state.deck)}")
        # self.state.on_round_end()
        # self._cycle_player()

    def set_command_index(self, index: int):
        while self.command_index != index:
            if self.command_index < index:
                self.command_index += 1
                self.history[self.command_index].forward(self.state)
            else:
                self.history[self.command_index].back(self.state)
                self.command_index -= 1
