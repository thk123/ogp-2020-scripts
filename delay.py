import re

import trello
import datetime

import create_dates
from create_dates import card_start_date
from trello_utility import get_cards_with_label


def delay_card(card: trello.Card, delay_amount):
    if card.due_date != None:
        card.set_due(card.due_date + delay_amount)

    start_date = card_start_date(card)
    if start_date != None:
        new_start_date = start_date + delay_amount
        new_card_description = re.sub(create_dates.start_work_prefix + create_dates.iso_date_format,
                                      create_dates.start_work_prefix + str(new_start_date.date()), card.description)
        card.set_description(new_card_description)

    card.comment('Delayed by ' + str(delay_amount))
    create_dates.position_card(card.board, card)


def delay(board: trello.board, goal_label: trello.label, delay_amount: datetime.timedelta):
    cards = get_cards_with_label(goal_label, board)
    for card in cards:
        delay_card(card, delay_amount)

