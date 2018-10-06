# -*- coding: utf-8 -*-

"""
<ENTER DESCRIPTION HERE>
"""

from logic.command import Command
from py_hanabi.settings import N_HINT_TOKENS_MAX
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
        state.discard_pile.append(card)

        if self.should_add_hint:
            state.hint_tokens += 1

        self.long_description = f"Player {self.player_index + 1} Discards {card.label}."

    def back(self, state: State):
        card = state.discard_pile.pop()
        state.hands[self.player_index].insert(self.card_index, card)

        if self.should_add_hint:
            state.hint_tokens -= 1

