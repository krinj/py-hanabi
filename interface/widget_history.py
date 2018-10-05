# -*- coding: utf-8 -*-

"""
<ENTER DESCRIPTION HERE>
"""
from PyQt5.QtWidgets import QBoxLayout, QListWidget, QListWidgetItem, QLabel

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class WidgetHistory:
    def __init__(self):
        self.list_widget: QListWidget = None
        self.layout: QBoxLayout = None
        pass

    def setup(self, layout: QBoxLayout):
        self.layout = layout
        self.update()

    def on_item_changed(self, item):
        pass

    def update(self):
        self.list_widget = QListWidget()
        label = QLabel("History")
        self.layout.addWidget(label)
        self.layout.addWidget(self.list_widget)
        self.list_widget.currentItemChanged.connect(self.on_item_changed)

        for i in range(100):
            item = QListWidgetItem(self.list_widget)
            item.setText(f"Item {i}")
            # if i > 40:
            #     item.setForeground(QColor(50, 50, 50))
