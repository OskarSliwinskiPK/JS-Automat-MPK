import unittest
from automat import AutomatMpk, Tickets
from coins import CoinStorage, Coin
from mpk_exceptions import *


class TestAutomatMpk(unittest.TestCase):
    def setUp(self):
        self.automat = AutomatMpk()


class TestInit(TestAutomatMpk):
    def test_initial_cart(self):
        self.assertEqual(self.automat.tickets, 0)

    def test_initial_price(self):
        self.assertEqual(self.automat.get_price, 0)

    def test_initial_coins(self):
        self.assertNotEqual(self.automat.balance(), 0)


class TestAdd(TestAutomatMpk):
    def test_add_ticket(self):
        self.automat.add_ticket(Tickets.NORMAL_20)
        self.assertEqual(self.automat.get_price, 2.8)
        self.automat.add_ticket(Tickets.REDUCED_60, 2)
        self.assertEqual(self.automat.get_price, 7.8)

    def test_add_coins(self):
        user_coins = CoinStorage()
        user_coins.add(Coin(5), 2)
        coins = self.automat.balance()
        self.automat.add_coins(user_coins)
        self.assertEqual(self.automat.balance(), coins+user_coins.balance())

    def test_should_not_allow_non_coins(self):
        coins = self.automat.balance()
        self.automat.add_coins(5)
        self.assertEqual(self.automat.balance(), coins)

    def test_clear_cart(self):
        self.automat.clear_cart()
        self.assertEqual(self.automat.get_price, 0)

    def test_should_not_allow_non_tickets(self):
        self.automat.clear_cart()
        self.automat.add_ticket("Ticket")
        self.assertEqual(self.automat.get_price, 0)


class TestPay(TestAutomatMpk):
    def test_pay_calculated_amount(self):
        self.automat.add_ticket(Tickets.NORMAL_20)
        user_coins = CoinStorage()
        user_coins.add(Coin(2))
        user_coins.add(Coin(0.5))
        user_coins.add(Coin(0.1), 3)
        result, change = self.automat.pay(user_coins)
        self.assertEqual(result, True)
        self.assertEqual(change, 0)
        self.assertEqual(self.automat.tickets, 0)

    def test_pay_with_change(self):
        automat_coins = CoinStorage()
        automat_coins.add(Coin(0.1), 10)
        automat_coins.add(Coin(0.5), 10)
        self.automat.add_coins(automat_coins)
        self.automat.add_ticket(Tickets.NORMAL_20)
        user_coins = CoinStorage()
        user_coins.add(Coin(2), 2)
        result, change = self.automat.pay(user_coins)
        self.assertEqual(result, True)
        self.assertEqual(change.balance(), 1.2)

    def test_pay_small_amount(self):
        automat_coins = CoinStorage()
        automat_coins.add(Coin(0.1), 10)
        automat_coins.add(Coin(0.5), 10)
        self.automat.add_coins(automat_coins)
        self.automat.add_ticket(Tickets.NORMAL_20)
        user_coins = CoinStorage()
        user_coins.add(Coin(2))
        with self.assertRaises(NotEnoughMoney):
            self.automat.pay(user_coins)