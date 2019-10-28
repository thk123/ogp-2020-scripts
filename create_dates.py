import datetime
import re

import trello

import election_utility
import trello_utility


def create_dates_interactive(board):
    """
    (Interactive) Creates a range of Date cards on the trello board
    Inclusive
    :param board: The board
    """
    start_date = datetime.datetime.strptime(input('Start date (YYYY-mm-dd): '), '%Y-%m-%d')
    end_date = datetime.datetime.strptime(input('End date (YYYY-mm-dd: '), '%Y-%m-%d')
    frequency = int(input('Days between'))
    return start_date, end_date, frequency


def card_position_date(card):
    #          Start work: 2019-08-25
    pattern = r'Start work: (\d\d\d\d-\d\d-\d\d)'
    match = re.search(pattern, card.description)
    if match:
        card_date_str = match.group(1)
        card_start_date = datetime.datetime.strptime(card_date_str, '%Y-%m-%d')
        return card_start_date
    elif card.due_date:
        return card.due_date
    return None


def create_dates(board, start_date, end_date, frequency):
    date = start_date
    backlog = trello_utility.get_list('Backlog', board)
    date_label = trello_utility.get_label('Date', board)
    while date < end_date:
        create_date(board, date)
        date += datetime.timedelta(days=frequency)


def date_pos(date: datetime.date):
    dt = datetime.datetime.combine(date, datetime.time(1, 0))
    return dt.timestamp()


def card_pos(start_date: datetime.date):
    dt = datetime.datetime.combine(start_date, datetime.time(12, 0))
    return dt.timestamp()


def create_date(board: trello.Board, date: datetime.date, custom_name=None):
    backlog = trello_utility.get_list('Backlog', board)
    date_label = trello_utility.get_label('Date', board)
    if not custom_name:
        custom_name = str(date)

    new_card = backlog.add_card(custom_name)
    try:
        new_card.add_label(date_label)
        new_card.set_due(date)
        new_card.set_pos(date_pos(date))
    except:
        new_card.delete()


def sort_backlog(board):
    backlog = trello_utility.get_list('Backlog', board)
    last_pos = 0

    for card in backlog.list_cards():
        pos = card.pos
        if not election_utility.is_date_card(card):
            card_date = card_position_date(card)
            if card_date:
                pos = card_date.timestamp()
            else:
                pos = last_pos + 1
        else:
            continue
        print("setting " + card.name + " to " + str(pos))
        card.set_pos(pos)
        last_pos = pos


def sort_dates(board):
    backlog = trello_utility.get_list('Backlog', board)

    for date_card in backlog.list_cards():
        if election_utility.is_date_card(date_card):
            date = date_card.due_date.timestamp()
            after_card = False
            last_card = False
            for card in backlog.list_cards():
                if not election_utility.is_date_card(card):
                    if card.pos > date:
                        after_card = card
                        break
                    last_card = card
            if after_card and last_card:
                print("Inserting " + date_card.name + ' between ' + last_card.name + ' and ' + after_card.name)
                date_card.set_pos((last_card.pos + after_card.pos) / 2)


def position_card(board, card):
    if election_utility.is_date_card(card):
        date = card.due_date
        card.set_pos(date_pos(date))
    else:
        date = card_position_date(card)
        if date:
            card.set_pos(date.timestamp())


def sort_board(board):
    backlog = trello_utility.get_list('Backlog', board)
    last_pos = 0

    for card in backlog.list_cards():
        pos = card.pos
        if election_utility.is_date_card(card):
            dd = card.due_date.date()
            dt = datetime.datetime.combine(dd, datetime.time(1, 0))
            pos = dt.timestamp()
        else:
            card_date = card_position_date(card)
            if card_date:
                pos = datetime.datetime.combine(card_date.date(), datetime.time(12, 0)).timestamp()
            else:
                pos = last_pos + 1
        card.set_pos(pos)
        last_pos = pos
