# -*- coding: utf-8 -*-

"""
<ENTER DESCRIPTION HERE>
"""
from abc import abstractmethod

from py_hanabi.state import State

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class Command:
    def __init__(self):
        self.name: str = "Initialize Board"

    @abstractmethod
    def forward(self, state: State):
        pass

    @abstractmethod
    def back(self, state: State):
        pass
