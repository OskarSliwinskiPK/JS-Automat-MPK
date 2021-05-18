import unittest
from coins import Coin, CoinStorage
from mpk_exceptions import Error


class MyTestCase(unittest.TestCase):
    def test_coin_class(self):
        self.assertEqual(Coin(5).get_value(), 5)
        with self.assertRaises(Error):
            Coin('a')
        with self.assertRaises(Error):
            Coin(100)

    def test_coin_storage_class(self):
        storage = CoinStorage()
        storage.add(Coin(5))
        self.assertEqual(storage.balance(), 5)
        with self.assertRaises(Error):
            storage.add(Coin('a'))
        with self.assertRaises(Error):
            storage.add(Coin('100'))
        with self.assertRaises(Error):
            storage.add(100)


if __name__ == '__main__':
    unittest.main()
