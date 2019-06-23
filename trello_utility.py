def get_list(name, board):
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
        print(label)
        if label.name == name:
            return label
    return None


def create_label(name, colour, board):
    """
    Create a new label of specified name and colour
    :param name:
    :param colour:
    :param board:
    :return:
    """
    return board.add_label(name, colour)