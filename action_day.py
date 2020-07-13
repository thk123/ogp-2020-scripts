import datetime

import trello_utility
import ward_newsletter
from ward_newsletter import Prereq


def action_day_name(delivery_date, ward):
    month = delivery_date.strftime("%B")
    year = str(delivery_date.year)
    return month + " " + year + ' ' + str(ward) + " Action Day"


def action_day_dependencies(date):
    final_reminder = date - datetime.timedelta(days=3)
    send_inital_email = date - datetime.timedelta(days=28)
    ward_call_round = date - datetime.timedelta(days=5)
    create_event = date - datetime.timedelta(days=30)

    return [Prereq("Prepare For Action Day",
                   date,
                   date - datetime.timedelta(days=8),
                   []),
            Prereq("Send Final Reminder", final_reminder, final_reminder, []),
            Prereq("Send initial email", send_inital_email + datetime.timedelta(days=7), send_inital_email, []),
            Prereq("Ward Call Round", ward_call_round, ward_call_round - datetime.timedelta(days=7), []),
            Prereq("Create event", create_event, create_event - datetime.timedelta(days=7), []),
            Prereq("Send round thank yous", date + datetime.timedelta(days=7), date + datetime.timedelta(days=1), [])]


def create_action_day(action_day, board, ward):
    event_name = action_day_name(action_day, ward)
    goal_card, goal_label = ward_newsletter.create_goal_card(event_name, board, action_day)
    goal_card.add_label(trello_utility.get_label('Event', board))

    prereqs = action_day_dependencies(action_day)
    backlog = trello_utility.get_list("Backlog", board)
    ward_newsletter.add_prereqs(goal_card, prereqs, board, goal_label, backlog)
