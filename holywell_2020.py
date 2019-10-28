import datetime
import sys

import trello

import create_dates
import ward_newsletter
from election_utility import create_custom_card
from start_up import create_trello_client


def clear_board(board: trello.Board):
    for list in board.get_lists('all'):
        list.archive_all_cards()
        list.close()

    preexisting_labels = board.get_labels()
    if preexisting_labels:
        for label in preexisting_labels:
            board.delete_label(label.id)


def create_holywell_campaign_board(board: trello.Board):
    clear_board(board)
    ward_name = 'Holywell'

    board.add_list('Resources')
    board.add_list('Done')
    board.add_list('Help Needed!')
    board.add_list('On Going')
    board.add_list('This Week')
    board.add_list('Backlog')

    board.add_label('Goal', 'green')
    board.add_label('Date', 'black')
    board.add_label('Event', 'red')

    # Michalemas
    create_dates.create_dates(board, datetime.date(year=2019, month=11, day=3),
                              datetime.date(year=2019, month=12, day=1), 7)
    create_dates.create_date(board, datetime.date(year=2019, month=12, day=7), 'End of Michaelmas (1st) Term')

    # Christmas
    create_dates.create_dates(board, datetime.date(year=2019, month=12, day=14),
                              datetime.date(year=2020, month=1, day=12), 7)

    # Hilary
    create_dates.create_date(board, datetime.date(year=2020, month=1, day=19), 'Start of Hilary (2nd) Term')
    create_dates.create_dates(board, datetime.date(year=2020, month=1, day=26),
                              datetime.date(year=2020, month=3, day=7), 7)
    create_dates.create_date(board, datetime.date(year=2020, month=3, day=14), 'End of Hilary (2nd) Term')

    # Easter

    create_dates.create_dates(board, datetime.date(year=2020, month=3, day=21),
                              datetime.date(year=2020, month=4, day=19), 7)

    # Trinity
    create_dates.create_date(board, datetime.date(year=2020, month=4, day=26), 'Start of Trinity (3rd) Term')
    create_dates.create_date(board, datetime.date(year=2020, month=5, day=7), 'Start of Trinity (3rd) Term')

    ward_newsletter.create_student_leaflet(datetime.date(year=2019, month=12, day=6), board, ward_name,
                                           'MT Term Leaflet')
    ward_newsletter.create_student_leaflet(datetime.date(year=2020, month=1, day=26), board, ward_name,
                                           'HT Term Welcome Back Leaflet')
    ward_newsletter.create_student_leaflet(datetime.date(year=2020, month=2, day=23), board, ward_name,
                                           'HT Half-Term Leaflet')
    ward_newsletter.create_student_leaflet(datetime.date(year=2020, month=3, day=13), board, ward_name,
                                           'End of HT Leaflet')

    create_custom_card(board, 'Set up social media accounts', datetime.date(year=2019, month=11, day=9),
                       datetime.date(year=2019, month=10, day=28), "Set up a FB page for both candidates. ")
    create_custom_card(board, 'Get an approved budget for this campaign plan',
                       datetime.date(year=2019, month=11, day=9),
                       datetime.date(year=2019, month=10, day=28),
                       "See Tim's current budget for Holywell, update with new plan and then get East Oxford and Team "
                       "2020 to sign off on it")
    create_custom_card(board, 'Get list of Holywell colleges', datetime.date(year=2019, month=11, day=16),
                       datetime.date(year=2019, month=10, day=28), "Either by looking at map of new boundaries, "
                                                                   "or asking David Newman, figure out exactly what "
                                                                   "colleges are in the new Holywell ward.")

    create_custom_card(board, 'Enter Trinity Term Campaign', datetime.date(year=2019, month=12, day=7),
                       datetime.date(year=2019, month=11, day=20),
                       "Agree with elections committee and East Oxford branch budget for the short campaign and "
                       "update this board with the plan.\nEnsure the plan includes polling day")


def main():
    if len(sys.argv) != 2:
        print("Provide board id to create campaign")
        return 1

    client = create_trello_client()
    board = client.get_board(sys.argv[1])
    print('Generating campaign for board ' + board.name)
    create_holywell_campaign_board(board)


main()
