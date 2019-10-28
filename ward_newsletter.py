import datetime

import trello_utility
from create_dates import position_card


class Prereq:
    def __init__(self, name, due_date: datetime.date, start_date: datetime.date, prereqs, description=''):
        self.name = name
        self.due_date = due_date
        self.start_date = start_date
        self.prereqs = prereqs
        self.desc = description


def ward_newsletter_name(delivery_date, prefix):
    month = delivery_date.strftime("%B")
    year = str(delivery_date.year)
    return prefix + ' ' + month + " " + year + " Ward Newsletter"


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
        prereq_card.set_description("Start work: " + str(prereq.start_date) + '\n\n' + prereq.desc)
        add_prereqs(prereq_card, prereq.prereqs, board, goal_label, list)
        dependency_cards.append(prereq_card.url)
        pos = datetime.datetime.combine(prereq.start_date, datetime.time(12, 0)).timestamp()
        prereq_card.set_pos(pos)

    card.add_checklist('TODO', dependency_cards)


def create_ward_newsletter(delivery_date, board, prefix):
    goal_name = ward_newsletter_name(delivery_date, prefix)
    backlog = trello_utility.get_list("Backlog", board)
    goal_card = backlog.add_card(goal_name)
    goal_card.add_label(trello_utility.get_label('Goal', board))

    goal_label = trello_utility.create_label(goal_name, "null", board)
    goal_card.add_label(goal_label)
    goal_card.set_due(delivery_date)

    prereqs = [leaflet_dependencies(delivery_date)]
    add_prereqs(goal_card, prereqs, board, goal_label, backlog)
    position_card(board, goal_card)
