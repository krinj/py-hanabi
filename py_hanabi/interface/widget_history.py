# -*- coding: utf-8 -*-

"""
Display a scrollable history list of commands.
"""

from typing import List, Callable
from PyQt5.QtWidgets import QBoxLayout, QListWidget, QListWidgetItem, QLabel
from py_hanabi.commands.command import Command

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class CommandListItem(QListWidgetItem):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.command: Command = None
        self.index: int = 0


class WidgetHistory:
    def __init__(self):
        self.list_widget: QListWidget = None
        self.layout: QBoxLayout = None
        self.list_widget: QListWidget = None
        self.action_set_command_index: Callable[[int], None] = None
        pass

    def setup(self, layout: QBoxLayout, action_set_command_index: Callable[[int], None]):
        self.action_set_command_index = action_set_command_index
        self.layout = layout
        self.list_widget = QListWidget()
        label = QLabel("History")
        self.layout.addWidget(label)
        self.layout.addWidget(self.list_widget)
        self.list_widget.currentItemChanged.connect(self.on_item_changed)

    def on_item_changed(self, item):
        if item is not None:
            self.action_set_command_index(item.index)
        else:
            self.action_set_command_index(None)

    def update(self, history: List[Command]):
        self.list_widget.clear()

        for i, command in enumerate(history):
            item = CommandListItem(self.list_widget)
            item.command = command
            item.index = i
            command_number = str(i + 1).zfill(3)
            item.setText(f"{command_number}:  {command.name}")

