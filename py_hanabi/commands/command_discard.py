# -*- coding: utf-8 -*-

"""
Discard the target card.
"""

from py_hanabi.commands.command import Command
from py_hanabi.state import State

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class CommandDiscard(Command):
    def __init__(self, player_index: int, card_index: int, should_add_hint: bool):
        super().__init__()
        self.player_index: int = player_index
        self.card_index: int = card_index
        self.name: str = f"Player {self.player_index + 1} discards {self.card_index}"
        self.should_add_hint: bool = should_add_hint

    def forward(self, state: State):

        card = state.hands[self.player_index].pop(self.card_index)
        state.add_to_discard_pile(card)

        if self.should_add_hint:
            state.hint_tokens += 1

        self.long_description = f"Player {self.player_index + 1} Discards {card.label}."

    def back(self, state: State):
        card = state.pop_from_discard_pile()
        state.hands[self.player_index].insert(self.card_index, card)
        state.set_dirty()

        if self.should_add_hint:
            state.hint_tokens -= 1

