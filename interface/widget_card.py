# -*- coding: utf-8 -*-

"""
<ENTER DESCRIPTION HERE>
"""
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QFrame, QLabel, QDialog, QPushButton

from py_hanabi.card import Color

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class WidgetCard(QLabel):

    def __init__(self):
        super().__init__()

        self.setAutoFillBackground(True)
        self.setAlignment(QtCore.Qt.AlignCenter)

        font = QtGui.QFont("", 24)
        self.setFont(font)

    def update(self, color: Color, number: int):

        if number is not None:
            self.setText(str(number))
        else:
            self.setText("")
        self.render_color(color)

    def mouseReleaseEvent(self, event: QMouseEvent):
        print("Clicked!")
        d = QDialog()
        b1 = QPushButton("ok", d)
        b1.move(50, 50)
        d.setWindowTitle("Dialog")
        d.setWindowModality(Qt.ApplicationModal)
        d.exec()

    def resize(self):
        self.setFixedWidth(int(self.height() * 0.75))

    def render_color(self, color: Color):
        self.setStyleSheet(f"background-color: {self.get_color_hex_background(color)}; "
                           "border-style: solid; "
                           "border-width: 2px; "
                           f"border-color: {self.get_color_hex_foreground(color)}; "
                           f"color: {self.get_color_hex_foreground(color)};"
                           "border-radius: 5px;")

    @staticmethod
    def get_color_hex_background(color: Color):

        colors = {
            Color.BLUE: "#84d6ff",
            Color.YELLOW: "#fff09b",
            Color.WHITE: "#ffffff",
            Color.GREEN: "#baffaa",
            Color.RED: "#ffafaf"
        }

        if color in colors:
            return colors[color]
        else:
            return "#999999"

    @staticmethod
    def get_color_hex_foreground(color: Color):
        return "#000000"
        #
        # colors = {
        #     color.BLUE: "#0077ff",
        #     color.YELLOW: "#d67500",
        #     color.WHITE: "#a8a8a8",
        #     color.GREEN: "#0e7721",
        #     color.RED: "#9e0f00"
        # }
        #
        # if color in colors:
        #     return colors[color]
        # else:
        #     return "#515151"



