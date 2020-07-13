import datetime

import create_dates
import trello_utility
from create_dates import position_card


class Prereq:
    def __init__(self, name, due_date: datetime.date, start_date: datetime.date, prereqs, description=''):
        self.name = name
        self.due_date = due_date
        self.start_date = start_date
        self.prereqs = prereqs
        self.desc = description

    @staticmethod
    def from_due_and_time(name, due_date: datetime.date, duration: datetime.timedelta, prereqs, description=''):
        return Prereq(name, due_date, due_date - duration, prereqs, description)


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


def produce_student_leaflet_dependencies(start_delivery_date):
    warn_hillingdon = datetime.timedelta(days=28)
    collect_data_time = datetime.timedelta(days=21)
    print_window = datetime.timedelta(days=7)

    start_printing = start_delivery_date - print_window
    design_window = datetime.timedelta(days=21)
    design_leaflet = Prereq("Design leaflet", start_printing, start_printing - design_window, [])
    collect_register = Prereq("Collect up to date register", start_printing, start_printing - collect_data_time, [])
    warn_hgp = Prereq("Warn Hillingdon Green Print of expected print", start_printing, start_printing - warn_hillingdon,
                      [])

    return Prereq("Print Leaflets", start_delivery_date, start_printing, [design_leaflet, warn_hgp, collect_register])


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


def student_leaflet_dependecies(delivery_date):
    delivery_window = datetime.timedelta(days=7)
    start_delivery = delivery_date - delivery_window

    # allow for more time - need to create an action day for students to come help out
    round_prep_window = datetime.timedelta(days=21)

    return Prereq("Deliver leaflets",
                  delivery_date,
                  start_delivery,
                  [produce_student_leaflet_dependencies(start_delivery),
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
        prereq_card.set_description(create_dates.start_work_prefix + str(prereq.start_date) + '\n\n' + prereq.desc)
        add_prereqs(card, prereq.prereqs, board, goal_label, list)
        dependency_cards.append(prereq_card.url)
        pos = datetime.datetime.combine(prereq.start_date, datetime.time(12, 0)).timestamp()
        prereq_card.set_pos(pos)

    found = False
    for c in card.checklists:
        if c.name == 'TODO':
            found = True
            for item in dependency_cards:
                c.add_checklist_item(item)
            break
    if not found:
        card.add_checklist('TODO', dependency_cards)


def create_ward_newsletter(delivery_date, board, prefix, custom_name=None):
    if not custom_name:
        custom_name = ward_newsletter_name(delivery_date, prefix)
    backlog = trello_utility.get_list("Backlog", board)
    goal_card = backlog.add_card(custom_name)
    goal_card.add_label(trello_utility.get_label('Goal', board))

    goal_label = trello_utility.create_label(custom_name, trello_utility.random_goal_colour(), board)
    goal_card.add_label(goal_label)
    goal_card.set_due(delivery_date)

    prereqs = [leaflet_dependencies(delivery_date)]
    add_prereqs(goal_card, prereqs, board, goal_label, backlog)
    position_card(board, goal_card)
    return goal_card


def create_goal_card(goal_name, board, due_date):
    backlog = trello_utility.get_list("Backlog", board)
    goal_card = backlog.add_card(goal_name)
    goal_card.add_label(trello_utility.get_label('Goal', board))

    goal_label = trello_utility.create_label(goal_name, trello_utility.random_goal_colour(), board)
    goal_card.add_label(goal_label)
    goal_card.set_due(due_date)

    position_card(board, goal_card)
    return goal_card, goal_label

def create_task_card(task_name, board, start_date, due_date, description=''):
    backlog = trello_utility.get_list("Backlog", board)
    goal_card = backlog.add_card(task_name)
    goal_card.set_due(due_date)

    goal_card.set_description(create_dates.start_work_prefix + str(start_date) + '\n\n' + description)

    position_card(board, goal_card)
    return goal_card

def create_short_campaign_literature(delivery_date, board, custom_name, description=''):
    goal_card, goal_label = create_goal_card(custom_name, board, delivery_date)
    goal_card.set_description(description)

    print_prereq = Prereq.from_due_and_time('Print ' + custom_name, delivery_date - datetime.timedelta(days=14),
                                            datetime.timedelta(days=7), [])
    deliver_prereq = Prereq.from_due_and_time('Deliver ' + custom_name, delivery_date, datetime.timedelta(days=7), [])

    prereqs = [print_prereq, deliver_prereq]
    backlog = trello_utility.get_list("Backlog", board)
    add_prereqs(goal_card, prereqs, board, goal_label, backlog)
    position_card(board, goal_card)
    return goal_card

def create_eve_of_poll(polling_date, board):
    goal_card, goal_label = create_goal_card('Eve of poll leaflet', board, polling_date)
    goal_card.set_description('Small postcard with just the camapign messages. To be delivered to all voters on the '
                              'evening before (or early morning of) polling day.')

    print_prereq = Prereq.from_due_and_time('Print Eve of poll leaflet', polling_date - datetime.timedelta(days=14),
                                            datetime.timedelta(days=7), [])
    deliver_prereq = Prereq.from_due_and_time('Deliver eve of poll leaflet', polling_date, datetime.timedelta(days=1), [])

    prereqs = [print_prereq, deliver_prereq]
    backlog = trello_utility.get_list("Backlog", board)
    add_prereqs(goal_card, prereqs, board, goal_label, backlog)
    position_card(board, goal_card)
    return goal_card


def create_student_leaflet(delivery_date, board, prefix, custom_name=None):
    if not custom_name:
        custom_name = ward_newsletter_name(delivery_date, prefix)
    backlog = trello_utility.get_list("Backlog", board)
    goal_card = backlog.add_card(custom_name)
    goal_card.add_label(trello_utility.get_label('Goal', board))

    goal_label = trello_utility.create_label(custom_name, trello_utility.random_goal_colour(), board)
    goal_card.add_label(goal_label)
    goal_card.set_due(delivery_date)

    prereqs = [student_leaflet_dependecies(delivery_date)]
    add_prereqs(goal_card, prereqs, board, goal_label, backlog)
    position_card(board, goal_card)
