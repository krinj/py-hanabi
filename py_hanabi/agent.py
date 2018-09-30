# -*- coding: utf-8 -*-

"""
An agent to play the Hanabi game.
"""

from py_hanabi.action import Action, ActionDiscard
from py_hanabi.state import State

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class Agent:
    def __init__(self, player_index: int):
        self.player_index: int = player_index
        pass

    def play(self, state: State) -> Action:
        return ActionDiscard(self.player_index, 0)
        pass
