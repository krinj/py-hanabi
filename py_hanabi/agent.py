# -*- coding: utf-8 -*-

"""
An agent to play the Hanabi game.
"""
import random
from typing import List

from py_hanabi import analyzer
from py_hanabi.action import Action, ActionDiscard, ActionPlay, ActionHint
from py_hanabi.card import Card
from py_hanabi.card_matrix import CardMatrix
from py_hanabi.state import State

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class Agent:
    def __init__(self, player_index: int):
        self.name: str = "Agent"
        self.player_index: int = player_index
        pass

    def play(self, state: State) -> Action:

        hand: List[Card] = state.get_player_hand(self.player_index)

        matrices: List[CardMatrix] = []
        for i, card in enumerate(hand):
            matrix = analyzer.get_card_matrix(state, self.player_index, card.observed_color, card.observed_number,
                                              card.not_color, card.not_number)
            matrix.hand_index = i
            matrices.append(matrix)

        ratings = [m.rating_play for m in matrices]
        print(ratings)

        play_matrix = sorted(matrices, key=lambda x: x.rating_play, reverse=True)
        discard_matrix = sorted(matrices, key=lambda x: x.rating_discard, reverse=True)

        card_play = play_matrix[0]
        if card_play.rating_play >= 0.8:
            return ActionPlay(self.player_index, card_play.hand_index)

        card_discard = discard_matrix[0]

        if card_discard.rating_discard >= 0.9:
            return ActionDiscard(self.player_index, card_discard.hand_index)

        if state.hint_tokens > 0:
            hints = analyzer.get_valid_hint_actions(state, self.player_index)
            hints = sorted(hints, key=lambda x: (x.rating, x.distance), reverse=True)
            return hints[0]

        return ActionDiscard(self.player_index, card_discard.hand_index)

        #return ActionDiscard(self.player_index, 0)

        # for i in range(len(hand)):
        #     card = hand[i]
        #     if state.is_card_playable(card):
        #         return ActionPlay(self.player_index, i)
        #
        # best_discard_score = 0
        # best_card_index = None
        #
        # for i in range(len(hand)):
        #     card = hand[i]
        #     score = state.get_discard_score(card)
        #     if best_card_index is None or score > best_discard_score:
        #         best_discard_score = score
        #         best_card_index = i
        #
        # if state.hint_tokens > 0:
        #     return ActionHint(self.player_index)
        #
        # return ActionDiscard(self.player_index, best_card_index)

        # if random.random() > 0.2:
        #     return ActionDiscard(self.player_index, 0)
        # else:
        #     return ActionPlay(self.player_index, 0)
