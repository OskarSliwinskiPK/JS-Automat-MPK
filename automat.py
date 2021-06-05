import random
from mpk_exceptions import NotEnoughMoney, AmountDeducted

from coins import CoinStorage, Coin
from enum import IntEnum


class Tickets(IntEnum):
    NORMAL_20 = 1
    NORMAL_40 = 2
    NORMAL_60 = 3
    REDUCED_20 = 4
    REDUCED_40 = 5
    REDUCED_60 = 6

    def __repr__(self):
        if self.value == Tickets.NORMAL_20:
            return "2.8"
        elif self.value == Tickets.NORMAL_40:
            return "3.8"
        elif self.value == Tickets.NORMAL_60:
            return "5"
        elif self.value == Tickets.REDUCED_20:
            return "1.4"
        elif self.value == Tickets.REDUCED_40:
            return "1.9"
        elif self.value == Tickets.REDUCED_60:
            return "2.5"


class AutomatMpk(CoinStorage):

    def __init__(self):
        super().__init__()
        self._cart = []
        self._price = 0.0
        self._coins = {key: random.randint(0, 5) for key in self._acceptable_values}

    def add_ticket(self, ticket, amount=1):
        if isinstance(ticket, Tickets):
            for _ in range(amount):
                self._cart.append((ticket, ticket.name))

    def add_coins(self, cash):
        if isinstance(cash, CoinStorage):
            merge_coins = lambda x, y: {k: x.get(k, 0) + y.get(k, 0) for k in set(x)}
            self._coins = merge_coins(self.get_coins, cash.get_coins)

    def return_money(self, coins):
        copy_user_coins = coins.get_coins
        coins.clear()
        return copy_user_coins

    def clear_cart(self):
        self._cart = []

    @property
    def tickets(self):
        result = []
        for item in self._cart:
            result.append(item[1])
        return len(result)

    def coins_returned(self, user_coins=None):
        result = []
        for item, amount in user_coins.get_coins.items():
            if amount > 0:
                result.append(f'{item}x{amount}')
                self._coins[item] -= amount
        return result

    @property
    def get_price(self):
        self._price = 0.0
        for ticket_price, ticket_name in self._cart:
            self._price += float(ticket_price.__repr__())
        return self._price.__round__(2)

    def pay(self, user_coins):
        self.add_coins(user_coins)
        if user_coins.balance() < self.get_price:
            raise NotEnoughMoney
        elif user_coins.balance() == self.get_price:
            self._cart = []
            return True, 0
        else:
            change = user_coins.balance() - self.get_price
            change_coins = CoinStorage()
            new_coins = sorted(self._coins.items(), reverse=True)
            for coin, amount in new_coins:
                while change >= coin and amount > 0:
                    change_coins.add(Coin(coin))
                    self._coins[coin] -= 1
                    amount -= 1
                    change = (change - coin).__round__(2)
            if change_coins.balance() < (user_coins.balance() - self.get_price).__round__(2):
                raise AmountDeducted(self.coins_returned(user_coins))
            return True, change_coins
