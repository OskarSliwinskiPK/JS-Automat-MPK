from automat import AutomatMpk
from coins import CoinStorage
from gui import App


if __name__ == '__main__':
    mpk = AutomatMpk()
    user_wallet = CoinStorage()
    app = App(mpk, user_wallet)