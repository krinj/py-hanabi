# -*- coding: utf-8 -*-

"""
Display the player's hand.
"""

from typing import List
from PyQt5 import QtCore
from PyQt5.QtWidgets import QBoxLayout, QGroupBox, QHBoxLayout, QVBoxLayout, QLabel

from py_hanabi.interface.widget_card import WidgetCard
from py_hanabi.state import State

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class WidgetHand:
    def __init__(self, index: int):
        self.player_index: int = index
        self.hand_group: QGroupBox = None
        self.hand_layout: QHBoxLayout = None

        self.player_info_layout: QVBoxLayout = None
        self.card_layout: QHBoxLayout = None
        self.label: QLabel = None

        self.layout: QBoxLayout = None
        self.cards: List[WidgetCard] = []

    def setup(self, layout: QBoxLayout):
        self.hand_group = QGroupBox()
        self.hand_layout = QHBoxLayout()
        self.card_layout = QHBoxLayout()
        self.player_info_layout = QVBoxLayout()

        self.hand_layout.addLayout(self.player_info_layout)
        self.hand_layout.addLayout(self.card_layout)
        self.hand_group.setLayout(self.hand_layout)

        self.label = QLabel(f"Player {self.player_index + 1}")
        self.player_info_layout.addWidget(self.label)
        self.card_layout.setAlignment(QtCore.Qt.AlignRight)
        self.layout = layout
        self.layout.addWidget(self.hand_group)

        for i in range(5):
            widget_card = WidgetCard(self.player_index)
            self.cards.append(widget_card)
            self.card_layout.addWidget(widget_card)

    def render_state(self, state: State):

        if state.player_index == self.player_index:
            self.label.setText(f"Player {self.player_index + 1} (Active)")
        else:
            self.label.setText(f"Player {self.player_index + 1}")

        hand = state.get_player_hand(self.player_index)

        for i in range(5):
            widget_card = self.cards[i]
            if i < len(hand):
                card = hand[i]
                self.card_layout.addWidget(widget_card)
                widget_card.update(state, card)
            else:
                widget_card.setParent(None)

        #
        # t = QtCore.QTimer()
        # t.singleShot(0, self.resize)
        # self.resize()

    def on_item_changed(self, item):
        pass

    def resize(self):
        for card in self.cards:
            card.resize()

    def update(self):
        for card in self.cards:
            card.update()