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


