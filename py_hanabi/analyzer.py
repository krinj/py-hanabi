# -*- coding: utf-8 -*-

"""
This class is used to analyze board situations and generate a probability matrix for each event.
"""

from typing import List, Dict
from py_hanabi.card import Color, Card
from py_hanabi.card_matrix import CardMatrix, CardStat, CardCounter
from py_hanabi.commands.command_hint import CommandHint
from py_hanabi.hint_stat import HintStat
from py_hanabi.state import State


__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


def get_card_matrix(state: State, player_index: int, known_color: Color=None, known_number: int=None,
                    not_color: List[Color] = None, not_number: List[int] = None,
                    observed_matrix: Dict[tuple, int] = None) -> CardMatrix:
    """ Get a card matrix with all the possible cards this card could be. """
    card_matrix: CardMatrix = CardMatrix()

    # For each possible card, work out its probability, play rating, and discard rating.
    for c in Color:
        for n in range(1, 6):
            stat = CardStat(c, n)
            stat.probability = get_card_probability(
                state, player_index, c, n, known_color, known_number, not_color, not_number, observed_matrix)
            stat.rating_play = get_rating_play(state, c, n)
            stat.rating_discard = get_rating_discard(state, c, n)
            card_matrix.add(stat)

    return card_matrix


def generate_observed_matrix(state: State, player_index: int, offhand_index: int = None):
    """ Generate a dictionary mapping (card key to count) of all the cards that we can see. """

    # Start off with the known deck.
    counter: CardCounter = CardCounter.deck()
    for card in state.discard_pile:
        counter.add(card.color, card.number, -1)

    for card in state.fireworks:
        counter.add(card.color, card.number, -1)

    for i in range(state.number_of_players):
        if i != player_index:
            for card in state.hands[i]:
                # If this is the offhand player, only include the details we know.
                if offhand_index == i:
                    if not card.hint_received_color or not card.hint_received_number:
                        continue
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
        state: State, c: Color, n: int) -> float:
    """ Get a rating for this card to be played. """
    if state.is_card_playable(Card(n, c)):
        return 1.0
    return 0.0


def get_rating_discard(state: State, c: Color, n: int) -> float:
    """ Get the discard rating for this card. """
    return state.get_discard_score(Card(n, c))


def get_valid_hint_commands(state: State, player_index: int) -> List[CommandHint]:
    """ Get a list of all hints that can be played this round. """
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
        command.hint_stat = get_hint_rating(state, command)

    return commands


def get_hint_rating(state: State, hint: CommandHint) -> HintStat:
    """ For the given hint, give it a score based on what it can accomplish. """

    # Get the prior information.
    hand = state.get_player_hand(hint.target_index)
    observed_matrix = generate_observed_matrix(state, hint.target_index, hint.player_index)

    # HintStat is how we store this hint's effectiveness.
    hint_stat = HintStat()

    for card in hand:

        # Get the probability matrix for the known state, before and after.
        original_matrix = get_card_matrix(
            state, hint.target_index, card.observed_color, card.observed_number,
            observed_matrix=observed_matrix)
        post_matrix = original_matrix

        # Simulate a color hint.
        if hint.color is not None and hint.color == card.color:
            if not card.hint_received_color:
                _set_hint_success(card, hint_stat, state)

            post_matrix = get_card_matrix(
                state, hint.target_index, hint.color, card.observed_number, observed_matrix=observed_matrix)

        # Simulate a number hint.
        if hint.number is not None and hint.number == card.number:
            if not card.hint_received_number:
                _set_hint_success(card, hint_stat, state)

            post_matrix = get_card_matrix(
                state, hint.target_index, card.observed_color, hint.number, observed_matrix=observed_matrix)

            if not card.hint_received_number and hint.number == 5:
                hint_stat.vital_reveal += 1

        gain = post_matrix.rating_play - original_matrix.rating_play
        discard_gain = post_matrix.rating_discard - original_matrix.rating_discard

        if post_matrix.rating_play > 0.99 and gain > 0:
            hint_stat.enables_play += 1

        if post_matrix.rating_discard > 0.99 and discard_gain > 0:
            hint_stat.enables_discard += 1

        hint_stat.total_play_gain += gain
        hint_stat.total_discard_gain += discard_gain

        hint_stat.max_play_gain = max(gain, hint_stat.max_play_gain)
        hint_stat.max_discard_gain = max(gain, hint_stat.max_discard_gain)

    return hint_stat


def _set_hint_success(card, hint_stat, state):
    """ If this hint adds new information, then mark this hint as successful. """
    hint_stat.n_cards_affected += 1
    if state.is_card_playable(card):
        hint_stat.true_playable_cards += 1

