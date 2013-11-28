import unittest
import importlib

import csvgroup.map as m


class Test_to_target_expression_pair(unittest.TestCase):
    def test_ValueError_for_empty_rule(self):
        with self.assertRaises(ValueError):
            m.to_target_expression_pair("")

    def test_ValueError_for_missing_target(self):
        with self.assertRaises(ValueError):
            m.to_target_expression_pair("= name.title()")

    def test_ValueError_for_missing_expression(self):
        with self.assertRaises(ValueError):
            m.to_target_expression_pair("name =")

    def test_target_expression_pair_for_proper_rule(self):
        self.assertEqual(
            m.to_target_expression_pair("name = name.title()"),
            ("name", "name.title()"))


class Test_apply_rules(unittest.TestCase):
    items = [dict(
                name="ALYSSA P HACKER",
                breakfast="True",
                lunch="True",
                dinner="False",
                arrives="2013-05-26",
                leaves="2013-06-05"),
             dict(
                name="CY D FECT",
                breakfast="True",
                lunch="True",
                dinner="True",
                arrives="2013-06-01",
                leaves="2013-06-05"),
             dict(
                name="LEM E TWEAKIT",
                breakfast="False",
                lunch="True",
                dinner="False",
                arrives="2013-06-01",
                leaves="2013-06-07")]
    rules = [("name", "name.title()"),
             ("meals", "sum([eval(breakfast), eval(lunch), eval(dinner)])"),
             ("stay",
              ("(datetime.datetime.strptime(leaves, '%Y-%m-%d') "
               + "- datetime.datetime.strptime(arrives, '%Y-%m-%d'))"
               + ".days"))]
    imported_module = importlib.import_module("datetime")

    def setUp(self):
        self.mapped_items = [m.apply_rules(
                                self.rules,
                                item,
                                self.imported_module)
                             for item in self.items]

    def test_existing_column_is_modified(self):
        self.assertEqual(
            [item.get("name") for item in self.mapped_items],
            ["Alyssa P Hacker", "Cy D Fect", "Lem E Tweakit"])

    def test_new_column_is_added(self):
        self.assertEqual(
            [item.get("meals") for item in self.mapped_items],
            [2, 3, 1])

    def test_reference_to_imported_module_works(self):
        self.assertEqual(
            [item.get("stay") for item in self.mapped_items],
            [10, 4, 6])
