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
    cart = []
    price = 0.0

    def add_ticket(self, ticket, amount=1):
        if isinstance(ticket, Tickets):
            for _ in range(amount):
                self.cart.append(ticket)

    def get_price(self):
        self.price = 0.0
        for ticket in self.cart:
            self.price += float(ticket.__repr__())
        return self.price.__round__(2)

    def pay(self):
        self.cart = None
        # TODO: realizacja platnosci, zwrot reszty itp.