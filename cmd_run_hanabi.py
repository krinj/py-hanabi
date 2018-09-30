#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
<ENTER DESCRIPTION HERE>
"""
from py_hanabi.agent import Agent
from py_hanabi.hanabi import Hanabi

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"
__version__ = "0.0.0"

if __name__ == "__main__":
    print("Running Hanabi Simulator")
    hanabi = Hanabi()
    agents = [Agent(0), Agent(1), Agent(2), Agent(3)]
    hanabi.simulate_game(agents)
