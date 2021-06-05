from automat import AutomatMpk
from coins import CoinStorage
from gui import App
from tkinter import Tk


if __name__ == '__main__':
    mpk = AutomatMpk()
    window = Tk()
    user_wallet = CoinStorage()
    app = App(window, mpk, user_wallet)
    window.mainloop()