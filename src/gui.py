from tkinter import Frame, Toplevel, PhotoImage, Button, Label, Spinbox, IntVar, Tk
import logging as log
from tkinter.constants import *
from src.mpk_exceptions import *
from src.automat import Tickets
from src.coins import *
from tkinter import messagebox
import os
import sys


class App:
    """ Klasa odpowiedzialna za interfejs. """
    def __init__(self, automat, user_wallet):
        log.basicConfig(level=10, format="[%(levelname)s]: %(message)s", stream=sys.stdout)
        self._user_cash = None
        self._tickets_to_buy = None
        self._charge = None
        self.window = Tk()
        self.automat = automat
        self.user_wallet = user_wallet
        self.load_photo()
        self.main_window()
        self.prepare()
        self.window.mainloop()

    def load_photo(self):
        """
        Odczytuje zdjęcia i zapisuje do zmiennych.
        Funkcja jest wywołana w __init__, więc wykonuję się tylko raz.
        """
        self.photo_50 = PhotoImage(file=os.path.abspath("images/z50.png"))
        self.photo_20 = PhotoImage(file=os.path.abspath("images/z20.png"))
        self.photo_10 = PhotoImage(file=os.path.abspath("images/z10.png"))
        self.photo_5 = PhotoImage(file=os.path.abspath("images/z5.png"))
        self.photo_2 = PhotoImage(file=os.path.abspath("images/z2.png"))
        self.photo_1 = PhotoImage(file=os.path.abspath("images/z1.png"))
        self.photo_050 = PhotoImage(file=os.path.abspath("images/g50.png"))
        self.photo_020 = PhotoImage(file=os.path.abspath("images/g20.png"))
        self.photo_010 = PhotoImage(file=os.path.abspath("images/g10.png"))
        self.photo_005 = PhotoImage(file=os.path.abspath("images/g5.png"))
        self.photo_002 = PhotoImage(file=os.path.abspath("images/g2.png"))
        self.photo_001 = PhotoImage(file=os.path.abspath("images/g1.png"))

    def prepare(self):
        """ Ustawia wielkość okna i tytuł. """
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.window.title("Automat biletowy MPK")

    def coins_window(self):
        """ Okno z wyborem wrzucanych monet. """
        wallet_window = Toplevel()
        wallet_window.resizable(0, 0)
        wallet_window.title("Portfel")
        wallet_col1 = Frame(wallet_window)
        wallet_col1.pack(side=LEFT, fill=Y)
        wallet_col2 = Frame(wallet_window)
        wallet_col2.pack(side=LEFT, fill=Y)
        wallet_col3 = Frame(wallet_window)
        wallet_col3.pack(side=LEFT, fill=Y)
        wallet_col4 = Frame(wallet_window)
        wallet_col4.pack(side=LEFT, fill=Y)
        b_money_001 = Button(wallet_col1, image=self.photo_001, overrelief=GROOVE,
                             command=lambda: self.balance(0.01, amount.get()))
        b_money_001.pack(anchor=N)
        b_money_002 = Button(wallet_col1, image=self.photo_002, overrelief=GROOVE,
                             command=lambda: self.balance(0.02, amount.get()))
        b_money_002.pack(anchor=N)
        b_money_005 = Button(wallet_col1, image=self.photo_005, overrelief=GROOVE,
                             command=lambda: self.balance(0.05, amount.get()))
        b_money_005.pack(anchor=N)
        b_money_01 = Button(wallet_col2, image=self.photo_010, overrelief=GROOVE,
                            command=lambda: self.balance(0.1, amount.get()))
        b_money_01.pack(anchor=N)
        b_money_02 = Button(wallet_col2, image=self.photo_020, overrelief=GROOVE,
                            command=lambda: self.balance(0.2, amount.get()))
        b_money_02.pack(anchor=N)
        b_money_05 = Button(wallet_col2, image=self.photo_050, overrelief=GROOVE,
                            command=lambda: self.balance(0.5, amount.get()))
        b_money_05.pack(anchor=N)
        b_money_1 = Button(wallet_col3, image=self.photo_1, overrelief=GROOVE,
                           command=lambda: self.balance(1, amount.get()))
        b_money_1.pack(anchor=N)
        b_money_2 = Button(wallet_col3, image=self.photo_2, overrelief=GROOVE,
                           command=lambda: self.balance(2, amount.get()))
        b_money_2.pack(anchor=N)
        b_money_5 = Button(wallet_col3, image=self.photo_5, overrelief=GROOVE,
                           command=lambda: self.balance(5, amount.get()))
        b_money_5.pack(anchor=N)
        b_money_10 = Button(wallet_col4, image=self.photo_10, overrelief=GROOVE,
                            command=lambda: self.balance(10, amount.get()))
        b_money_10.pack(anchor=N)
        b_money_20 = Button(wallet_col4, image=self.photo_20, overrelief=GROOVE,
                            command=lambda: self.balance(20, amount.get()))
        b_money_20.pack(anchor=N)
        b_money_50 = Button(wallet_col4, image=self.photo_50, overrelief=GROOVE,
                            command=lambda: self.balance(50, amount.get()))
        b_money_50.pack(anchor=N)

        l_amount = Label(wallet_col3, text="ILOŚĆ:")
        l_amount.pack(anchor=N)
        amount = Spinbox(wallet_col4, from_=1, to=100)
        amount.pack(anchor=N)

        l_cash = Label(wallet_col3, text="WRZUCONO", height=2, width=20, foreground="RED")
        l_cash.pack(anchor=N)
        balance = self.user_wallet.balance()
        self._user_cash = Label(wallet_col4, text=balance.__str__(), height=2, width=20, foreground="RED")
        self._user_cash.pack(anchor=N)

    def balance(self, value, amount):
        """
        Funkcja dodająca Monetę i odświeżająca wyświetlaną kwotę wrzuconą przez użytkownika.
        :param value: nominał
        :param amount: liczba monet
        """
        self.user_wallet.add(Coin(value), int(amount))
        user_balance = self.user_wallet.balance()
        self._user_cash.configure(text=user_balance.__str__())

    def ticket(self, ticket, amount):
        """
        Funkcja dodająca bilet do listy i odświeżająca łączną liczbę biletów wybranych przez użytkownika.
        :param ticket: bilet
        :param amount: liczba monet
        """
        self.automat.add_ticket(ticket, int(amount))
        self._tickets_to_buy.configure(text=f"Lączna liczba biletów: {self.automat.tickets}")
        self._charge.configure(text=f"Należność:\n{self.automat.get_price}")

    def pay(self):
        """ Funkcja obsługująca przycisk KUP BILETY. """
        if self._tickets_to_buy is not None and self._user_cash is not None:
            try:
                result, change = self.automat.pay(self.user_wallet)
                if result:
                    if change == 0:
                        messagebox.showinfo('Zakup udany', f"Wyliczona kwota!")
                        log.info(f'Zakup udany. Wyliczona kwota!')
                    else:
                        messagebox.showinfo('Zakup udany', f"Kupiono bilety!\nReszta: {change.balance()}\n"
                                                           f"Zwrot: {self.automat.coins_returned(change)}")
                        log.info(f'Zakup udany, Kupiono bilety!\nReszta: {change.balance()}\n'
                                 f'Zwrot: {self.automat.coins_returned(change)}')
                    self.user_wallet.clear()
                    self.automat.clear_cart()
                    self._tickets_to_buy.configure(text=f"Lączna liczba biletów: {self.automat.tickets}")
                    self._charge.configure(text=f"Należność:\n{self.automat.get_price}")
                    user_balance = self.user_wallet.balance()
                    self._user_cash.configure(text=user_balance.__str__())
            except NotEnoughMoney as e:
                messagebox.showerror('Błąd', e)
                log.error(e)
            except AmountDeducted as e:
                returned = self.automat.coins_returned(self.user_wallet)
                messagebox.showerror('Błąd', f'{e}\nZwrot: {returned}')
                log.error(f'{e}\nZwrot: {returned}')
                self.user_wallet.clear()
                user_balance = self.user_wallet.balance()
                self._user_cash.configure(text=user_balance.__str__())

    def return_money(self):
        """ Funkcja obsługująca przycisk ZWRÓĆ PIENIĄDZE. """
        if self._user_cash is not None:
            try:
                user_balance = self.user_wallet.balance()
                self._user_cash.configure(text=user_balance.__str__())
                returned = self.user_wallet.coins_returned()
                messagebox.showinfo('Zwrot', f"Zwrot monet: {returned}")
                log.info(f'Zwrot, Zwrot monet: {returned}')
            except Exception as e:
                messagebox.showerror('Błąd', e)
                log.error(e)

    def return_tickets(self):
        """ Funkcja obsługująca przycisk USUŃ BILETY. """
        if self._tickets_to_buy is not None:
            try:
                self.automat.clear_cart()
                self._charge.configure(text=f"Należność:\n{self.automat.get_price}")
                self._tickets_to_buy.configure(text=f"Lączna liczba biletów: {self.automat.tickets}")
                messagebox.showinfo('Usuwanie', f"Usunięto bilety z listy!")
                log.info('Usuwanie, Usunięto bilety z listy!')
            except Exception as e:
                messagebox.showerror('Błąd', e)
                log.error(e)

    def main_window(self):
        """ Główne okno programu z wyborem biletów do kupienia. """
        mainframe = Frame(self.window)
        mainframe.grid(column=3, row=1, sticky=(N, W, E, S))
        self._tickets_to_buy = Label(mainframe, text=f"Lączna liczba biletów:\n{self.automat.tickets}", height=4,
                                     width=20, foreground="RED")
        self._tickets_to_buy.grid(column=0, row=4)
        Button(mainframe, text="Bilet normalny 20 min\n2,80zł", height=4, width=20, bg="gray65",
               command=lambda: self.ticket(Tickets.NORMAL_20, number_of_tickets.get())).grid(column=0, row=0)
        Button(mainframe, text="Bilet ulgowy 20 min\n1,40zł", height=4, width=20, bg="gray65",
               command=lambda: self.ticket(Tickets.REDUCED_20, number_of_tickets.get())).grid(column=1, row=0)
        Button(mainframe, text="Bilet normalny 40 min\n3,80zł", height=4, width=20, bg="gray75",
               command=lambda: self.ticket(Tickets.NORMAL_40, number_of_tickets.get())).grid(column=0, row=1)
        Button(mainframe, text="Bilet ulgowy 40 min\n1,90zł", height=4, width=20, bg="gray75",
               command=lambda: self.ticket(Tickets.REDUCED_40, number_of_tickets.get())).grid(column=1, row=1)
        Button(mainframe, text="Bilet normalny 60 min\n5,00zł", height=4, width=20, bg="gray85",
               command=lambda: self.ticket(Tickets.NORMAL_60, number_of_tickets.get())).grid(column=0, row=2)
        Button(mainframe, text="Bilet ulgowy 60 min\n2,50zł", height=4, width=20, bg="gray85",
               command=lambda: self.ticket(Tickets.REDUCED_60, number_of_tickets.get())).grid(column=1, row=2)
        Label(mainframe, text="Liczba biletów:").grid(column=0, row=3)

        amount = IntVar(value=0)
        number_of_tickets = Spinbox(mainframe, from_=1, to=100, textvariable=amount, wrap=True)
        number_of_tickets.grid(column=1, row=3)

        Button(mainframe, text="ZWRÓĆ PIENIĄDZE", height=4, width=20, bg="gray65",
               command=lambda: self.return_money()).grid(column=2, row=0)
        Button(mainframe, text="USUŃ BILETY", height=4, width=20, bg="gray65",
               command=lambda: self.return_tickets()).grid(column=2, row=1)
        Button(mainframe, text="KUP BILETY", height=4, width=20, bg="gray65", foreground="RED",
               command=lambda: self.pay()).grid(column=2, row=2)

        Button(mainframe, text="PORTFEL", height=4, width=20, bg="gray65", foreground="RED",
               command=self.coins_window).grid(column=1, row=4)

        self._charge = Label(mainframe, text=f"Należność:\n{self.automat.get_price}", height=4, width=20,
                             foreground="RED")
        self._charge.grid(column=2, row=4)
