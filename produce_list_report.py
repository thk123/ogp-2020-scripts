import urllib

import trello

import trello_utility


def card_text(card, with_date=False):
    if with_date:
        return '<a href=' + card.url + '>' + card.name + ' (' + str(card.due_date.date()) + ')</a>'
    return '<a href=' + card.url + '>' + card.name + '</a>'


def label_link(label: trello.Label):
    name_string = urllib.parse.quote(label.name)
    return 'https://trello.com/b/6o2TiKE8/2020-city-council-elections?menu=filter&filter=label:' + name_string


def html_link(name, url):
    return '<a href="' + url + '">' + name + '</a>'


def print_label(label: trello.Label):
    colours = {
        'yellow': 'd9b51c',
        'purple': '89609e',
        'blue': '0079bf',
        'red': 'b04632',
        'green': '61bd4f',
        'orange': 'cd8313',
        'black': '091e42',
        'sky': '00c2e0',
        'pink': 'ff78cb',
        'lime': '4bbf6b',
        'null': '97a0af'
    }

    format_wrapper = '<i><span style="color:white;background-color: ' + colours[label.color] + '">'
    return '<a href="' + label_link(label) + '">' + format_wrapper + label.name + '</span></i></a>'


class ReportEntry:
    def __init__(self, date, goals, tasks):
        self.date = date
        self.goals = goals
        self.tasks = tasks

    def print(self):
        content = "<h3>" + self.date + "</h3>"
        for goal in self.goals:
            content += "<p><b>Goal: "
            content += card_text(goal)
            content += '</b></p>'
        for task in self.tasks:
            content += "<p>"
            content += card_text(task)
            if task.labels and len(task.labels) == 1:
                content += " (" + print_label(task.labels[0]) + ")"
            content += "</p>"
        return content



class Report:
    def __init__(self):
        self.current_date = None
        self.rolling_tasks = []
        self.entries = []

    def add_date(self, text):
        # if len(list(filter(lambda entry: entry.date == text, self.entries))) > 0:
        #     return
        if self.current_date != None:
            self.entries.append(ReportEntry(self.current_date, self.rolling_goals, self.rolling_tasks))
        self.rolling_goals = []
        self.rolling_tasks = []
        self.current_date = text

    def add_regular_card(self, card):
        self.rolling_tasks.append(card)

    def add_goal_card(self, card):
        self.rolling_goals.append(card)

    def print(self):
        for skipped in self.rolling_tasks:
            print('Skipping tasks:' + str(skipped))
        for skipped in self.rolling_goals:
            print('Skipping goals:' + str(skipped))
        content = ""
        for entry in self.entries:
            content += entry.print()
        return content

    def find_matching_entry(self, entry):
        matching_entry = list(filter(lambda my_entry: my_entry.date == entry.date, self.entries))
        if len(matching_entry) == 1:
            return matching_entry[0]
        if len(matching_entry) > 1:
            raise Exception('Too many dates')
        return None

    def merge(self, report):
        new_entries = []
        for entry in report.entries:
            matching_entry = self.find_matching_entry(entry)
            if matching_entry:
                matching_entry.goals.extend(entry.goals)
                matching_entry.tasks.extend(entry.tasks)
            else:
                new_entries.append(entry)
        self.entries.extend(new_entries)





def card_list(cards, title, with_date=False):
    if len(cards) == 0:
        return ""
    content = ""
    content += "<h2>" + title + "</h2>\n"
    for card in cards:
        content += "<li>" + card_text(card, with_date)
        if card.labels:
            relevant_labels = list(
                filter(lambda label: label.name != 'Goal' and label.name != 'Date' and label.name != 'Event',
                       card.labels))
            if relevant_labels and len(relevant_labels) == 1:
                content += " (<i>" + html_link(relevant_labels[0].name, label_link(relevant_labels[0])) + "</i>)"
        content += "</li>\n"
    content += "</ul>\n"
    return content


class WeeklyUpdate:

    def __init__(self):
        self.completed = []
        self.this_week = []
        self.on_going = []
        self.blocked = []
        self.events = []

    def add_completed_card(self, card):
        self.completed.append(card)

    def add_week_card(self, card):
        self.this_week.append(card)

    def add_on_going_card(self, card):
        self.on_going.append(card)

    def add_blocked_card(self, card):
        self.blocked.append(card)

    def add_event_card(self, card):
        self.events.append(card)

    def print(self):
        content = ""
        content += card_list(self.events, "Upcoming Events", True)
        content += card_list(self.this_week, "This Week")
        content += card_list(self.on_going, "On going")
        content += card_list(self.blocked, "Help Needed!")
        content += card_list(self.completed, "Completed")
        content += "<i>If you're receiving this and you don't think you should be  - let me know!</i>"
        return content


def produce_email(board):
    date_label = trello_utility.get_label('Date', board)
    goal_label = trello_utility.get_label('Goal', board)
    event_label = trello_utility.get_label('Event', board)
    report = WeeklyUpdate()

    this_week = trello_utility.get_list('This Week', board)
    for card in this_week.list_cards():
        if card.labels and event_label in card.labels:
            report.add_event_card(card)
        else:
            report.add_week_card(card)

    blocked = trello_utility.get_list('Help Needed!', board)
    for card in blocked.list_cards():
        report.add_blocked_card(card)

    on_going = trello_utility.get_list('On Going', board)
    for card in on_going.list_cards():
        report.add_on_going_card(card)

    done = trello_utility.get_list('Done', board)
    print(done)
    for card in done.list_cards():
        report.add_completed_card(card)

    backlog = trello_utility.get_list('Backlog', board)
    for card in backlog.list_cards():
        if card.labels and event_label in card.labels:
            report.add_event_card(card)

    return report


def produce_list_report(board, backlog):
    date_label = trello_utility.get_label('Date', board)
    goal_label = trello_utility.get_label('Goal', board)
    report = Report()
    for card in backlog.list_cards():
        if card.labels and date_label in card.labels:
            report.add_date(card.name)
        elif card.labels and goal_label in card.labels:
            report.add_goal_card(card)
        else:
            report.add_regular_card(card)

    return report

def produce_list_report_from_cards(cards, board):
    date_label = trello_utility.get_label('Date', board)
    goal_label = trello_utility.get_label('Goal', board)
    report = Report()
    for card in cards:
        if card.labels and date_label in card.labels:
            report.add_date(card.name)
        elif card.labels and goal_label in card.labels:
            report.add_goal_card(card)
        else:
            report.add_regular_card(card)

    return report
