import datetime
from unittest import TestCase

from ward_newsletter import leaflet_dependencies, Prereq


class TestLeaflet_dependencies(TestCase):
    def test_leaflet_dependencies(self):
        dependencies = leaflet_dependencies(datetime.date(1900, 7, 12))
        self.assertIsInstance(dependencies, Prereq)
        self.assertEquals(dependencies.due_date, datetime.date(1900, 7, 12))
        self.assertEqual(dependencies.start_date, datetime.date(1900, 6, 28))
        self.assertEqual(len(dependencies.prereqs), 2)

        print_dep = dependencies.prereqs[0]
        self.assertEqual(print_dep.due_date, datetime.date(1900, 6, 28))
        self.assertEqual(print_dep.start_date, datetime.date(1900, 6, 21))
        self.assertEqual(len(print_dep.prereqs), 1)

        design_dep = print_dep.prereqs[0]
        self.assertEqual(design_dep.due_date, datetime.date(1900, 6, 21))
        self.assertEqual(design_dep.start_date, datetime.date(1900, 5, 31))
        self.assertEqual(len(design_dep.prereqs), 0)

        prep_dep = dependencies.prereqs[1]
        self.assertEqual(prep_dep.due_date, datetime.date(1900, 6, 28))
        self.assertEqual(prep_dep.start_date, datetime.date(1900, 6, 21))
        self.assertEqual(len(prep_dep.prereqs), 0)
