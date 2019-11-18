import os
from unittest import TestCase

from gmap_lookup import GMapIdLookup, InvalidPlaceException


class TestGMapIdLookup(TestCase):
    def gmap_key(self):
        return os.environ['gmap_key']

    def test_id_of_place(self):
        gmap = GMapIdLookup(self.gmap_key())
        self.assertEqual(gmap.id_of_place("3 Campbell Road, Oxford"), 'ChIJe_70IxbBdkgRPnzclYeX0Jo')
        self.assertNotEqual(gmap.id_of_place("19 Clive Road Flat 1, Oxford"),
                            gmap.id_of_place("19 Clive Road Flat 3, Oxford"))

    def test_invalid_place(self):
        gmap = GMapIdLookup(self.gmap_key())
        with self.assertRaises(InvalidPlaceException):
            gmap.id_of_place('Nonsense Street, Liverpool')
