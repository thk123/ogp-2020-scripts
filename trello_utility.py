import random

import trello


def get_list(name: str, board: trello.Board) -> trello.List:
    """
    Find  an open Trello list of the specified name
    :param name: The name of the list
    :param board: The board
    :return: The list
    """
    for trello_list in board.get_lists('open'):
        if trello_list.name == name:
            return trello_list
    return None


def get_label(name, board):
    """
    Find a label object by name
    :param name:
    :param board:
    :return:
    """
    for label in board.get_labels():
        if label.name == name:
            return label
    return None


def random_goal_colour():
    # removed green, black and red as used for goals, dates and events respectively
    colours = ['yellow', 'purple', 'blue', 'orange', 'sky', 'pink', 'lime']
    return random.choice(colours)


def create_label(name, colour, board):
    """
    Create a new label of specified name and colour
    :param name:
    :param colour:
    :param board:
    :return:
    """
    return board.add_label(name, colour)


def get_cards_with_label(label: trello.Label, board: trello.Board):
    return filter(lambda card: card.labels and label in card.labels, board.get_cards())


def archive_cards(cards):
    for card in cards:
        card.set_closed(True)
