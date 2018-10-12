# -*- coding: utf-8 -*-

"""
Display a single card UI.
"""

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent, QColor
from PyQt5.QtWidgets import QLabel, QDialog, QTableWidget, QDesktopWidget, QTableWidgetItem, \
    QVBoxLayout

from py_hanabi import analyzer
from py_hanabi.card import Color, Card
from py_hanabi.card_matrix import CardMatrix
from py_hanabi.state import State

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class WidgetCard(QLabel):

    def __init__(self, player_index: int = 0):
        super().__init__()

        self.setAutoFillBackground(True)
        self.setAlignment(QtCore.Qt.AlignCenter)

        font = QtGui.QFont("", 24)
        self.setFont(font)

        # Need to store these references for matrix construction.
        self.state: State = None
        self.player_index: int = player_index
        self.card: Card = None
        self.matrix: CardMatrix = None

    def update(self, state: State, card: Card):

        # Set the reference states and clear the matrix.
        self.state = state
        self.card = card
        self.matrix = None

        if state.player_index == self.player_index:
            display_num = str(card.observed_number) if card.observed_number is not None else ""
            self.setText(display_num)
            self.render_color(card.observed_color)
        else:
            self.setText(str(card.number))
            self.render_color(card.color)

    def resize(self):
        self.setFixedWidth(int(self.height() * 0.75))

    def render_color(self, color: Color):
        self.setStyleSheet(f"background-color: {self.get_color_hex_background(color)}; "
                           "border-style: solid; "
                           "border-width: 2px; "
                           f"border-color: #000000; "
                           f"color: #000000;"
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

    # ===================================================================================================
    # Matrix Popup.
    # ===================================================================================================

    def mouseReleaseEvent(self, event: QMouseEvent):
        """ Display the card probability matrix as a pop-up, as known to this player. """
        if self.matrix is None:
            c = self.card
            self.matrix = analyzer.get_card_matrix(
                self.state, self.player_index, c.observed_color, c.observed_number, c.not_color, c.not_number)

        d = QDialog()
        layout = QVBoxLayout()
        d.setLayout(layout)

        t_size_x = 540
        t_size_y = 180

        table = QTableWidget()

        table.setRowCount(5)
        table.setColumnCount(5)

        table.setHorizontalHeaderLabels([c.name for c in Color])
        table.setVerticalHeaderLabels([str(i + 1) for i in range(0, 5)])

        for color in Color:
            for j in range(0, 5):

                i = color.value - 1
                number = j + 1

                stat = self.matrix.stats[(color, number)]
                item = QTableWidgetItem(f"{(100 * stat.probability):.0f}%")

                if stat.probability == 0:
                    item.setForeground(QColor(50, 50, 50))
                elif stat.rating_play > 0.5:
                    item.setForeground(QColor(0, 255, 0))
                elif stat.rating_discard > 0.8:
                    item.setForeground(QColor(255, 0, 0))

                table.setItem(j, i, item)

        table.resize(t_size_x, t_size_y)
        layout.addWidget(table)

        label = QLabel()
        label.setText(f"Play Rating: {self.matrix.rating_play:.2f}\n "
                      f"Discard Rating: {self.matrix.rating_discard:.2f}")
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)
        layout.setContentsMargins(20, 20, 20, 20)

        # Resize the dialog and center it.
        d.setMinimumWidth(t_size_x + 20)
        qt_rectangle = d.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        d.move(qt_rectangle.topLeft())

        # Display the dialog.
        d.setWindowTitle("Card Value Matrix")
        d.setWindowModality(Qt.ApplicationModal)
        d.exec()

