import datetime

import trello_utility
import ward_newsletter
from ward_newsletter import Prereq


def produce_sorry_we_missed_you_card(board):
    start_date = datetime.date.today() + datetime.timedelta(days=2)
    collect_photos_time = datetime.timedelta(days=5)
    photo_due = start_date + collect_photos_time
    design_time = datetime.timedelta(days=2)
    design_due = photo_due + design_time
    print_time = datetime.timedelta(days=7)

    delivery_date = design_due + print_time

    goal_name = "Out cards"
    backlog = trello_utility.get_list("Backlog", board)
    goal_card = backlog.add_card(goal_name)
    goal_card.add_label(trello_utility.get_label('Goal', board))

    goal_label = trello_utility.create_label(goal_name, "null", board)
    goal_card.add_label(goal_label)
    goal_card.set_due(delivery_date)
    # date_card = ward_newsletter.get_insert_position(delivery_date, board)
    # goal_card.set_pos(date_card.pos - 1)

    prereqs = [Prereq("Print out cards", delivery_date, delivery_date - print_time, [
        Prereq("Design cards", design_due, photo_due, [
            Prereq("Collect candidate photos", photo_due, start_date, [])
        ])])]
    ward_newsletter.add_prereqs(goal_card, prereqs, board, goal_label, backlog)
