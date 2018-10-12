# -*- coding: utf-8 -*-

"""
Collect the results for a given hint command.
"""

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class HintStat:
    def __init__(self):
        self.enables_play: int = 0
        self.enables_discard: int = 0
        self.total_play_gain: float = 0
        self.total_discard_gain: float = 0
        self.max_play_gain: float = 0
        self.max_discard_gain: float = 0
        self.vital_reveal: int = 0

        # If this hint points to a card that can immediately be played.
        self.n_cards_affected: int = 0
        self.true_playable_cards: int = 0
