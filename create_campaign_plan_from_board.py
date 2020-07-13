import argparse

import produce_list_report
import trello_utility
from start_up import boot

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--board', type=str, help='board id', dest='board')
    args = parser.parse_args()

    client, main_board = boot()
    # board = client.get_board(args.board)
    ost_board = client.get_board('9WVxzf50')
    cowley_board = client.get_board('146gQMLj')
    dsm_board = client.get_board('rsKD2538')

    for board in (dsm_board, cowley_board, ost_board):
        print('Generating campaign plan for ' + board.name)
        report = produce_list_report.produce_list_report(board, trello_utility.get_list('Backlog', board))

        with open(board.name + '_short_campaign_plan.html', 'w') as f:
            f.write('<head>')
            f.write('<link rel="stylesheet" type="text/css" href="main.css">')
            f.write('</head>')
            f.write(report.print())


main()