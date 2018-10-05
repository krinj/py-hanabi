# -*- coding: utf-8 -*-

"""
<ENTER DESCRIPTION HERE>
"""

from logic.command import Command
from py_hanabi.card import Card
from py_hanabi.state import State

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class CommandPlay(Command):
    def __init__(self, player_index: int, card_index: int, is_playable: bool):
        super().__init__()
        self.player_index: int = player_index
        self.card_index: int = card_index
        self.is_playable: bool = is_playable
        self.name: str = "Play Card"

    def forward(self, state: State):
        card = state.hands[self.player_index].pop(self.card_index)

        if self.is_playable:
            state.fireworks.append(card)
            self.long_description = f"Player {self.player_index} Successfully Plays {card.label}."
        else:
            state.discard_pile.append(card)
            state.fuse_tokens -= 1
            self.long_description = f"Player {self.player_index} Wrongly Plays {card.label}."

    def back(self, state: State):
        if self.is_playable:
            card = state.fireworks.pop()
        else:
            card = state.discard_pile.pop()
            state.fuse_tokens += 1

        state.hands[self.player_index].insert(self.card_index, card)
