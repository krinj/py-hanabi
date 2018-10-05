# -*- coding: utf-8 -*-

"""
<ENTER DESCRIPTION HERE>
"""

from typing import List
from PyQt5 import QtCore
from PyQt5.QtWidgets import QBoxLayout, QGroupBox, QHBoxLayout, QVBoxLayout, QLabel

from interface.widget_card import WidgetCard

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class WidgetHand:
    def __init__(self):
        self.hand_group: QGroupBox = None
        self.hand_layout: QHBoxLayout = None

        self.player_info_layout: QVBoxLayout = None
        self.card_layout: QHBoxLayout = None

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

        label = QLabel("Player 1")
        self.player_info_layout.addWidget(label)

        for i in range(4):
            widget_card = WidgetCard()
            self.cards.append(widget_card)
            self.card_layout.addWidget(widget_card)

        self.card_layout.setAlignment(QtCore.Qt.AlignRight)
        self.layout = layout
        self.layout.addWidget(self.hand_group)

    def on_item_changed(self, item):
        pass

    def resize(self):
        for card in self.cards:
            card.resize()

    def update(self):
        for card in self.cards:
            card.update()