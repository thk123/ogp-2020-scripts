from unittest import TestCase

from survey_count import parse_marked_register_row, Address, Voted


class TestParse_marked_register_row(TestCase):
    def test_parse_marked_register_row_dnv(self):
        address_result, vote_result = parse_marked_register_row(
            {'address': '123 random road', 'randomColumn': 'noise', 'vote2018': '0'})
        self.assertEqual(address_result, Address('random road', 123))
        self.assertEqual(vote_result, Voted.DNV)

    def test_parse_marked_register_row_pv(self):
        address_result, vote_result = parse_marked_register_row(
            {'address': '123 random road', 'randomColumn': 'noise', 'vote2018': '2'})
        self.assertEqual(address_result, Address('random road', 123))
        self.assertEqual(vote_result, Voted.PV)

    def test_parse_marked_register_row_voted(self):
        address_result, vote_result = parse_marked_register_row(
            {'address': '123 random road', 'randomColumn': 'noise', 'vote2018': '1'})
        self.assertEqual(address_result, Address('random road', 123))
        self.assertEqual(vote_result, Voted.VOTED)

    def test_parse_marked_register_invalid(self):
        with self.assertRaises(Exception) as context:
            parse_marked_register_row({'address': '123 random road', 'missingVoted': ''})
        with self.assertRaises(Exception) as context:
            parse_marked_register_row({'missingAddress': '123 random road', 'vote2018': ''})
        with self.assertRaises(Exception) as context:
            parse_marked_register_row({'address': 'invalid address', 'randomColumn': 'noise', 'vote2018': '1'})
        with self.assertRaises(Exception) as context:
            # invalid voted index
            parse_marked_register_row({'address': 'invalid address', 'randomColumn': 'noise', 'vote2018': '10'})
