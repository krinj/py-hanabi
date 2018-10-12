# -*- coding: utf-8 -*-

"""
Draw a card for the player.
"""

from py_hanabi.commands.command import Command
from py_hanabi.state import State

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class CommandDraw(Command):
    def __init__(self, player_index: int):
        super().__init__()
        self.player_index: int = player_index
        self.name: str = f"Player {self.player_index + 1} Draws Card"

    def forward(self, state: State):
        card = state.deck.pop()
        state.hands[self.player_index].append(card)
        self.long_description = f"Player {self.player_index + 1} Draws {card.label}."

    def back(self, state: State):
        card = state.hands[self.player_index].pop()
        state.deck.append(card)
