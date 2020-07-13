import datetime

import klembord
import trello

import create_dates
import produce_list_report
import trello_utility


def copy_email_to_klipboard(board):
    email = produce_list_report.produce_email(board)
    klembord.set_with_rich_text(email.print(), email.print())


def is_date_card(card: trello.Card):
    date_label = trello_utility.get_label("Date", card.board)
    if not date_label:
        raise Exception("Board doesn't have date label")
    if card.labels:
        return date_label in card.labels
    else:
        return False


def create_custom_card(board: trello.Board, name, due_date, start_date=None, description=None):
    backlog = trello_utility.get_list('Backlog', board)
    if start_date:
        start_work_str = create_dates.start_work_prefix + str(start_date)
        if description:
            description = start_work_str + '\n\n' + description
        else:
            description = start_work_str

    new_card = backlog.add_card(name, description)
    new_card.set_due(datetime.datetime.combine(due_date, datetime.time(12, 0)))
    create_dates.position_card(board, new_card)

def copy_card(card):
    klembord.set_with_rich_text(card.name, '<a href="' + card.url + '">' + card.name + '</a>')
