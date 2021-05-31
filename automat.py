import random
from mpk_exceptions import NotEnoughMoney

from coins import CoinStorage
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
    _cart = []
    _price = 0.0

    def __init__(self):
        super().__init__()
        self._coins = {key: random.randint(0, 5) for key in self._acceptable_values}

    def add_ticket(self, ticket, amount=1):
        if isinstance(ticket, Tickets):
            for _ in range(amount):
                self._cart.append((ticket, ticket.name))

    def add_coins(self, cash):
        merge_coins = lambda x, y: {k: x.get(k, 0) + y.get(k, 0) for k in set(x)}
        self._coins = merge_coins(self.get_coins, cash.get_coins)

    @property
    def get_price(self):
        self._price = 0.0
        for ticket_price, ticket_name in self._cart:
            self._price += float(ticket_price.__repr__())
        return self._price.__round__(2)

    def pay(self, user_coins):
        print("Wrzucono: ", user_coins.balance())
        print('Bilety w koszyku: ', self._cart)
        print(f'Trzeba zapłacić: {self.get_price}')
        print(self._coins)
        if user_coins.balance() < self.get_price:
            raise NotEnoughMoney
        elif user_coins.balance() == self.get_price:
            print("Perfect!")
        else:
            change = user_coins.balance() - self.get_price
            coins = []
            new_coins = sorted(self._coins.items(), reverse=True)
            coins_ = self.non_zero()
            for coin, amount in new_coins:
                while change >= coin and amount > 0:
                    coins.append(coin)
                    self._coins[coin] -=1
                    amount -= 1
                    change = (change - coin).__round__(2)
            print(f"Trzeba wydać resztę! {(user_coins.balance() - self.get_price).__round__(2)}")
            print(f"Monety do zwrócenia: {coins}")
            print(sum(coins).__round__(2))
        self._cart = None
