import datetime

import election_utility
import trello_utility


class Prereq:
    def __init__(self, name, due_date, start_date, prereqs):
        self.name = name
        self.due_date = due_date
        self.start_date = start_date
        self.prereqs = prereqs


def ward_newsletter_name(delivery_date):
    month = delivery_date.strftime("%B")
    year = str(delivery_date.year)
    return month + " " + year + " Ward Newsletter"


def get_temp_list(board, goal_name):
    if not trello_utility.get_list(goal_name, board):
        return board.add_list(goal_name)
    else:
        return trello_utility.get_list(goal_name, board)


def produce_leaflet_dependency(start_delivery_date):
    print_window = datetime.timedelta(days=7)

    start_printing = start_delivery_date - print_window
    design_window = datetime.timedelta(days=21)
    design_leaflet = Prereq("Design leaflet", start_printing, start_printing - design_window, [])

    return Prereq("Print Leaflets", start_delivery_date, start_printing, [design_leaflet])


def leaflet_dependencies(delivery_date):
    delivery_window = datetime.timedelta(days=14)
    start_delivery = delivery_date - delivery_window

    round_prep_window = datetime.timedelta(days=7)

    return Prereq("Deliver leaflets",
                  delivery_date,
                  start_delivery,
                  [produce_leaflet_dependency(start_delivery),
                   Prereq("Prepare delivery rounds", start_delivery, start_delivery - round_prep_window, [])
                   ])


def add_prereqs(card, prereqs, board, goal_label, list):
    """

    :type goal_label: trello.Label
    :type prereqs: Prereq[]
    """
    dependency_cards = []
    for prereq in prereqs:
        prereq_card = list.add_card(prereq.name)
        prereq_card.set_due(prereq.due_date)
        prereq_card.add_label(goal_label)
        prereq_card.set_description("Start work: " + str(prereq.start_date))
        add_prereqs(prereq_card, prereq.prereqs, board, goal_label, list)
        dependency_cards.append(prereq_card.url)
        insert_before_card = get_insert_position(prereq.start_date, board)
        prereq_card.set_pos(insert_before_card.pos - 1)

    card.add_checklist('TODO', dependency_cards)


def get_insert_position(date, board):
    """
    Get the Date card that is the fist card after the date
    :param date: The date to find the date after
    :param board: Trello board to look for date cards in
    :return: The Date card
    """
    backlog = trello_utility.get_list("Backlog", board)
    cards = backlog.list_cards()
    date_cards = list(filter(election_utility.is_date_card, cards))
    after_date_cards = list(filter(lambda card: card.due_date.date() > date, date_cards))
    print(after_date_cards)
    smallest_date_card = min(after_date_cards, key=lambda card: card.due_date)
    return smallest_date_card


def create_ward_newsletter(delivery_date, board):
    goal_name = ward_newsletter_name(delivery_date)
    backlog = trello_utility.get_list("Backlog", board)
    goal_card = backlog.add_card(goal_name)
    goal_card.add_label(trello_utility.get_label('Goal', board))

    goal_label = trello_utility.create_label(goal_name, "null", board)
    goal_card.add_label(goal_label)
    goal_card.set_due(delivery_date)
    date_card = get_insert_position(delivery_date, board)
    goal_card.set_pos(date_card.pos - 1)

    prereqs = [leaflet_dependencies(delivery_date)]
    add_prereqs(goal_card, prereqs, board, goal_label, backlog)
