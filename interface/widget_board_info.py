# -*- coding: utf-8 -*-

"""
<ENTER DESCRIPTION HERE>
"""
from PyQt5.QtWidgets import QLabel, QBoxLayout, QListWidget, QListWidgetItem, QSpacerItem

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class WidgetBoardInfo:
    def __init__(self):
        self.n_deck_label: QLabel = None
        self.n_fuse_label: QLabel = None
        self.n_hint_label: QLabel = None
        self.list_widget: QListWidget = None
        self.layout: QBoxLayout = None

    def setup(self, layout: QBoxLayout):

        self.layout = layout
        self.n_deck_label = QLabel(f"Deck: {0}")
        self.n_fuse_label = QLabel(f"Fuse Tokens: {3}")
        self.n_hint_label = QLabel(f"Hint Tokens: {8}")
        label = QLabel("Discard Pile")
        self.list_widget = QListWidget()
        self.layout.addWidget(self.n_deck_label)
        self.layout.addWidget(self.n_fuse_label)
        self.layout.addWidget(self.n_hint_label)
        self.layout.addItem(QSpacerItem(0, 20))
        self.layout.addWidget(label)
        self.layout.addWidget(self.list_widget)
        self.update()

    def update(self):
        self.list_widget.clear()
        for i in range(100):
            item = QListWidgetItem(self.list_widget)
            item.setText(f"Item {i}")
