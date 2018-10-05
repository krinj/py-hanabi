# -*- coding: utf-8 -*-

"""
<ENTER DESCRIPTION HERE>
"""
from logic.command import Command
from py_hanabi.state import State

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class CommandAddTokens(Command):
    def __init__(self):
        super().__init__()
        self.name = "Add Tokens"

    def forward(self, state: State):
        state.fuse_tokens += 1
        state.discard_pile.append(state.deck[0])
        state.deck.pop(0)

    def back(self, state: State):
        state.fuse_tokens -= 1
        c = state.discard_pile.pop()
        state.deck.insert(0, c)

