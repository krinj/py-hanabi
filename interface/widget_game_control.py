# -*- coding: utf-8 -*-

"""
<ENTER DESCRIPTION HERE>
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

    def setup(self, layout: QBoxLayout):
        self.layout = layout
        self.label: QLabel = QLabel("Game Control")
        self.play_button: QPushButton = QPushButton("Play")
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.play_button)
        self.update()

    def update(self):
        pass