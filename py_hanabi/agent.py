# -*- coding: utf-8 -*-

"""
An agent to play the Hanabi game.
"""
import random
from typing import List

from py_hanabi.action import Action, ActionDiscard, ActionPlay, ActionHint
from py_hanabi.card import Card
from py_hanabi.state import State

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class Agent:
    def __init__(self, player_index: int):
        self.player_index: int = player_index
        pass

    def play(self, state: State) -> Action:
        hand: List[Card] = state.get_player_hand(self.player_index)

        for i in range(len(hand)):
            card = hand[i]
            if state.is_card_playable(card):
                return ActionPlay(self.player_index, i)

        best_discard_score = 0
        best_card_index = None

        for i in range(len(hand)):
            card = hand[i]
            score = state.get_discard_score(card)
            if best_card_index is None or score > best_discard_score:
                best_discard_score = score
                best_card_index = i

        if state.hint_tokens > 0:
            return ActionHint(self.player_index)

        return ActionDiscard(self.player_index, best_card_index)
        # if random.random() > 0.2:
        #     return ActionDiscard(self.player_index, 0)
        # else:
        #     return ActionPlay(self.player_index, 0)
