import unittest

import csvgroup.aggregate as m


class Test_cast_to_type(unittest.TestCase):
    def test_skips_item_if_cannot_cast_to_type(self):
        self.assertEqual(
            m.cast_to_type(
                int,
                ["2", "3", ""]),
            [2, 3])

    def test_returns_empty_list_if_none_can_be_cast(self):
        self.assertEqual(
            m.cast_to_type(
                int,
                ["", "", ""]),
            [])


class Test_aggregate(unittest.TestCase):
    def test_empty_values_are_left_out_of_aggregation(self):
        self.assertEqual(
            m.aggregate(
                lambda v: 1. * sum(v) / len(v),
                ["2", "3", ""],
                int),
            2.5)

    def test_aggregates_to_None_if_every_value_is_empty(self):
        self.assertIsNone(
            m.aggregate(
                lambda v: 1. * sum(v) / len(v),
                ["", "", ""],
                int))
