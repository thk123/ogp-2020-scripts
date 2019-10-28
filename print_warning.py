import re

import trello_utility
from start_up import boot


def main():
    client, main_board = boot()
    cowley_board = client.get_board('146gQMLj')
    dsm_board = client.get_board('rsKD2538')
    ost_board = client.get_board('9WVxzf50')

    boards = [main_board]

    for board in boards:
        backlog = trello_utility.get_list('Backlog', board)
        for card in backlog.list_cards():
            if re.search(r'Print') in card.name:


main()
