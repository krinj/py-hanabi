# -*- coding: utf-8 -*-

"""
A card (duh).
"""
import random
import uuid
from enum import Enum
from typing import List

from py_hanabi.settings import CARD_DECK_DISTRIBUTION

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class Color(Enum):
    RED = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4
    WHITE = 5


class Card:
    def __init__(self, number: int, color: Color):
        self._number: int = number
        self._color: Color = color
        self._id: str = uuid.uuid4().hex
        self._hint_received_number: bool = False
        self._hint_received_color: bool = False

    def __repr__(self):
        hint_str = ""
        if self.hint_received_color:
            hint_str += "C"
        if self.hint_received_number:
            hint_str += "N"

        return f"[{self.color} {self.number} {hint_str}]"

    def __eq__(self, other: 'Card'):
        return self.color == other.color and self.number == other.number

    def receive_hint_number(self):
        self._hint_received_number = True

    def receive_hint_color(self):
        self._hint_received_color = True

    @property
    def id(self) -> str:
        return self._id

    @property
    def key(self) -> str:
        return self.get_key(self.color, self.number)

    @staticmethod
    def get_key(c: Color, n: int) -> str:
        return f"{c}_{n}"

    @property
    def number(self) -> int:
        return self._number

    @property
    def color(self) -> Color:
        return self._color

    @property
    def observed_color(self) -> Color:
        return None if not self._hint_received_color else self._color

    @property
    def observed_number(self) -> int:
        return None if not self._hint_received_number else self._number

    @property
    def hint_received_number(self) -> bool:
        return self._hint_received_number

    @property
    def hint_received_color(self) -> bool:
        return self._hint_received_color

    @staticmethod
    def generate_deck() -> List['Card']:
        """ Generate the starting deck for the game. """
        deck: List[Card] = []
        for color in Color:
            for i in CARD_DECK_DISTRIBUTION:
                card = Card(i, color)
                deck.append(card)

        random.shuffle(deck)
        return deck
