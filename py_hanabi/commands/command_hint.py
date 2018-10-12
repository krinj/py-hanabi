# -*- coding: utf-8 -*-

"""
Give a hint to a player.
"""

from py_hanabi.commands.command import Command
from py_hanabi.card import Color
from py_hanabi.hint_stat import HintStat
from py_hanabi.state import State

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class CommandHint(Command):
    def __init__(self, player_index: int, target_index: int, number: int=None, color: Color=None):
        super().__init__()
        self.player_index: int = player_index
        self.target_index: int = target_index
        self.number: int = number
        self.color: Color = color
        self.hint_stat: HintStat = None
        self.distance: int = 0

        self.name: str = "Give Hint"

        i = player_index
        while i != target_index:
            i += 1
            self.distance += 1
            if i > 3:
                i = 0

        self.distance = 4 - self.distance

    def forward(self, state: State):

        state.hint_tokens -= 1
        hand = state.get_player_hand(self.target_index)

        if self.number is not None:
            for card in hand:
                card.receive_hint_number(self.number)
            self.long_description = \
                f"Player {self.player_index + 1} Gives Hint to Player {self.target_index + 1}: {self.number}"
        else:
            for card in hand:
                card.receive_hint_color(self.color)
                self.long_description = \
                    f"Player {self.player_index + 1} Gives Hint to Player {self.target_index + 1}: {self.color}"

    def back(self, state: State):

        state.hint_tokens += 1
        hand = state.get_player_hand(self.target_index)

        if self.number is not None:
            for card in hand:
                card.remove_hint_number(self.number)
        else:
            for card in hand:
                card.remove_hint_color(self.color)
