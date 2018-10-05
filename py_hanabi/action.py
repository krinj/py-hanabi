# -*- coding: utf-8 -*-

"""
<ENTER DESCRIPTION HERE>
"""

from abc import abstractmethod
from typing import List

from py_hanabi.card import Card, Color
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
        return state

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
        c = state.hands[self.player_index].pop(self.card_index)
        state.discard_pile.append(c)

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
    def __init__(self, player_index: int, target_index: int, number: int=None, color: Color=None):
        super().__init__(player_index)
        self.target_index: int = target_index
        self.number = number
        self.color = color
        self.rating: float = 0.0
        self.distance: int = 0

        i = player_index
        while i != target_index:
            i += 1
            self.distance += 1
            if i > 3:
                i = 0

        self.distance *= -1

    def __repr__(self):
        hint_subject = self.color if self.color is not None else self.number
        return f"Hint Action: To Player {self.target_index} " \
               f"Subject: {hint_subject} Rating: {self.rating} Dist: {self.distance}"

    def execute(self, state: State) -> State:
        state.hint_tokens -= 1

        hand = state.get_player_hand(self.target_index)

        if self.number is not None:
            for card in hand:
                card.receive_hint_number(self.number)
                # if card.number == self.number:
                #     card.receive_hint_number()
                # else:
                #     card.not_number.append(self.number)
        else:
            for card in hand:
                card.receive_hint_color(self.color)
                # if card.color == self.color:
                #     card.receive_hint_color()
                # else:
                #     card.not_color.append(self.color)

        return state
