import datetime

import trello_utility
import ward_newsletter
from ward_newsletter import Prereq


def year_round_doorknocking(board):
    backlog = trello_utility.get_list("Backlog", board)
    goal_name = 'Complete Initial Door Knock'
    goal_card = backlog.add_card(goal_name)
    door_knocking_description = 'By the start of February, every door on the marked register should be knocked. The ' \
                                'aim ' \
                                'is to have spoken to approximately 50% of those people by this point.\n' \
                                '\n' \
                                'The door knocking should be a mixture of 60 second surveys, petitions and case work ' \
                                'gathering. '

    goal_card.set_description(door_knocking_description)
    goal_card.add_label(trello_utility.get_label('Goal', board))

    goal_label = trello_utility.create_label(goal_name, 'pink', board)
    goal_card.add_label(goal_label)
    goal_card.set_due(datetime.date(day=1, month=2, year=2020))

    final_review_date = datetime.date(day=30, month=11, year=2019)
    final_review_description = 'By this point 75% of the initial door knock should be complete. (Either one or two ' \
                               'complete runs through the marked register)\n' \
                               '\n' \
                               'If this is not the case, discuss with Annie to decide how best to proceed. '

    inital_review_date = datetime.date(day=30, month=9, year=2019)
    initial_review_description = 'By this point canvassing of the marked register be well under way. At this point we ' \
                                 'should be able to estimate:\n' \
                                 '\n' \
                                 ' - how much time at the current rate it will take to get to every door at least once ' \
                                 'by February\n' \
                                 '- whether a second full canvass is required (based on trying to hit 50% spoken to ' \
                                 'by Feb)'

    start_canvassing = datetime.date(day=1, month=9, year=2019)

    prereqs = [
        Prereq('Begin year round canvassing', start_canvassing, start_canvassing - datetime.timedelta(days=7), [],
               'Get a group going for a hour or two every week knocking the marked register and enter the data '),
        Prereq('Review canvassing process', inital_review_date, inital_review_date - datetime.timedelta(days=7), [],
               initial_review_description),
        Prereq('Verify canvassing progress', final_review_date, final_review_date, [], final_review_description)]

    ward_newsletter.add_prereqs(goal_card, prereqs, board, goal_label, backlog)
    goal_card.set_pos(datetime.datetime.combine(goal_card.due_date.date(), datetime.time(12, 0)).timestamp())
