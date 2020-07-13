import datetime

import trello_utility
from create_dates import position_card
from ward_newsletter import add_prereqs, Prereq


def create_posters(due_date, board):
    create_posters_name = 'Create Posters'
    backlog = trello_utility.get_list("Backlog", board)
    goal_card = backlog.add_card(create_posters_name)
    goal_card.add_label(trello_utility.get_label('Goal', board))

    goal_label = trello_utility.create_label(create_posters_name, trello_utility.random_goal_colour(), board)
    goal_card.add_label(goal_label)
    goal_card.set_due(due_date)

    design_posters_prereq = Prereq.from_due_and_time('Design posters', due_date - datetime.timedelta(days=7),
                                                     datetime.timedelta(days=7), [])
    print_posters_prereq = Prereq.from_due_and_time('Print posters', due_date, datetime.timedelta(days=7), [])

    prereqs = [design_posters_prereq, print_posters_prereq,
               Prereq('Deliver to members', datetime.date(2020, 4, 23), due_date, [])]
    add_prereqs(goal_card, prereqs, board, goal_label, backlog)
    position_card(board, goal_card)
    return goal_card
