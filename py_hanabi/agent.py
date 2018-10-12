# -*- coding: utf-8 -*-

"""
An agent to play the Hanabi game.
"""

from typing import List
from logic.command import Command
from logic.command_discard import CommandDiscard
from logic.command_draw import CommandDraw
from logic.command_play import CommandPlay
from py_hanabi import analyzer
from py_hanabi.analyzer import generate_observed_matrix
from py_hanabi.card import Card
from py_hanabi.card_matrix import CardMatrix
from py_hanabi.state import State

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class Agent:
    def __init__(self, player_index: int):
        self.name: str = "Agent"
        self.player_index: int = player_index

        self.normal_play_limit = 0.80
        self.safe_play_limit = 1.00
        self.discard_limit = 0.80

    def hand(self, state: State) -> List[Card]:
        return state.get_player_hand(self.player_index)

    def play_command(self, state: State) -> List[Command]:

        state.set_dirty()

        hand: List[Card] = state.get_player_hand(self.player_index)
        draw_command = CommandDraw(self.player_index)
        matrices: List[CardMatrix] = []
        commands = []

        observed_matrix = generate_observed_matrix(state, self.player_index)

        for i, card in enumerate(hand):
            matrix = analyzer.get_card_matrix(state, self.player_index, card.observed_color, card.observed_number,
                                              card.not_color, card.not_number, observed_matrix=observed_matrix)
            matrix.hand_index = i
            matrices.append(matrix)

        play_matrix = sorted(matrices, key=lambda x: x.rating_play, reverse=True)
        discard_matrix = sorted(matrices, key=lambda x: x.rating_discard, reverse=True)

        card_play = play_matrix[0]
        play_limit = self.safe_play_limit if state.fuse_tokens == 1 else self.normal_play_limit

        if card_play.rating_play >= play_limit:
            card = hand[card_play.hand_index]
            play_command = CommandPlay(self.player_index, card_play.hand_index, state.is_card_playable(card))
            commands.append(play_command)
            if state.number_of_cards_in_deck > 0:
                commands.append(draw_command)
            return commands

        card_discard = discard_matrix[0]
        discard_command = CommandDiscard(self.player_index, card_discard.hand_index, not state.hint_token_capped)

        if card_discard.rating_discard >= self.discard_limit:
            # Discard
            commands.append(discard_command)
            if state.number_of_cards_in_deck > 0:
                commands.append(draw_command)
            return commands

        if state.hint_tokens > 0:
            hints = analyzer.get_valid_hint_commands(state, self.player_index)
            hints = sorted(hints, key=lambda x: (x.rating, x.distance), reverse=True)
            return [hints[0]]

        # Discard Anyway
        # discard_command = CommandDiscard(self.player_index, card_discard.hand_index, not state.hint_token_capped)
        commands.append(discard_command)
        if state.number_of_cards_in_deck > 0:
            commands.append(draw_command)
        return commands

