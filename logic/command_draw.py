# -*- coding: utf-8 -*-

"""
<ENTER DESCRIPTION HERE>
"""

from logic.command import Command
from py_hanabi.state import State

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class CommandDraw(Command):
    def __init__(self, player_index: int):
        super().__init__()
        self.player_index: int = player_index
        self.name: str = f"Player {self.player_index} Draws Card"

    def forward(self, state: State):
        card = state.deck.pop()
        state.hands[self.player_index].append(card)

    def back(self, state: State):
        card = state.hands[self.player_index].pop()
        state.deck.append(card)
