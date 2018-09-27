# -*- coding: utf-8 -*-

"""
The current state of the game.
"""

from typing import List
from py_hanabi.card import Card, Color

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class State:
    def __init__(self):

        # Player State
        self.player_index: int = 0  # The current player.
        self.hands: List[List[Card]] = []  # List of each player's hands.

        # Common Cards
        self.discard_pile: List[Card] = []
        self.deck: List[Card] = []
        self.fireworks: List[Card] = []

        # Tokens
        self.hint_tokens = 0
        self.fuse_tokens = 0

    @property
    def number_of_players(self) -> int:
        return len(self.hands)

    def reset(self, n_players: int, deck: List[Card], hint_tokens: int, fuse_tokens: int):

        self.hands.clear()
        for i in range(n_players):
            self.hands.append([])

        self.deck = deck
        self.discard_pile.clear()
        self._draw_initial_cards()

        self.hint_tokens = hint_tokens
        self.fuse_tokens = fuse_tokens

    def _draw_initial_cards(self):
        """ Draw the starting cards for the game. """
        n_cards_to_draw = 5 if self.number_of_players < 4 else 4
        for i in range(self.number_of_players):
            self.draw_card(i, n_cards_to_draw)

    def draw_card(self, player_index: int, amount: int=1):
        """ Draw a number of cards from the deck. """
        for _ in range(amount):
            card = self.deck.pop()
            self.hands[player_index].append(card)
            if len(self.deck) == 0:
                break

    @property
    def playable_cards(self) -> List[Card]:
        """ Get a list of all possible playable cards. """
        cards = []
        for color in Color:

            pass

        return cards
