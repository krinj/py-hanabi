# -*- coding: utf-8 -*-

"""
The current state of the game.
"""
from itertools import chain
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
        self.all_cards: List[Card] = []

        # Tokens
        self.hint_tokens = 0
        self.fuse_tokens = 0
        self.rounds_left = None
        self.game_has_ended = False

    @property
    def number_of_players(self) -> int:
        return len(self.hands)

    def reset(self, n_players: int, deck: List[Card], hint_tokens: int, fuse_tokens: int):

        self.hands.clear()
        for i in range(n_players):
            self.hands.append([])

        self.deck = deck
        self.all_cards = deck[:]
        self.discard_pile.clear()
        self._draw_initial_cards()

        self.hint_tokens = hint_tokens
        self.fuse_tokens = fuse_tokens
        self.rounds_left = None
        self.game_has_ended = False

    def on_round_end(self):
        if self.rounds_left is None:
            if len(self.deck) == 0:
                self.rounds_left = 4
        else:
            self.rounds_left -= 1
            if self.rounds_left == 0:
                self.game_has_ended = True

    def _draw_initial_cards(self):
        """ Draw the starting cards for the game. """
        n_cards_to_draw = 5 if self.number_of_players < 4 else 4
        for i in range(self.number_of_players):
            self.draw_card(i, n_cards_to_draw)

    def draw_card(self, player_index: int, amount: int = 1):
        """ Draw a number of cards from the deck. """
        for _ in range(amount):
            if len(self.deck) == 0:
                break
            card = self.deck.pop()
            self.hands[player_index].append(card)

    @property
    def playable_cards(self) -> List[Card]:
        """ Get a list of all possible playable cards. """
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

        return cards

    def play_card(self, card: Card):
        print(f"Is Card Playable: {card}: {self.is_card_playable(card)}")
        if self.is_card_playable(card):
            self.fireworks.append(card)
        else:
            self.discard_pile.append(card)
            self.fuse_tokens -= 1

    @property
    def score(self) -> int:
        color_score = {}
        for card in self.fireworks:
            color = card.color
            if color not in color_score or card.number > color_score[color]:
                color_score[color] = card.number

        score = sum([color_score[k] for k in color_score])
        return score

    def get_player_hand(self, player_index: int):
        return self.hands[player_index]

    # ===================================================================================================
    # Querying Functions.
    # ===================================================================================================

    def is_card_playable(self, card: Card):
        for playable_card in self.playable_cards:
            if playable_card == card:
                return True
        return False

    def get_discard_score(self, card: Card):

        for p in self.playable_cards:
            if p.color == card.color:
                if p.number > card.number:
                    return 1

        if card.number == 5:
            return 0

        for p in self.playable_cards:
            if p == card:
                return 0.2

        all_visible = list(chain.from_iterable(self.hands))
        same_count = sum([1 for c in all_visible if c == card])

        if same_count >= 2:
            print("Same Card")
            return 0.5

        return 0.3

    # ===================================================================================================
    # Property.
    # ===================================================================================================

    @property
    def number_of_cards_in_deck(self) -> int:
        return len(self.deck)
