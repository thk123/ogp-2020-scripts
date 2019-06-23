import trello_utility


def card_text(card, with_date=False):
    if with_date:
        return '<a href=' + card.url + '>' + card.name + ' (' + str(card.due_date.date()) + ')</a>'
    return '<a href=' + card.url + '>' + card.name + '</a>'


class ReportEntry:
    def __init__(self, date, goals, tasks):
        self.date = date
        self.goals = goals
        self.tasks = tasks

    def print(self):
        content = "<h3>" + self.date + "</h3>"
        for goal in self.goals:
            content += "<p><b>Goal: "
            content += self.card_text(goal)
            content += '</b></p>'
        for task in self.tasks:
            content += "<p>"
            content += self.card_text(task)
            content += "</p>"
        return content


class Report:
    def __init__(self):
        self.rolling_goals = []
        self.rolling_tasks = []
        self.entries = []

    def add_date(self, text):
        self.entries.append(ReportEntry(text, self.rolling_goals, self.rolling_tasks))
        self.rolling_goals = []
        self.rolling_tasks = []

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


def card_list(cards, title, with_date=False):
    content = ""
    content += "<h2>" + title + "</h2>\n"
    for card in cards:
        content += "<li>" + card_text(card, with_date) + "</li>\n"
    content += "</ul>\n"
    return content


class WeeklyUpdate:

    def __init__(self):
        self.completed = []
        self.this_week = []
        self.blocked = []
        self.events = []

    def add_completed_card(self, card):
        self.completed.append(card)

    def add_week_card(self, card):
        self.this_week.append(card)

    def add_blocked_card(self, card):
        self.blocked.append(card)

    def add_event_card(self, card):
        self.events.append(card)

    def print(self):
        content = ""
        content += card_list(self.events, "Upcoming Events", True)
        content += card_list(self.this_week, "This Week")
        content += card_list(self.blocked, "Blocked")
        content += card_list(self.completed, "Completed")
        content += "<i>If you're receiving this and you don't think you should be  - let me know!</i>"
        return content


def produce_email(board):
    date_label = trello_utility.get_label('Date', board)
    goal_label = trello_utility.get_label('Goal', board)
    event_label = trello_utility.get_label('Event', board)
    report = WeeklyUpdate()

    this_week = trello_utility.get_list('This week', board)
    for card in this_week.list_cards():
        if card.labels and event_label in card.labels:
            report.add_event_card(card.name)
        else:
            report.add_week_card(card)

    blocked = trello_utility.get_list('Blocked / On going', board)
    for card in blocked.list_cards():
        report.add_blocked_card(card)

    done = trello_utility.get_list('Done', board)
    print(done)
    for card in done.list_cards():
        report.add_completed_card(card)

    backlog = trello_utility.get_list('Backlog', board)
    for card in backlog.list_cards():
        if card.labels and event_label in card.labels:
            report.add_event_card(card)

    return report


def produce_list_report(board, list):
    date_label = trello_utility.get_label('Date', board)
    goal_label = trello_utility.get_label('Goal', board)
    report = Report()
    for card in list.list_cards():
        if (date_label in card.labels):
            report.add_date(card.name)
        elif goal_label in card.labels:
            report.add_goal_card(card)
        else:
            report.add_regular_card(card)

    return report
