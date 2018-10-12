# -*- coding: utf-8 -*-

"""
The current state of the game.
"""

from itertools import chain
from typing import List, Dict
from py_hanabi.card import Card, Color
from py_hanabi.card_matrix import CardCounter
from py_hanabi.settings import N_HINT_TOKENS_MAX

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class State:
    def __init__(self):

        # Player State
        self.player_index: int = 0  # The current player.
        self.hands: List[List[Card]] = []  # List of each player's hands.

        # Common Cards
        self._discard_pile: List[Card] = []
        self._fireworks: List[Card] = []
        self.deck: List[Card] = []
        self.all_cards: List[Card] = []

        # Tokens
        self.hint_tokens = 0
        self.fuse_tokens = 0
        self.grace_rounds: int = 0

        # State Temporary Maps.
        self._playable_cards: List[Card] = None
        self._playable_card_map: Dict[tuple, bool] = None
        self._number_map: Dict[Color, int] = None
        self._block_map: Dict[Color, bool] = None

    def set_dirty(self):
        self._playable_cards = None
        self._playable_card_map = None
        self._number_map = None
        self._block_map = None

    def reset(self, n_players: int, deck: List[Card], hint_tokens: int, fuse_tokens: int):

        self.hands.clear()
        for i in range(n_players):
            self.hands.append([])

        self.player_index = 0
        self.deck = deck
        self.all_cards = deck[:]
        self._discard_pile.clear()
        self._fireworks.clear()
        self._draw_initial_cards()

        self.hint_tokens = hint_tokens
        self.fuse_tokens = fuse_tokens
        self.grace_rounds = n_players + 1

    def _draw_initial_cards(self):
        """ Draw the starting cards for the game. """
        n_cards_to_draw = 5 if self.number_of_players < 4 else 4
        for i in range(self.number_of_players):
            self._draw_card(i, n_cards_to_draw)

    def _draw_card(self, player_index: int, amount: int = 1):
        """ Draw a number of cards from the deck. """
        for _ in range(amount):
            if len(self.deck) == 0:
                break
            card = self.deck.pop()
            self.hands[player_index].append(card)

    def get_player_hand(self, player_index: int):
        return self.hands[player_index]

    # ===================================================================================================
    # State modification.
    # ===================================================================================================

    def add_to_discard_pile(self, card: Card):
        self._discard_pile.append(card)
        self.set_dirty()

    def pop_from_discard_pile(self) -> Card:
        card = self._discard_pile.pop()
        self.set_dirty()
        return card

    def add_to_fireworks(self, card: Card):
        self._fireworks.append(card)
        self.set_dirty()

    def pop_from_fireworks(self) -> Card:
        card = self._fireworks.pop()
        self.set_dirty()
        return card

    @property
    def playable_cards(self) -> List[Card]:
        """ Get a list of all possible playable cards. """
        if self._playable_cards is None:
            cards = []
            color_value_map = {}
            for color in Color:
                color_value_map[color] = 0

            for card in self.fireworks:
                color = card.color
                if color_value_map[color] < card.number:
                    color_value_map[color] = card.number

            for color in color_value_map:
                n = color_value_map[color]
                if n < 5:
                    card = Card(n + 1, color)
                    cards.append(card)
            self._playable_cards = cards
        return self._playable_cards

    @property
    def playable_map(self):
        if self._playable_card_map is None:
            self._playable_card_map = {}
            for card in self.playable_cards:
                self._playable_card_map[card.key] = True
        return self._playable_card_map

    @property
    def number_map(self):
        if self._number_map is None:
            self._number_map = {}
            for card in self.playable_cards:
                self._number_map[card.color] = card.number
        return self._number_map

    @property
    def blocked_map(self):
        """ Return a map of colors to bool, whether this color is completely blocked or not. """
        # A blocked color is one that can no longer be played because a part of the chain is discarded.
        if self._block_map is None:
            block_map: Dict[Color, bool] = {}
            for c in Color:
                block_map[c] = False

            # For each playable card...
            # Get the total number in the deck...
            # And check if the discard pile has depleted it.

            deck_map = CardCounter.deck_map
            for card in self.playable_cards:
                total_number = deck_map[card.key]
                for d_card in self.discard_pile:
                    if d_card == card:
                        total_number -= 1

                if total_number <= 0:
                    block_map[card.color] = True
                else:
                    block_map[card.color] = False

            self._block_map = block_map

        return self._block_map

    # ===================================================================================================
    # Querying Functions.
    # ===================================================================================================

    def is_card_playable(self, card: Card):
        return card.key in self.playable_map

    def get_discard_score(self, card: Card):

        if self.blocked_map[card.color]:
            # This card is no longer playable.
            return 1

        if card.number == 5:
            return 0

        if card.key in self.playable_map:
            return 0.2

        if card.color in self.number_map and card.number < self.number_map[card.color]:
            # This card is no longer playable.
            return 1

        all_visible = list(chain.from_iterable(self.hands))
        same_count = sum([1 for c in all_visible if c == card])

        if same_count >= 2:
            return 0.5

        return 0.3

    # ===================================================================================================
    # Property.
    # ===================================================================================================

    @property
    def game_ended(self) -> bool:
        return self.grace_rounds == 0 or self.fuse_tokens == 0

    @property
    def discard_pile(self) -> List[Card]:
        return self._discard_pile

    @property
    def fireworks(self) -> List[Card]:
        return self._fireworks

    @property
    def number_of_cards_in_deck(self) -> int:
        return len(self.deck)

    @property
    def number_of_players(self) -> int:
        return len(self.hands)

    @property
    def hint_token_capped(self) -> bool:
        return self.hint_tokens >= N_HINT_TOKENS_MAX

    @property
    def score(self) -> int:
        return len(self._fireworks)
