# -*- coding: utf-8 -*-

"""
<ENTER DESCRIPTION HERE>
"""
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication

from interface.window import Window
from interface.window_game import WindowGame

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class HanabiInterface(QMainWindow):

    def __init__(self):

        app = QApplication([])
        app.setStyle('Fusion')

        super().__init__()
        self.setWindowTitle("Hanabi Visualizer")
        self.current_window: Window = None
        self.window_game: WindowGame = WindowGame()
        self.show_window(self.window_game)

        # Force a resize update.
        t = QtCore.QTimer()
        t.singleShot(0, self.resizeEvent)

        app.exec()

    def show_window(self, window: Window):
        self.current_window = window
        window.render(self)
        self.center_screen()

    def center_screen(self):
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

    def resizeEvent(self, event=None):
        self.current_window.on_resize(event)
