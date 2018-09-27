# -*- coding: utf-8 -*-

"""
This is an instance of a Hanabi game.
"""

import random
from typing import List

from py_hanabi.action import Action
from py_hanabi.agent import Agent
from py_hanabi.card import Card, Color
from py_hanabi.settings import N_HINT_TOKENS_MAX, N_FUSE_TOKENS_MAX, CARD_DECK_DISTRIBUTION
from py_hanabi.state import State

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class Hanabi:

    def __init__(self):
        self.state: State = State()
        self.agents: List[Agent] = []

    def simulate_game(self, agents: List[Agent]):
        assert(2 <= len(agents) <= 5)
        self.agents = agents
        self._reset()

        while not self._is_game_over(self.state):
            self._play()

        print("Game is over")

    def _reset(self):
        """ Reset the simulator and board state. """
        deck = self._generate_deck()
        self.state.reset(self.number_of_agents, deck, N_HINT_TOKENS_MAX, N_FUSE_TOKENS_MAX)

    def _play(self):
        """ Execute a turn in the game. """
        print("Play")
        agent = self.agents[self.state.player_index]
        action = agent.play(self.state)
        self.state.fuse_tokens -= 1
        self._execute_action(action)

    def _execute_action(self, action: Action) -> None:
        pass

    def _is_game_over(self, state: State) -> bool:
        if state.fuse_tokens == 0:
            return True
        return False

    def _generate_deck(self) -> List[Card]:
        """ Generate the starting deck for the game. """
        deck: List[Card] = []
        for color in Color:
            for i in CARD_DECK_DISTRIBUTION:
                card = Card(i, color)
                deck.append(card)

        random.shuffle(deck)
        return deck

    @property
    def number_of_agents(self) -> int:
        return len(self.agents)