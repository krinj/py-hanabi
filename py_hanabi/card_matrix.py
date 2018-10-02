# -*- coding: utf-8 -*-

"""
<ENTER DESCRIPTION HERE>
"""
from typing import Dict, List

from py_hanabi.card import Color, Card
from py_hanabi.settings import CARD_DECK_DISTRIBUTION

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class CardStat:
    def __init__(self):
        self.color: Color = None
        self.number: int = 0
        self.probability: float = 0.0
        self.rating_play: float = 0.0
        self.rating_discard: float = 0.0


class CardCounter:
    def __init__(self):
        self.card_map: Dict[str, int] = {}

        # Initialize an empty map.
        for c in Color:
            for n in range(1, 6):
                self.set(c, n, 0)

    @staticmethod
    def deck() -> 'CardCounter':
        card_counter = CardCounter()
        deck = Card.generate_deck()
        for card in deck:
            card_counter.add(card.color, card.number, 1)
        return card_counter

    def set(self, c: Color, n: int, value: int):
        key = Card.get_key(c, n)
        self.card_map[key] = value

    def add(self, c: Color, n: int, value: int):
        key = Card.get_key(c, n)
        self.card_map[key] += value

    def count(self, c: Color, n: int) -> int:
        key = Card.get_key(c, n)
        return self.card_map[key]

    def total_count(self) -> int:
        value = 0
        for k in self.card_map:
            value += self.card_map[k]
        return value


class CardMatrix:
    def __init__(self, hand_index: int=None):
        # TODO: Turn this into a hash table for faster recall.
        self.stats: List[CardStat] = []
        self.hand_index: int = hand_index

    def add(self, stat: CardStat):
        self.stats.append(stat)

    @property
    def rating_play(self):
        score = 0
        for stat in self.stats:
            score += stat.probability * stat.rating_play
        return score

    @property
    def rating_discard(self):
        score = 0
        for stat in self.stats:
            score += stat.probability * stat.rating_discard
        return score

    def __repr__(self):
        desc = ""
        for stat in self.stats:
            desc += f"[{stat.color} {stat.number}]: {(100 * stat.probability):.0f}% P: {stat.rating_play} D: {stat.rating_discard}\n"

        desc += "\n"
        desc += f"Play Rating: {self.rating_play:.2f}\n"
        desc += f"Discard Rating: {self.rating_discard:.2f}\n"
        return desc
