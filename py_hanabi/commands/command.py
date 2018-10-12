# -*- coding: utf-8 -*-

"""
A Command pattern class for all state modification actions.
"""

from abc import abstractmethod
from py_hanabi.state import State

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class Command:
    def __init__(self, name: str="Command Name", long_description: str="Description"):
        self.name: str = name
        self.long_description: str = long_description

    @abstractmethod
    def forward(self, state: State):
        pass

    @abstractmethod
    def back(self, state: State):
        pass
