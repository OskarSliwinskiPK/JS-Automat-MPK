class Error(Exception):
    """ Raise for an exception in this app """
    pass


class NotValidCoinValue(Error):
    """ When the value does not match the available ones. """
    def __init__(self):
        super().__init__("The value is not available")


class CoinAttributeError(Error):
    """ Only Coin object available. """
    def __init__(self):
        super().__init__("Only COIN object available")


class NotEnoughMoney(Error):
    """ If someone pay too little. """
    def __init__(self):
        super().__init__("Put in more money")


class AmountDeducted(Error):
    """ When there are no suitable coins in the machine. """
    def __init__(self):
        super().__init__("Tylko odliczona kwota")


