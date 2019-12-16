import datetime
from unittest import TestCase
from mock import Mock

from create_dates import card_position_date


def mock_card(description, due_date):
    return Mock(due_date=due_date, description=description)


class TestCard_position_date(TestCase):
    def test_card_position_date_from_desc(self):
        self.assertEqual(card_position_date(mock_card('', None)), None)
        self.assertEqual(card_position_date(mock_card('Nonsense', None)), None)
        self.assertEqual(card_position_date(mock_card('Start work: 2020-01-01', None)),
                         datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0))

    def test_card_positon_date_from_invalid_desc(self):
        # self.assertEqual(card_position_date(mock_card('Start work: 2020-15-01', None)), None)
        self.assertEqual(card_position_date(mock_card('Start work: When we\'re ready', None)), None)

    def test_card_positon_date_due_date(self):
        example_date = datetime.datetime(year=2020, month=1, day=1, hour=16, minute=10)
        self.assertEqual(card_position_date(mock_card('', example_date)), example_date)
        self.assertEqual(card_position_date(mock_card('Nonsense', example_date)), example_date)

    def test_card_positon_date_due_date_and_desc(self):
        self.assertEqual(card_position_date(
            mock_card('Start work: 2020-01-01', datetime.datetime(year=2020, month=2, day=3, hour=16, minute=10))),
                         datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0))
