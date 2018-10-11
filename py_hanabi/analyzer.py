# -*- coding: utf-8 -*-

"""
<ENTER DESCRIPTION HERE>
"""

from typing import List, Dict
from logic.command_hint import CommandHint
from py_hanabi.action import ActionHint
from py_hanabi.card import Color, Card
from py_hanabi.card_matrix import CardMatrix, CardStat, CardCounter
from py_hanabi.state import State
from py_hanabi.timer import Timer

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"

T_CARD_MATRIX_TIMER = "get_card_matrix"
T_HINT_RATING = "get_hint_rating"
T_VALID_HINTS = "valid_hints"
T_MARKER_1 = "marker_1"
T_MARKER_2 = "marker_2"


def get_card_matrix(state: State, player_index: int, known_color: Color=None, known_number: int=None,
                    not_color: List[Color] = None, not_number: List[int] = None,
                    observed_matrix: Dict[tuple, int] = None) -> CardMatrix:
    """ Get a card matrix with all the possible cards this card could be. """

    Timer.start(T_CARD_MATRIX_TIMER)
    card_matrix: CardMatrix = CardMatrix()

    for c in Color:
        for n in range(1, 6):
            stat = CardStat()
            stat.color = c
            stat.number = n
            stat.probability = get_card_probability(state, player_index, c, n, known_color, known_number,
                                                    not_color, not_number, observed_matrix)

            stat.rating_play = get_rating_play(state, c, n)
            Timer.start(T_MARKER_1)
            stat.rating_discard = get_rating_discard(state, c, n)
            Timer.stop(T_MARKER_1)

            card_matrix.add(stat)

    Timer.stop(T_CARD_MATRIX_TIMER)
    return card_matrix


def generate_observed_matrix(state: State, player_index: int, offhand_index: int = None):

    # Eliminate cards based on what we see.
    counter: CardCounter = CardCounter.deck()
    for card in state.discard_pile:
        counter.add(card.color, card.number, -1)

    for card in state.fireworks:
        counter.add(card.color, card.number, -1)

    for i in range(state.number_of_players):
        if i != player_index and i != offhand_index:
            for card in state.hands[i]:
                counter.add(card.color, card.number, -1)
    return counter.card_map.copy()


def get_card_probability(
        state: State, player_index: int, c: Color, n: int,
        known_color: Color=None, known_number: int=None,
        not_color: List[Color]=None, not_number: List[int]=None,
        observed_matrix: Dict[tuple, int]=None) -> float:

    # Find all cards in the deck.
    counter = CardCounter()

    if observed_matrix is None:
        counter.card_map = generate_observed_matrix(state, player_index)
    else:
        counter.card_map = observed_matrix.copy()

    # Eliminate cards we know it cannot be.

    Timer.start(T_MARKER_2)
    for c_i, n_i in [(c_i, n_i) for c_i in Color for n_i in range(1, 6)]:
        if (known_color is not None and known_color != c_i) or (known_number is not None and known_number != n_i):
            counter.set(c_i, n_i, 0)

        if (not_color is not None and c_i in not_color) or (not_number is not None and n_i in not_number):
            counter.set(c_i, n_i, 0)

    # Find the count of number of cards.
    card_count = counter.count(c, n)
    total_count = counter.total_count()
    if total_count == 0:
        return 0

    probability = card_count/total_count
    Timer.stop(T_MARKER_2)
    return probability


def get_rating_play(
        state: State, c: Color, n: int) -> float:
    """ Get a rating for this card to be played. """
    if state.is_card_playable(Card(n, c)):
        return 1.0
    return 0.0


def get_rating_discard(state: State, c: Color, n: int) -> float:
    return state.get_discard_score(Card(n, c))


def get_valid_hint_commands(state: State, player_index: int) -> List[CommandHint]:

    Timer.start(T_VALID_HINTS)
    commands = []

    for i in range(len(state.hands)):
        if i != player_index:

            map_colors = {}
            map_numbers = {}

            hand = state.get_player_hand(i)
            for card in hand:
                if not card.hint_received_color:
                    map_colors[card.color] = True
                if not card.hint_received_number:
                    map_numbers[card.number] = True

            for c in map_colors:
                command = CommandHint(player_index, i, None, c)
                commands.append(command)

            for n in map_numbers:
                command = CommandHint(player_index, i, n, None)
                commands.append(command)

    for command in commands:
        command.rating = get_hint_rating(state, command)

    Timer.stop(T_VALID_HINTS)
    return commands


def get_hint_rating(state: State, hint: ActionHint) -> float:
    Timer.start(T_HINT_RATING)
    hand = state.get_player_hand(hint.target_index)
    max_gain = -1
    best_matrix = None
    total_gain = 0

    observed_matrix = generate_observed_matrix(state, hint.target_index, hint.player_index)

    for card in hand:
        original_matrix = get_card_matrix(
            state, hint.target_index, card.observed_color, card.observed_number,
            observed_matrix=observed_matrix)
        post_matrix = original_matrix

        if hint.color is not None and hint.color == card.color:
            # print(f"Get Hint C {hint.color} - {card.color}")
            post_matrix = get_card_matrix(
                state, hint.target_index, hint.color, card.observed_number, observed_matrix=observed_matrix)

        if hint.number is not None and hint.number == card.number:
            # print(f"Get Hint R {hint.number} - {card.number}")
            post_matrix = get_card_matrix(
                state, hint.target_index, card.observed_color, hint.number, observed_matrix=observed_matrix)

        gain = post_matrix.rating_play - original_matrix.rating_play
        discard_gain = (post_matrix.rating_discard - original_matrix.rating_discard) * 0.5

        if post_matrix.rating_play > 0.99 and gain > 0:
            gain = 1

        if post_matrix.rating_discard > 0.99 and discard_gain > 0:
            discard_gain = 0.5

        gain = min(1, gain)
        discard_gain = min(0.5, discard_gain)

        total_gain += gain + discard_gain

        if gain > max_gain:
            max_gain = gain
            best_matrix = post_matrix

    Timer.stop(T_HINT_RATING)
    return total_gain


def write_timers():
    Timer.end(T_CARD_MATRIX_TIMER)
    Timer.end(T_HINT_RATING)
    Timer.end(T_VALID_HINTS)
    Timer.end(T_MARKER_1)
    Timer.end(T_MARKER_2)

