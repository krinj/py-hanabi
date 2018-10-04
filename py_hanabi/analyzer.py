# -*- coding: utf-8 -*-

"""
<ENTER DESCRIPTION HERE>
"""

from typing import List

from py_hanabi.action import ActionHint
from py_hanabi.card import Color, Card
from py_hanabi.card_matrix import CardMatrix, CardStat, CardCounter
from py_hanabi.state import State

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


def get_card_matrix(state: State, player_index: int, known_color: Color=None, known_number: int=None,
                    not_color: List[Color] = None, not_number: List[int] = None) -> CardMatrix:
    """ Get a card matrix with all the possible cards this card could be. """
    card_matrix: CardMatrix = CardMatrix()

    for c in Color:
        for n in range(1, 6):
            stat = CardStat()
            stat.color = c
            stat.number = n
            stat.probability = get_card_probability(state, player_index, c, n, known_color, known_number,
                                                    not_color, not_number)
            stat.rating_play = get_rating_play(state, player_index, c, n, known_color, known_number)
            stat.rating_discard = get_rating_discard(state, player_index, c, n, known_color, known_number)
            card_matrix.add(stat)

    # To do this we need to know how
    # print(card_matrix)
    return card_matrix


def get_card_probability(
        state: State, player_index: int, c: Color, n: int,
        known_color: Color=None, known_number: int=None,
        not_color: List[Color]=None, not_number: List[int]=None) -> float:

    # Find all cards in the deck.
    counter: CardCounter = CardCounter.deck()

    # Eliminate cards based on what we see.
    seen_cards: List[Card] = []
    seen_cards += state.discard_pile
    seen_cards += state.fireworks

    for i in range(len(state.hands)):
        if i != player_index:
            seen_cards += state.hands[i]

    for card in seen_cards:
        counter.add(card.color, card.number, -1)

    # Eliminate cards we know it cannot be.
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
    return probability


def get_rating_play(
        state: State, player_index: int, c: Color, n: int,
        known_color: Color=None, known_number: int=None) -> float:
    """ Get a rating for this card to be played. """
    if state.is_card_playable(Card(n, c)):
        return 1.0
    return 0.0


def get_rating_discard(
        state: State, player_index: int, c: Color, n: int,
        known_color: Color=None, known_number: int=None) -> float:
    return state.get_discard_score(Card(n, c))


def get_valid_hint_actions(state: State, player_index: int) -> List[ActionHint]:

    actions = []


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
                action = ActionHint(player_index, i, None, c)
                actions.append(action)

            for n in map_numbers:
                action = ActionHint(player_index, i, n, None)
                actions.append(action)

    for action in actions:
        action.rating = get_hint_rating(state, action)

    return actions


def get_hint_rating(state: State, hint: ActionHint) -> float:
    hand = state.get_player_hand(hint.target_index)
    max_gain = -1
    best_matrix = None
    total_gain = 0

    for card in hand:
        original_matrix = get_card_matrix(state, hint.target_index, card.observed_color, card.observed_number)
        post_matrix = original_matrix

        if hint.color is not None and hint.color == card.color:
            # print(f"Get Hint C {hint.color} - {card.color}")
            post_matrix = get_card_matrix(state, hint.target_index, hint.color, card.observed_number)

        if hint.number is not None and hint.number == card.number:
            # print(f"Get Hint R {hint.number} - {card.number}")
            post_matrix = get_card_matrix(state, hint.target_index, card.observed_color, hint.number)

        gain = post_matrix.rating_play - original_matrix.rating_play
        discard_gain = post_matrix.rating_discard - original_matrix.rating_discard

        if post_matrix.rating_play > 0.99 and gain > 0:
            gain = 1

        if post_matrix.rating_discard > 0.99 and discard_gain > 0:
            discard_gain = 1

        gain = min(1, gain)
        discard_gain = min(1, discard_gain)

        total_gain += gain + discard_gain

        if gain > max_gain:
            max_gain = gain
            best_matrix = post_matrix

    # print(f"Hint Analysis: {hint.color} {hint.number} Player {hint.target_index}")
    # print(f"Rating: {max_gain}")
    # print(best_matrix)
    # print()
    return total_gain


def get_matrix(state: State, player_index: int, hand_index: int) -> float:
    pass
