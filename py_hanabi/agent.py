# -*- coding: utf-8 -*-

"""
An agent to play the Hanabi game.
"""
import random

from py_hanabi.action import Action, ActionDiscard, ActionPlay
from py_hanabi.state import State

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class Agent:
    def __init__(self, player_index: int):
        self.player_index: int = player_index
        pass

    def play(self, state: State) -> Action:
        if random.random() > 0.5:
            return ActionDiscard(self.player_index, 0)
        else:
            return ActionPlay(self.player_index, 0)
