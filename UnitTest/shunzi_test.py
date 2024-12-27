import unittest

from main import *


class TestShunzi(unittest.TestCase):

    def test_shunzi(self):
        self.assertEqual(check_shunzi_without_recycle([("10",), ("J",), ("Q",), ("K",), ("A",)]), True)
        self.assertEqual(check_shunzi_without_recycle([("10",), ("J",), ("Q",), ("K",), ("2",)]), False)
        self.assertEqual(check_shunzi([("J",), ("Q",), ("K",), ("A",), ("2",)], allow_recycle=True), True)
        self.assertEqual(check_shunzi([("J",), ("Q",), ("K",), ("A",), ("3",)], allow_recycle=True), False)

    def test_tonghua(self):
        self.assertEqual(check_tonghua([("10", "♠"), ("J", "♠"), ("Q", "♠"), ("K", "♠"), ("A", "♠")]), True)
        self.assertEqual(check_tonghua([("10", "♣"), ("J", "♣"), ("Q", "♣"), ("K", "♣"), ("A", "♣")]), True)
        self.assertEqual(check_tonghua([("10", "♦"), ("J", "♦"), ("Q", "♦"), ("K", "♦"), ("A", "♦")]), True)
        self.assertEqual(check_tonghua([("10", "♥"), ("J", "♥"), ("Q", "♥"), ("K", "♥"), ("A", "♥")]), True)
        self.assertEqual(check_tonghua([("10", "♠"), ("J", "♣"), ("Q", "♦"), ("K", "♥"), ("A", "♥")]), False)
        self.assertEqual(check_tonghua([("10", "♣"), ("J", "♠"), ("Q", "♦"), ("K", "♣"), ("A", "♣")]), False)
        self.assertEqual(check_tonghua([("10", "♦"), ("J", "♠"), ("Q", "♦"), ("K", "♦"), ("A", "♦")]), False)
        self.assertEqual(check_tonghua([("10", "♥"), ("J", "♥"), ("Q", "♥"), ("K", "♣"), ("A", "♥")]), False)
