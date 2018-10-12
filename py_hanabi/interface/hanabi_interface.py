# -*- coding: utf-8 -*-

"""
Initialize the Hanabi PyQT5 Interface.
"""

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication

from py_hanabi.interface.hanabi_window import HanabiWindow
from py_hanabi.interface.window import Window

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class HanabiInterface(QMainWindow):

    def __init__(self):

        app = QApplication([])
        app.setStyle('Fusion')

        palette = QPalette()
        palette.setColor(QPalette.Window, QtGui.QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QtCore.Qt.white)
        palette.setColor(QPalette.Base, QtGui.QColor(15, 15, 15))
        palette.setColor(QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, QtCore.Qt.white)
        palette.setColor(QPalette.ToolTipText, QtCore.Qt.white)
        palette.setColor(QPalette.Text, QtCore.Qt.white)
        palette.setColor(QPalette.Button, QtGui.QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QtCore.Qt.white)
        palette.setColor(QPalette.BrightText, QtCore.Qt.red)
        palette.setColor(QPalette.Highlight, QtGui.QColor(0, 110, 200))
        palette.setColor(QPalette.HighlightedText, QtGui.QColor(255, 255, 255))
        app.setPalette(palette)

        super().__init__()
        self.setWindowTitle("Hanabi Visualizer")
        self.current_window: Window = None
        self.window_game: HanabiWindow = HanabiWindow()
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
