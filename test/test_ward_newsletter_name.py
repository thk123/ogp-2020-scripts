import datetime
from unittest import TestCase

from ward_newsletter import ward_newsletter_name


class TestWard_newsletter_name(TestCase):
    def test_ward_newsletter_name(self):
        self.assertEqual(ward_newsletter_name(datetime.date(1900, 1, 1)), "January 1900 Ward Newsletter")
        self.assertEqual(ward_newsletter_name(datetime.date(2019, 10, 1)), "October 2019 Ward Newsletter")
