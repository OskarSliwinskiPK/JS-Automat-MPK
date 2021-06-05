from src.automat import AutomatMpk
from src.coins import CoinStorage
from src.gui import App
from tkinter import Tk


if __name__ == '__main__':
    mpk = AutomatMpk()
    user_wallet = CoinStorage()
    app = App(mpk, user_wallet)