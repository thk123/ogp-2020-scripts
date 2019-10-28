import klembord
import trello

import produce_list_report
import trello_utility


def copy_email_to_klipboard(board):
    email = produce_list_report.produce_email(board)
    klembord.set_with_rich_text(email.print(), email.print())


def add_prereqs(card, prereqs, board, goal_label):
    backlog = trello_utility.get_list('Backlog', board)
    dependency_cards = []
    for prereq in prereqs:
        prereq_card = backlog.add_card(prereq['name'])
        prereq_card.add_label(goal_label)
        add_prereqs(prereq_card, prereq['prereqs'], board, goal_label)
        dependency_cards.append(prereq_card.url)

    card.add_checklist('TODO', dependency_cards)


def is_date_card(card: trello.Card):
    date_label = trello_utility.get_label("Date", card.board)
    if card.labels:
        return date_label in card.labels
    else:
        return False


def copy_card(card):
    klembord.set_with_rich_text(card.name, '<a href="' + card.url + '">' + card.name + '</a>')


def create_goal(goal_name, prereqs, board):
    backlog = trello_utility.get_list('Backlog', board)
    goal_card = backlog.add_card(goal_name)
    goal_card.add_label(trello_utility.get_label('Goal', board))

    goal_label = trello_utility.create_label(goal_name, "null", board)
    goal_card.add_label(goal_label)

    add_prereqs(goal_card, prereqs, board, goal_label)


def create_prereq_interactive(name):
    print("Creating pre-req %s" % name)

    prereq_names = []
    while True:
        prereq_name = input("Enter pre-requisite")
        if prereq_name == '':
            break
        prereq_names.append(prereq_name)

    print(prereq_names)

    prereqs = []
    for prereq in prereq_names:
        prereqs.append(create_prereq_interactive(prereq))

    return {'name': name, 'prereqs': prereqs}


def create_goal_interactive():
    goal_name = input('Enter goal name:')
    goal_description = input('Enter goal description')

    prereqs = create_prereq_interactive(goal_name)

    print(str(prereqs['prereqs']))

    print("Run `create_goal(goal_name, goal_description, prereqs, oxford2020_board)` to create the goal")
    return goal_name, goal_description, prereqs['prereqs']
