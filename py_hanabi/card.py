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

        self._hint_number_counter: int = 0
        self._hint_color_counter: int = 0

        # self._index_hinted: List[int] = []
        # self._lone_hinted: List[bool] = []

        # According to hints, these are the ones we know it is NOT.
        self.not_color: List[Color] = []
        self.not_number: List[int] = []

    def __repr__(self):
        hint_str = ""
        if self.hint_received_color:
            hint_str += "C"
        if self.hint_received_number:
            hint_str += "N"

        return f"[{self.color} {self.number} {hint_str}]"

    def __eq__(self, other: 'Card'):
        return self.color == other.color and self.number == other.number

    def receive_hint_number(self, number: int):
        if number == self.number:
            self._hint_number_counter += 1
        else:
            self.not_number.append(number)

    def receive_hint_color(self, color: Color):
        if color == self.color:
            self._hint_color_counter += 1
        else:
            self.not_color.append(color)

    def remove_hint_number(self, number: int):
        if number == self.number:
            self._hint_number_counter -= 1
        else:
            self.not_number.pop()

    def remove_hint_color(self, color: Color):
        if color == self.color:
            self._hint_color_counter -= 1
        else:
            self.not_color.pop()

    @property
    def label(self):
        return f"{self.number} of {self.get_color_label(self.color)}"

    @property
    def id(self) -> str:
        return self._id

    @property
    def key(self) -> tuple:
        return self.get_key(self.color, self.number)

    @staticmethod
    def get_key(c: Color, n: int) -> tuple:
        return c, n

    @property
    def number(self) -> int:
        return self._number

    @property
    def color(self) -> Color:
        return self._color

    @property
    def observed_color(self) -> Color:
        return None if not self.hint_received_color else self._color

    @property
    def observed_number(self) -> int:
        return None if not self.hint_received_number else self._number

    @property
    def hint_received_number(self) -> bool:
        return self._hint_number_counter > 0

    @property
    def hint_received_color(self) -> bool:
        return self._hint_color_counter > 0

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

    @staticmethod
    def get_color_label(color: Color) -> str:
        color_labels = {
            Color.BLUE: "Blue",
            Color.RED: "Red",
            Color.YELLOW: "Yellow",
            Color.GREEN: "Green",
            Color.WHITE: "White",
        }
        return color_labels[color]

