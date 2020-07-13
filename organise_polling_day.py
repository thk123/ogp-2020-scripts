import datetime

import trello_utility
from create_dates import position_card
from ward_newsletter import Prereq
import ward_newsletter


def organise_polling_day(board):
    election_day = datetime.date(year=2020, month=5, day=7)
    goal, label = ward_newsletter.create_goal_card('Polling day operation', board, election_day)

    print_prereq = Prereq.from_due_and_time('Find venue', election_day - datetime.timedelta(days=7),
                                            datetime.timedelta(days=45), [])
    knocking_up = Prereq.from_due_and_time('Organise knocking up', election_day, datetime.timedelta(days=2), [])
    telling = Prereq.from_due_and_time('Organise telling', election_day, datetime.timedelta(days=14), [])

    prereqs = [print_prereq, knocking_up, telling]
    backlog = trello_utility.get_list("Backlog", board)
    ward_newsletter.add_prereqs(goal, prereqs, board, label, backlog)
    position_card(board, goal)
    return goal
