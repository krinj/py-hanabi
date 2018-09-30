# -*- coding: utf-8 -*-

"""
A card (duh).
"""
import uuid
from enum import Enum

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

    def __repr__(self):
        return f"[{self.color} {self.number}]"

    @property
    def id(self) -> str:
        return self._id

    @property
    def number(self) -> int:
        return self._number

    @property
    def color(self) -> Color:
        return self._color
