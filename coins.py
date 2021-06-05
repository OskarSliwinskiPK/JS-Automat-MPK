from decimal import *
from mpk_exceptions import NotValidCoinValue, CoinAttributeError


class Coin:
    _acceptable_values = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50]

    def __init__(self, value):
        self._value = None
        if value in self._acceptable_values:
            self._value = Decimal(str(value))
        else:
            raise NotValidCoinValue()

    def __eq__(self, other):
        if isinstance(other, Coin):
            return self._value == other._value
        return False

    @property
    def get_value(self):
        return self._value


class CoinStorage:
    _acceptable_values = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50]

    def __init__(self):
        self._coins = {key: 0 for key in self._acceptable_values}

    def add(self, coin, amount=1):
        if isinstance(coin, Coin):
            if isinstance(amount, int):
                for _ in range(amount):
                    self._coins[float(coin.get_value)] += 1
            else:
                raise ValueError()
        else:
            raise CoinAttributeError()

    def clear(self):
        self._coins = {key: 0 for key in self._acceptable_values}

    def return_money(self, coins):
        pass

    def coins_returned(self, user_coins=None):
        result = []
        for item, amount in self.get_coins.items():
            if amount > 0:
                result.append(f'{item}x{amount}')
        self.clear()
        return result

    @property
    def get_coins(self):
        return self._coins

    def balance(self):
        return sum([key*value for key, value in self._coins.items()]).__round__(2)
