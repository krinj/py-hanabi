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
        self.loop_breaker: int = 9000

    def simulate_game(self, agents: List[Agent]):
        assert (2 <= len(agents) <= 5)
        self.agents = agents
        self._reset()

        while not self._is_game_over(self.state):
            self._play()

        print("Game is over")
        print(f"Score: {self.state.score}")

    def _reset(self):
        """ Reset the simulator and board state. """
        deck = self._generate_deck()
        self.loop_breaker = 9000
        self.state.reset(self.number_of_agents, deck, N_HINT_TOKENS_MAX, N_FUSE_TOKENS_MAX)

    def _play(self):
        """ Execute a turn in the game. """
        print("Round\n")
        agent = self.agents[self.state.player_index]
        action = agent.play(self.state)
        self._execute_action(action)
        print(f"Action: {action}")
        print(f"Deck Size: {len(self.state.deck)}")

    def _execute_action(self, action: Action) -> None:
        action.execute(self.state)
        pass

    def _is_game_over(self, state: State) -> bool:

        if state.number_of_cards_in_deck == 0:
            return True

        if state.fuse_tokens == 0:
            return True

        if self.loop_breaker == 0:
            return True
        else:
            self.loop_breaker -= 1

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
