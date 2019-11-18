import datetime

import trello_utility
import ward_newsletter
from create_dates import card_pos
from ward_newsletter import Prereq


def target_letter_newsletter_name(delivery_date, prefix):
    month = delivery_date.strftime("%B")
    year = str(delivery_date.year)
    return prefix + ' ' + month + " " + year + " Targetted Letter"


def target_letter_dependencies(delivery_date):
    delivery_window = datetime.timedelta(days=7)
    start_delivery = delivery_date - delivery_window
    print_time = datetime.timedelta(days=7)
    ready_for_print_deadline = start_delivery - print_time
    design_time = datetime.timedelta(days=7)
    ready_for_design_deadline = ready_for_print_deadline - design_time
    decision_time = datetime.timedelta(days=28)

    round_prep_window = datetime.timedelta(days=7)

    return Prereq("Deliver targetted letter",
                  delivery_date,
                  start_delivery,
                  [Prereq("Print letters", start_delivery, ready_for_print_deadline, [
                      Prereq("Design letters", ready_for_print_deadline, ready_for_print_deadline, [
                          Prereq("Decide what letter to do", ready_for_design_deadline,
                                 ready_for_design_deadline - decision_time, [])
                      ])
                  ]),
                   Prereq("Work out how will be delivered", start_delivery, start_delivery - round_prep_window, [])
                   ])


def create_targetted_letter(delivery_date: datetime.date, board, prefix, description=''):
    letter_name = target_letter_newsletter_name(delivery_date, prefix)
    backlog = trello_utility.get_list("Backlog", board)
    goal_card = backlog.add_card(letter_name)
    goal_card.add_label(trello_utility.get_label('Goal', board))

    goal_label = trello_utility.create_label(letter_name, trello_utility.random_goal_colour(), board)
    goal_card.add_label(goal_label)
    goal_card.set_due(delivery_date)
    goal_card.set_pos(card_pos(delivery_date))
    goal_card.set_description(description)

    prereqs = [target_letter_dependencies(delivery_date)]
    ward_newsletter.add_prereqs(goal_card, prereqs, board, goal_label, backlog)
