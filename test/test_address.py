from unittest import TestCase

from survey_count import Address


class TestAddress(TestCase):
    def test_from_full_string(self):
        # todo: don't compress, just have address combine strings
        self.assertEqual(Address.from_full_string('1 Random St'), Address('Random St', 1))
        self.assertEqual(Address.from_full_string('295 Random St'), Address('Random St', 295))
        self.assertEqual(Address.from_full_string('295 Random'), Address('Random', 295))
        # self.assertEqual(Address.from_full_string('295A Random'), Address('Random', '295A'))
        # self.assertEqual(Address.from_full_string('Flat 2 Random'), Address('Random', '295A'))
        with self.assertRaises(Exception) as context:
            Address.from_full_string('NoNumber')
            Address.from_full_string('123')

    def test_equals(self):
        self.assertEqual(Address('Random St', 1), Address('Random St', 1))
        self.assertNotEqual(Address('Random St', 1), Address('Random St', 2))
        self.assertNotEqual(Address('Random St', 1), Address('Other St', 1))
        self.assertNotEqual(Address('Random St', 1), Address('Other St', 2))
