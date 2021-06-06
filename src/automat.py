import random
from src.mpk_exceptions import NotEnoughMoney, AmountDeducted, CoinStorageAttributeError

from src.coins import CoinStorage, Coin
from enum import IntEnum


class Tickets(IntEnum):
    """ Klasa dziedzicząca po IntEnum przechowująca dostępne do zakupu bilety i ich ceny. """
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
    """ Klasa dziedzicząca po CoinStorage odpowiadająca za główną logikę programu. """
    def __init__(self):
        """
        :var self._cart: lista biletów do zakupu
        :var self._price: kwota do zapłaty
        :var self._coins: monety dostępne w automacie (inicjowane losowymi liczbami 0-5 na start)
        """
        super().__init__()
        self._cart = []
        self._price = 0.0
        self._coins = {key: random.randint(0, 5) for key in self._acceptable_values}

    def add_ticket(self, ticket, amount=1):
        """
        Dodawanie biletu/biletów do listy zakupowej.
        :param ticket: atrybut klasy Tickets
        :param amount: liczba biletów (int) domyślnie 1
        """
        if isinstance(ticket, Tickets):
            for _ in range(amount):
                self._cart.append((ticket, ticket.name))

    def add_coins(self, cash):
        """
        Dodaje monety do automatu.
        :param cash: Obiekt klasy CoinStorage
        """
        if isinstance(cash, CoinStorage):
            merge_coins = lambda x, y: {k: x.get(k, 0) + y.get(k, 0) for k in set(x)}
            self._coins = merge_coins(self.get_coins, cash.get_coins)

    def return_money(self, coins):
        """
        Metoda nadpisana.
        Czyści przekazany portfel i zwraca monety.
        :param coins: Obiekt klasy CoinStorage
        :return: dict zawierający nominały i liczbę monet
        """
        if isinstance(coins, CoinStorage):
            copy_user_coins = coins.get_coins
            coins.clear()
            return copy_user_coins

    def clear_cart(self):
        """ Czyści koszyk. """
        self._cart = []

    @property
    def tickets(self):
        """
        :return: Liczba biletów w koszyku
        """
        result = []
        for item in self._cart:
            result.append(item[1])
        return len(result)

    def coins_returned(self, user_coins=None):
        """
        Metoda nadpisana. Zwraca monety wrzucone przez użytkownika i odejmuje je od monet automatu.
        :param user_coins: Obiekt klasy CoinStorage
        :return: listę zwróconych monet
        """
        result = []
        if isinstance(user_coins, CoinStorage):
            for item, amount in user_coins.get_coins.items():
                if amount > 0:
                    result.append(f'{item}x{amount}')
                    self._coins[item] -= amount
        return result

    @property
    def get_price(self):
        """
        Funkcja do wyliczania ceny zamówienia.
        :return: Kwota do zapłaty
        """
        self._price = 0.0
        for ticket_price, ticket_name in self._cart:
            self._price += float(ticket_price.__repr__())
        return self._price.__round__(2)

    def pay(self, user_coins):
        """
        Funkcja obsługująca płatność.
        Jeśli wrzucona kwota jest za mała wyrzuca wyjątek NotEnoughMoney
        :param user_coins: Obiekt klasy CoinStorage - portfel klienta
        :return: True, 0 jeśli reszta jest niepotrzebna, True, change_coins - jeśli reszta jest wymagana (change_coins
        obiekt klasy CoinStorage)
        """
        if not isinstance(user_coins, CoinStorage):
            raise CoinStorageAttributeError
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
