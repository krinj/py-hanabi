# -*- coding: utf-8 -*-

"""
This is the Hanabi simulator engine.
It first sets up the game state based on the settings.
Then it modifies the state based on a sequence of commands.
It allows the user to scrub back and forth between all actions.
"""

from typing import List
from py_hanabi.commands.command import Command
from py_hanabi.commands.command_next_player import CommandNextPlayer
from py_hanabi.agent import Agent
from py_hanabi.card import Card
from py_hanabi.settings import N_HINT_TOKENS_MAX, N_FUSE_TOKENS_MAX, N_PLAYERS
from py_hanabi.state import State

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class Engine:

    def __init__(self):

        # Create the agents.
        self.agents: List[Agent] = []
        for i in range(N_PLAYERS):
            self.agents.append(Agent(i))

        self.command_index: int = 0
        self.state: State = State()
        self.history: List[Command] = []
        self.reset()

    def reset(self):
        """ Reset the entire state of this controller for a new game. """
        self.state = State()
        self.history = []
        self.history.append(Command("Initialize Board", "Set up the game board."))
        self.state.reset(len(self.agents), Card.generate_deck(), N_HINT_TOKENS_MAX, N_FUSE_TOKENS_MAX)
        self.command_index: int = 0

    @property
    def latest_command_index(self) -> int:
        """ Get the index of the latest command. """
        return len(self.history) - 1

    def add_command(self, command: Command):
        """ Add a command to the history list."""
        self.history.append(command)
        self.set_command_index(self.latest_command_index)

    def play(self) -> bool:
        """ Execute a turn in the game. """

        # First, step to the latest command.
        self.set_command_index(self.latest_command_index)
        if self.state.game_ended:
            return True

        # Play out the command.
        agent = self.agents[self.state.player_index]
        commands = agent.play_command(self.state)
        for c in commands:
            self.add_command(c)

        # Switch the player.
        self.add_command(CommandNextPlayer())

        # Check for game ending.
        if self.state.game_ended:
            self.history.append(Command("Game Over", "The game is over."))
            print(f"Game Ended. Score: {self.state.score}")
            return True

        return False

    def set_command_index(self, index: int) -> None:
        """ Scrub the state of this game to the specified command index. """
        while self.command_index != index:
            if self.command_index < index:
                self.command_index += 1
                self.history[self.command_index].forward(self.state)
            else:
                self.history[self.command_index].back(self.state)
                self.command_index -= 1
