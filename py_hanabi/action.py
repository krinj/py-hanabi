# -*- coding: utf-8 -*-

"""
<ENTER DESCRIPTION HERE>
"""

from abc import abstractmethod
from typing import List

from py_hanabi.card import Card
from py_hanabi.settings import N_HINT_TOKENS_MAX
from py_hanabi.state import State

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class Action:
    def __init__(self):
        self.player_index: int = 0
        pass

    @abstractmethod
    def execute(self, state: State) -> State:
        pass

    def hand(self, state: State) -> List[Card]:
        return state.hands[self.player_index]


class ActionDiscard(Action):
    def __init__(self):
        super().__init__()
        self.card_index: int = 0

    def execute(self, state: State) -> State:
        # Remove this card.
        state.hands[self.player_index].pop(self.card_index)

        # Recover a hint token if possible.
        if state.hint_tokens < N_HINT_TOKENS_MAX:
            state.hint_tokens += 1

        return state


class ActionPlay(Action):
    def __init__(self):
        super().__init__()

    def execute(self, state: State) -> State:
        pass


class ActionHint(Action):
    def __init__(self):
        super().__init__()

    def execute(self, state: State) -> State:
        pass