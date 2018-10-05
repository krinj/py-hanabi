# -*- coding: utf-8 -*-

"""
<ENTER DESCRIPTION HERE>
"""
from typing import List

from PyQt5 import QtCore
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QGroupBox, \
    QVBoxLayout, QListWidget, QListWidgetItem, QBoxLayout, QLabel

from interface.widget_board_info import WidgetBoardInfo
from interface.widget_game_control import WidgetGameControl
from interface.widget_hand import WidgetHand
from interface.widget_history import WidgetHistory
from interface.window import Window
from logic.game_controller import GameController
from py_hanabi.state import State

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class WindowGame(Window):

    def __init__(self):
        super().__init__()

        self.game_controller: GameController = GameController()
        self.widget_history: WidgetHistory = WidgetHistory()
        self.widget_game_control: WidgetGameControl = WidgetGameControl()
        self.widget_board_info: WidgetBoardInfo = WidgetBoardInfo()
        self.action_label: QLabel = None
        self.hands: List[WidgetHand] = []

    def render(self, parent: QMainWindow):
        super().render(parent)
        parent.setMinimumWidth(1136)
        parent.setMinimumHeight(720)
        self.show_window(parent)

        main_layout = QHBoxLayout()
        main_widget = QWidget()
        main_widget.setLayout(main_layout)

        control_panel_widget, control_panel_layout = self.create_layout_group("Game Controls", width=240)
        self.widget_game_control.setup(control_panel_layout)
        self.widget_history.setup(control_panel_layout, self.set_history_index)
        main_layout.addWidget(control_panel_widget)

        state_widget, state_layout = self.create_layout_group("Board State")
        self.action_label = QLabel("...")
        self.action_label.setFixedHeight(32)
        self.action_label.setAlignment(QtCore.Qt.AlignCenter)
        state_layout.addWidget(self.action_label)
        for i in range(4):
            hand = WidgetHand(i)
            hand.setup(state_layout)
            self.hands.append(hand)

        main_layout.addWidget(state_widget)

        info_widget, info_layout = self.create_layout_group("Board Info", width=240)
        self.widget_board_info.setup(info_layout)
        main_layout.addWidget(info_widget)

        self.add_widget(main_widget)
        self.show_window(parent)
        self.render_state(self.game_controller.state)
        self.update()

    def render_state(self, state: State):
        self.widget_board_info.render_state(state)
        for h in self.hands:
            h.render_state(state)

    def on_resize(self, event: QResizeEvent):
        for h in self.hands:
            h.resize()

    def update(self):
        self.widget_history.update(self.game_controller.history)

    def set_history_index(self, index: int):
        self.game_controller.set_command_index(index)
        self.action_label.setText(self.game_controller.history[index].long_description)
        self.render_state(self.game_controller.state)

    @staticmethod
    def create_layout_group(name: str, width: int = None, horizontal: bool = False) -> (QWidget, QBoxLayout):
        group_box = QGroupBox(name)

        if width is not None:
            group_box.setFixedWidth(width)

        layout = QHBoxLayout() if horizontal else QVBoxLayout()
        group_box.setLayout(layout)
        return group_box, layout

