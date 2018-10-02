#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
<ENTER DESCRIPTION HERE>
"""
import time

from py_hanabi.agent import Agent
from py_hanabi.hanabi import Hanabi

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"
__version__ = "0.0.0"

if __name__ == "__main__":
    print("Running Hanabi Simulator")
    n = 1

    t_start = time.time()

    total_score = 0
    for i in range(n):
        hanabi = Hanabi()
        agents = [Agent(0), Agent(1), Agent(2), Agent(3)]
        score = hanabi.simulate_game(agents)
        total_score += score
        # if score != 25:
        #     break

    duration = time.time() - t_start

    print("Average Time Per Round: {:.4f}s".format(duration/n))
    print(f"Average Score Over {n} Rounds: {total_score/n}")

