import datetime
import time

import trello_utility


def create_dates(board):
    """
    (Interactive) Creates a range of Date cards on the trello board
    Inclusive
    :param board: The board
    """
    start_date = datetime.datetime.strptime(input('Start date (YYYY-mm-dd): '), '%Y-%m-%d')
    end_date = datetime.datetime.strptime(input('End date (YYYY-mm-dd: '), '%Y-%m-%d')
    frequency = int(input('Days betweem'))

    date = start_date
    backlog = trello_utility.get_list('Backlog', board)
    date_label = trello_utility.get_label('Date', board)
    while date < end_date:
        new_card = backlog.add_card(str(date.date()))
        time.sleep(1)
        new_card.add_label(date_label)
        new_card.set_due(date.date())
        date += datetime.timedelta(days=frequency)
