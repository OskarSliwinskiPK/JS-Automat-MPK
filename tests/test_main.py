from unittest import TestCase
from automat import AutomatMpk, Tickets
from coins import CoinStorage, Coin
from mpk_exceptions import *


class TestMain(TestCase):
    def setUp(self):
        self.automat = AutomatMpk()
        self.automat.clear()
        self.user_cash = CoinStorage()

    def test_1(self):
        self.automat.add_ticket(Tickets.REDUCED_40)
        self.user_cash.add(Coin(1))
        self.user_cash.add(Coin(0.2), 4)
        self.user_cash.add(Coin(0.1))
        result, change = self.automat.pay(self.user_cash)
        self.assertEqual(result, True)
        self.assertEqual(change, 0)
        self.assertEqual(self.automat.tickets, 0)

    def test_2(self):
        automat_coins = CoinStorage()
        automat_coins.add(Coin(0.1), 10)
        automat_coins.add(Coin(0.5), 10)
        self.automat.add_coins(automat_coins)
        self.automat.add_ticket(Tickets.NORMAL_20)
        self.user_cash.add(Coin(2), 2)
        result, change = self.automat.pay(self.user_cash)
        self.assertEqual(result, True)
        self.assertEqual(change.balance(), 1.2)

    def test_3(self):
        self.automat.clear()
        self.automat.add_ticket(Tickets.NORMAL_20)
        self.user_cash.add(Coin(2), 2)
        with self.assertRaises(AmountDeducted):
            self.automat.pay(self.user_cash)
        self.assertEqual(self.automat.balance(), 0)

    def test_4(self):
        self.automat.add_ticket(Tickets.REDUCED_20)
        self.user_cash.add(Coin(0.01), 100)
        self.user_cash.add(Coin(0.2), 2)
        result, change = self.automat.pay(self.user_cash)
        self.assertEqual(result, True)
        self.assertEqual(change, 0)

    def test_5(self):
        automat_coins = CoinStorage()
        automat_coins.add(Coin(0.1), 10)
        automat_coins.add(Coin(0.5), 10)
        self.automat.add_coins(automat_coins)
        self.automat.add_ticket(Tickets.NORMAL_20)
        self.automat.add_ticket(Tickets.REDUCED_40)
        self.user_cash.add(Coin(2), 3)
        result, change = self.automat.pay(self.user_cash)
        self.assertEqual(result, True)
        self.assertEqual(change.balance(), 1.3)

    def test_6(self):
        self.automat.add_ticket(Tickets.NORMAL_20)
        self.user_cash.add(Coin(1))
        self.user_cash.add(Coin(0.5))
        self.automat.add_ticket(Tickets.REDUCED_20)
        self.user_cash.add(Coin(2))
        self.user_cash.add(Coin(0.5))
        self.user_cash.add(Coin(0.1), 2)
        result, change = self.automat.pay(self.user_cash)
        self.assertEqual(result, True)
        self.assertEqual(change, 0)

    def test_7(self):
        with self.assertRaises(Error):
            self.user_cash.add(Coin(-100))
        with self.assertRaises(ValueError):
            self.user_cash.add(Coin(5), 0.3)