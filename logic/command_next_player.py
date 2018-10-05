# -*- coding: utf-8 -*-

"""
<ENTER DESCRIPTION HERE>
"""
from logic.command import Command
from py_hanabi.state import State

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class CommandNextPlayer(Command):
    def __init__(self):
        super().__init__()
        self.name: str = "Next Player"

    def forward(self, state: State):
        state.player_index += 1
        if state.player_index >= state.number_of_players:
            state.player_index = 0

    def back(self, state: State):
        state.player_index -= 1
        if state.player_index < 0:
            state.player_index = state.number_of_players - 1
