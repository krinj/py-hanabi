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
    def __init__(self, player_index: int):
        self.player_index: int = player_index

    @abstractmethod
    def execute(self, state: State) -> State:
        print("EXECUTE ACTION BASE")
        pass

    def hand(self, state: State) -> List[Card]:
        return state.hands[self.player_index]


class ActionDiscard(Action):
    def __init__(self, player_index: int, card_index: int):
        super().__init__(player_index)
        self.card_index: int = card_index

    def __repr__(self):
        return "Discard Action"

    def execute(self, state: State) -> State:
        # Remove this card.
        print("EXECUTE ACTION DISCARD")
        state.hands[self.player_index].pop(self.card_index)

        # Recover a hint token if possible.
        if state.hint_tokens < N_HINT_TOKENS_MAX:
            state.hint_tokens += 1

        state.draw_card(self.player_index, 1)
        return state


class ActionPlay(Action):
    def __init__(self, player_index: int, card_index: int):
        super().__init__(player_index)
        self.card_index: int = card_index

    def __repr__(self):
        return f"Play Action: {self.card_index}"

    def execute(self, state: State) -> State:
        print("EXECUTE ACTION PLAY")
        # Remove this card.
        card = state.hands[self.player_index].pop(self.card_index)
        state.play_card(card)
        state.draw_card(self.player_index, 1)
        return state


class ActionHint(Action):
    def __init__(self, player_index: int):
        super().__init__(player_index)

    def __repr__(self):
        return f"Hint Action"

    def execute(self, state: State) -> State:
        state.hint_tokens -= 1
        return state
