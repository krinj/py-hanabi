# -*- coding: utf-8 -*-

"""
<ENTER DESCRIPTION HERE>
"""
from typing import List

from logic.command import Command
from logic.command_next_player import CommandNextPlayer
from py_hanabi import analyzer
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

        self.command_index: int = 0
        self.state: State = State()
        self.history: List[Command] = []

        self.reset()

    def reset(self):
        self.state: State = State()
        self.history: List[Command] = []
        self.history.append(Command("Initialize Board", "Set up the game board."))
        deck = Card.generate_deck()
        self.state.reset(len(self.agents), deck, 8, 3)
        self.command_index: int = 0

    def auto_play(self):

        games = 3
        total_score = 0
        total_games = 0

        while games > 0:
            games -= 1
            game_ended = False
            self.reset()
            while not game_ended:
                game_ended = self.play()
            total_score += self.state.score
            total_games += 1

        average_score = total_score/total_games
        print(f"Average Score over {total_games} games: {average_score}")

    @property
    def latest_command_index(self) -> int:
        return len(self.history) - 1

    def add_command(self, command: Command):
        self.history.append(command)
        self.set_command_index(self.latest_command_index)

    def play(self):
        """ Execute a turn in the game. """

        # First, step to the latest command.
        self.set_command_index(self.latest_command_index)
        print(f"Play: {self.state.number_of_cards_in_deck}")

        if self.state.game_ended:
            return True

        agent = self.agents[self.state.player_index]
        commands = agent.play_command(self.state)
        for c in commands:
            self.add_command(c)

        self.add_command(CommandNextPlayer())

        if self.state.game_ended:
            self.history.append(Command("Game Over", "The game is over."))
            analyzer.write_timers()
            return True

        return False

    def set_command_index(self, index: int):
        while self.command_index != index:
            if self.command_index < index:
                self.command_index += 1
                self.history[self.command_index].forward(self.state)
            else:
                self.history[self.command_index].back(self.state)
                self.command_index -= 1
