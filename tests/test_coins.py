from unittest import TestCase
from src.coins import CoinStorage, Coin
from src.mpk_exceptions import *


class TestCoin(TestCase):
    def test_get_value(self):
        self.assertEqual(Coin(5).get_value, 5)

    def test_should_not_allow_non_acceptable_values(self):
        with self.assertRaises(Error):
            Coin('a')
        with self.assertRaises(Error):
            Coin(100)

    def test_equal(self):
        coin_1 = Coin(5)
        coin_2 = Coin(5)
        self.assertEqual(coin_1, coin_2)


class TestCoinStorage(TestCase):
    def setUp(self):
        self.wallet = CoinStorage()

    def test_add(self):
        self.wallet.add(Coin(5))
        self.assertEqual(self.wallet.balance(), 5)

    def test_clear(self):
        self.wallet.clear()
        self.assertEqual(self.wallet.balance(), 0)

    def test_balance(self):
        self.wallet.add(Coin(5))
        self.wallet.add(Coin(2), 5)
        self.assertEqual(self.wallet.balance(), 15)

    def test_should_not_allow_non_acceptable_values(self):
        with self.assertRaises(Error):
            self.wallet.add(Coin('a'))
        with self.assertRaises(Error):
            self.wallet.add(Coin('100'))
        with self.assertRaises(Error):
            self.wallet.add(100)