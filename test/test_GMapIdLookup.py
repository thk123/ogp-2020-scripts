import os
from unittest import TestCase

from gmap_lookup import GMapIdLookup, InvalidPlaceException


class TestGMapIdLookup(TestCase):
    def gmap_key(self):
        return os.environ['gmap_key']

    def test_id_of_place(self):
        gmap = GMapIdLookup(self.gmap_key())
        self.assertEqual(gmap.id_of_place("3 Campbell Road, Oxford"), 'ChIJe_70IxbBdkgRPnzclYeX0Jo')
        self.assertEqual(gmap.cache['3 Campbell Road, Oxford'], 'ChIJe_70IxbBdkgRPnzclYeX0Jo')
        self.assertNotEqual(gmap.id_of_place("19 Clive Road Flat 1, Oxford"),
                            gmap.id_of_place("19 Clive Road Flat 3, Oxford"))

    def test_awkward(self):
        gmap = GMapIdLookup(self.gmap_key())
        gmap.id_of_place('13 Isis Court Cornwallis Road, Oxford')
        gmap.id_of_place('Flat 3 Withywind Beauchamp Lane, Oxford')

    def test_invalid_place(self):
        gmap = GMapIdLookup(self.gmap_key())
        with self.assertRaises(InvalidPlaceException):
            gmap.id_of_place('Nonsense Street, Liverpool')

    def test_cache(self):
        gmap = GMapIdLookup(self.gmap_key())
        gmap.load_cache('test_cache.csv')
        self.assertEqual(gmap.id_of_place('13 Road, Oxford'), 'abc123')
        self.assertEqual(gmap.id_of_place('Another, Addres'), 'anc$')

    def test_invalidcache(self):
        gmap = GMapIdLookup(self.gmap_key())
        gmap.load_cache('nonsense.csv')
