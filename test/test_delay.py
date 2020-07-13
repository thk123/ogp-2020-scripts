import unittest
import datetime

import dateutil

from delay import delay
from start_up import boot
from trello_utility import get_label


class TestDelay(unittest.TestCase):
    def test_delay_integration(self):
        client, _ = boot()
        test_board = client.get_board('Tc4kcuCu')
        label = get_label('October 2019 Osney & St Thomas Action Day', test_board)

        # Test delaying by one day
        delay(test_board, label, datetime.timedelta(days=1))

        # TODO: this test should create the cards and delete them when they're done
        goal_card = client.get_card('4Q1JZEIW')
        self.assertEqual(goal_card.due_date, datetime.datetime(year=2019, month=10, day=13, hour=0, minute=0, tzinfo=dateutil.tz.tzutc()))

        ward_callround = client.get_card('mCFV3khN')
        self.assertTrue(ward_callround.description.startswith('Start work: 2019-10-01'))
        self.assertEqual(ward_callround.due_date, datetime.datetime(year=2019, month=10, day=8, hour=0, minute=0, tzinfo=dateutil.tz.tzutc()))
        self.assertEqual(ward_callround.get_comments()[-1]['data']['text'], 'Delayed by 1 day, 0:00:00')

        # Reset the cards
        delay(test_board, label, datetime.timedelta(days=-1))




