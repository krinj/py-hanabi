# -*- coding: utf-8 -*-

"""
Control options for the game.
"""

from PyQt5.QtWidgets import QBoxLayout, QPushButton, QLabel

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class WidgetGameControl:
    def __init__(self):
        self.label: QLabel = None
        self.play_button: QPushButton = None
        self.layout: QBoxLayout = None
        pass

    def setup(self, layout: QBoxLayout, on_press_play):
        self.layout = layout
        self.label: QLabel = QLabel("Game Control")
        self.play_button: QPushButton = QPushButton("Play")
        self.play_button.clicked.connect(on_press_play)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.play_button)
        self.update()

    def update(self):
        pass