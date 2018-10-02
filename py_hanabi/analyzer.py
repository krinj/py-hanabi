# -*- coding: utf-8 -*-

"""
<ENTER DESCRIPTION HERE>
"""

from typing import List
from py_hanabi.card import Color, Card
from py_hanabi.card_matrix import CardMatrix, CardStat, CardCounter
from py_hanabi.state import State

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


def get_card_matrix(state: State, player_index: int, known_color: Color=None, known_number: int=None) -> CardMatrix:
    """ Get a card matrix with all the possible cards this card could be. """
    card_matrix: CardMatrix = CardMatrix()

    for c in Color:
        for n in range(1, 6):
            stat = CardStat()
            stat.color = c
            stat.number = n
            stat.probability = get_card_probability(state, player_index, c, n, known_color, known_number)
            stat.rating_play = get_rating_play(state, player_index, c, n, known_color, known_number)
            stat.rating_discard = get_rating_discard(state, player_index, c, n, known_color, known_number)
            card_matrix.add(stat)

    # To do this we need to know how
    print(card_matrix)
    return card_matrix


def get_card_probability(
        state: State, player_index: int, c: Color, n: int,
        known_color: Color=None, known_number: int=None) -> float:

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

    # Find the count of number of cards.
    card_count = counter.count(c, n)
    total_count = counter.total_count()

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
