# -*- coding: utf-8 -*-

"""
Shows extra data about the game board.
"""

from typing import Dict
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel, QBoxLayout, QListWidget, QListWidgetItem, QSpacerItem, QAbstractItemView

from py_hanabi.card import Color
from py_hanabi.state import State

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class WidgetBoardInfo:
    def __init__(self):
        self.n_deck_label: QLabel = None
        self.n_fuse_label: QLabel = None
        self.n_hint_label: QLabel = None
        self.n_score_label: QLabel = None
        self.n_grace_rounds: QLabel = None

        self.discard_list: QListWidget = None
        self.firework_list: QListWidget = None
        self.layout: QBoxLayout = None

        self.color_map: Dict[Color, QColor] = {
            Color.BLUE: QColor(50, 180, 255),
            Color.WHITE: QColor(255, 255, 255),
            Color.YELLOW: QColor(255, 200, 0),
            Color.GREEN: QColor(50, 255, 0),
            Color.RED: QColor(255, 50, 50)
        }

    def setup(self, layout: QBoxLayout):

        self.layout = layout
        self.n_deck_label = QLabel(f"Deck: --")
        self.n_fuse_label = QLabel(f"Fuse Tokens: --")
        self.n_hint_label = QLabel(f"Hint Tokens: --")
        self.n_score_label = QLabel(f"Score: --")
        self.n_grace_rounds = QLabel()

        self.discard_list = QListWidget()
        self.firework_list = QListWidget()
        self.firework_list.setFixedHeight(100)
        self.firework_list.setSelectionMode(QAbstractItemView.NoSelection)

        self.layout.addWidget(self.n_deck_label)
        self.layout.addWidget(self.n_fuse_label)
        self.layout.addWidget(self.n_hint_label)
        self.layout.addWidget(self.n_score_label)
        self.layout.addWidget(self.n_grace_rounds)

        self.layout.addItem(QSpacerItem(0, 20))
        self.layout.addWidget(QLabel("Playable Cards"))
        self.layout.addWidget(self.firework_list)

        self.layout.addItem(QSpacerItem(0, 20))
        self.layout.addWidget(QLabel("Discard Pile"))
        self.layout.addWidget(self.discard_list)
        # self.update()

    def render_state(self, state: State):

        self.n_deck_label.setText(f"Deck: {state.number_of_cards_in_deck} Cards")
        self.n_fuse_label.setText(f"Fuse Tokens: {state.fuse_tokens}")
        self.n_hint_label.setText(f"Hint Tokens: {state.hint_tokens}")
        self.n_score_label.setText(f"Score: {len(state.fireworks)}")
        self.n_grace_rounds.setText(f"Grace Rounds: {max(0, state.grace_rounds - 1)}")

        self.discard_list.clear()
        for card in state.discard_pile:
            item = QListWidgetItem(self.discard_list)
            item.setText(card.label)
            if state.get_discard_score(card) == 1:
                item.setForeground(QColor(50, 50, 50))
            else:
                item.setForeground(self.color_map[card.color])

        self.firework_list.clear()
        for card in state.playable_cards:
            item = QListWidgetItem(self.firework_list)
            item.setText(card.label)
            item.setForeground(self.color_map[card.color])
