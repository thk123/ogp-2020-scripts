import datetime

import trello

import action_day
import create_dates
import sorry_we_missed_you_card
import targetted_letter
import ward_newsletter


def create_cowley_trello(board: trello.Board):
    ward_name = 'Cowley'
    # board.add_list('Resources')
    # board.add_list('Done')
    # board.add_list('Help Needed!')
    # board.add_list('On Going')
    # board.add_list('This Week')
    # board.add_list('Backlog')
    #
    # board.add_label('Goal', 'green')
    # board.add_label('Date', 'black')
    board.add_label('Event', 'red')

    # create_dates.create_dates(board, datetime.date(year=2019, month=8, day=19), datetime.date(2020, 5, 7), 7)
    #
    # sorry_we_missed_you_card.produce_sorry_we_missed_you_card(board)
    #
    # ward_newsletter.create_ward_newsletter(datetime.date(year=2019, month=9, day=8), board, 'Cowley')
    # ward_newsletter.create_ward_newsletter(datetime.date(year=2019, month=10, day=27), board, 'Cowley')
    # ward_newsletter.create_ward_newsletter(datetime.date(year=2019, month=12, day=1), board, 'Cowley')
    # ward_newsletter.create_ward_newsletter(datetime.date(year=2020, month=1, day=26), board, 'Cowley')
    #
    # targetted_letter.create_targetted_letter(datetime.date(year=2019, month=12, day=10), board, 'Cowley')

    action_day.create_action_day(datetime.date(year=2019, month=8, day=24), board, 'Cowley')
    action_day.create_action_day(datetime.date(year=2019, month=10, day=19), board, 'Cowley')
    action_day.create_action_day(datetime.date(year=2020, month=1, day=18), board, 'Cowley')

    create_dates.sort_board(board)


def create_ost_trello(board: trello.Board):
    ward_name = 'O&ST'

    board.add_list('Resources')
    board.add_list('Done')
    board.add_list('Help Needed!')
    board.add_list('On Going')
    board.add_list('This Week')
    board.add_list('Backlog')

    board.add_label('Goal', 'green')
    board.add_label('Date', 'black')
    board.add_label('Event', 'red')

    create_dates.create_dates(board, datetime.date(year=2019, month=8, day=19), datetime.date(2020, 5, 7), 7)

    sorry_we_missed_you_card.produce_sorry_we_missed_you_card(board)

    ward_newsletter.create_ward_newsletter(datetime.date(year=2019, month=9, day=13), board, ward_name)
    ward_newsletter.create_ward_newsletter(datetime.date(year=2019, month=10, day=27), board, ward_name)
    ward_newsletter.create_ward_newsletter(datetime.date(year=2019, month=12, day=1), board, ward_name)
    ward_newsletter.create_ward_newsletter(datetime.date(year=2020, month=1, day=26), board, ward_name)

    targetted_letter.create_targetted_letter(datetime.date(year=2019, month=12, day=10), board, ward_name)

    action_day.create_action_day(datetime.date(year=2019, month=8, day=31), board, ward_name)

    create_dates.sort_board(board)


def create_dsm_trello(board: trello.Board):
    ward_name = 'D&SM'

    board.add_list('Resources')
    board.add_list('Done')
    board.add_list('Help Needed!')
    board.add_list('On Going')
    board.add_list('This Week')
    board.add_list('Backlog')

    board.add_label('Goal', 'green')
    board.add_label('Date', 'black')
    board.add_label('Event', 'red')

    create_dates.create_dates(board, datetime.date(year=2019, month=8, day=19), datetime.date(2020, 5, 7), 7)

    sorry_we_missed_you_card.produce_sorry_we_missed_you_card(board)

    ward_newsletter.create_ward_newsletter(datetime.date(year=2019, month=9, day=10), board, ward_name)
    ward_newsletter.create_ward_newsletter(datetime.date(year=2019, month=10, day=27), board, ward_name)
    ward_newsletter.create_ward_newsletter(datetime.date(year=2019, month=12, day=1), board, ward_name)
    ward_newsletter.create_ward_newsletter(datetime.date(year=2020, month=1, day=26), board, ward_name)

    targetted_letter.create_targetted_letter(datetime.date(year=2019, month=12, day=10), board, ward_name)

    action_day.create_action_day(datetime.date(year=2019, month=9, day=7), board, ward_name)

    create_dates.sort_board(board)
