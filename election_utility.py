import klembord
import trello

import produce_list_report
import trello_utility


def copy_email_to_klipboard(board):
    email = produce_list_report.produce_email(board)
    klembord.set_with_rich_text(email.print(), email.print())


def is_date_card(card: trello.Card):
    date_label = trello_utility.get_label("Date", card.board)
    if card.labels:
        return date_label in card.labels
    else:
        return False


def copy_card(card):
    klembord.set_with_rich_text(card.name, '<a href="' + card.url + '">' + card.name + '</a>')

