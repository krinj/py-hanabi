# -*- coding: utf-8 -*-

"""
<ENTER DESCRIPTION HERE>
"""
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QFrame, QLabel, QDialog, QPushButton

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class WidgetCard(QLabel):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)
        self.setText("5")
        self.setAlignment(QtCore.Qt.AlignCenter)

        font = QtGui.QFont("", 24)
        self.setFont(font)
        self.setStyleSheet("background-color: #ffffff; "
                           "border-style: solid; "
                           "border-width: 2px; "
                           "border-color: #ff0000; "
                           "color: #ff0000;"
                           "border-radius: 5px;")

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


