import tkinter
import sqlite3
import tkinter.messagebox
import logging

logging.basicConfig(filename='txn.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def is_valid_decimal(s):
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True


class StudentWallet:
    def __init__(self, ID):
        self.row = []
        self.ID = ID
        self.getData(ID)
        self.balance = str(self.row[0]).strip()
        self.wallet = str(self.row[1]).strip()

        logging.info(f'{self.wallet} just logged in')

        self.root = tkinter.Tk()
        self.root.geometry('400x250')
        self.root.title('Wallet')

        # Frames
        self.walletFrame = tkinter.Frame(self.root)
        self.balanceFrame = tkinter.Frame(self.root)
        self.buttonFrame = tkinter.Frame(self.root)
        self.payFrame = tkinter.Frame(self.root)
        self.payBottomFrame = tkinter.Frame(self.root)

        # Balance Variable
        self.balanceVar = tkinter.StringVar()
        self.balanceVar.set(self.balance)

        # Labels
        self.pageLabel = tkinter.Label(self.root, text='STUDENT WALLET', font='50', bg='#0D97F2')
        self.walletLabel = tkinter.Label(self.walletFrame, text=f'Wallet Number: \t')
        self.walletNumLabel = tkinter.Label(self.walletFrame, text=self.wallet)
        self.balanceLabel = tkinter.Label(self.balanceFrame, text='Balance:', font='50')
        self.balanceVarLabel = tkinter.Label(self.balanceFrame, textvariable=self.balanceVar, font='50',
                                             width=25)  # not working
        self.payInfoLabel = tkinter.Label(self.payFrame, text='if you wish to deposit money to another wallet')
        self.payLabel = tkinter.Label(self.payBottomFrame, text='Wallet Number: \t')
        self.amountLabel = tkinter.Label(self.payFrame, text='Amount:')
        # Buttons
        self.buttonPay = tkinter.Button(self.buttonFrame, text='Pay', command=self.pay)
        self.buttonBack = tkinter.Button(self.buttonFrame, text='Logout', command=self.toSignUp)  # fix

        # Entries
        self.payEntry = tkinter.Entry(self.payBottomFrame, width=20)
        self.amountEntry = tkinter.Entry(self.payFrame, width=10)

        # Packing
        self.pageLabel.pack(ipadx=10, ipady=10, fill='x')

        self.walletFrame.pack()
        self.walletLabel.pack(side='left')
        self.walletNumLabel.pack(side='right')

        self.balanceFrame.pack()
        self.balanceLabel.pack(side='left')
        self.balanceVarLabel.pack(side='right')

        self.payFrame.pack()
        self.payInfoLabel.pack(pady=10)
        self.amountLabel.pack(side='left')
        self.amountEntry.pack(side='right')

        self.payBottomFrame.pack()
        self.payLabel.pack(side='left')
        self.payEntry.pack(side='right')

        self.buttonFrame.pack()
        self.buttonBack.pack(side='left')
        self.buttonPay.pack(side='right')

        self.root.mainloop()

    def getData(self, ID):
        connection = sqlite3.connect('KsuPayDB.db')
        cursor = connection.execute('SELECT BALANCE, WALLET FROM STUDENTS WHERE ID = ?', [ID])
        for row in cursor:
            self.row.append(row[0])
            self.row.append(row[1])

    def pay(self):  # exception handling

        if not is_valid_decimal(str(self.amountEntry.get()).strip()) or int(self.amountEntry.get()) < 0:
            tkinter.messagebox.showerror('showerror','Please enter a valid number')
            return
        conn = sqlite3.connect('KsuPayDB.db')
        cursor = conn.execute('SELECT WALLET FROM STUDENTS WHERE WALLET = ?', [str(self.payEntry.get())])
        toID = None
        for row in cursor:
            toID = str(row[0]).strip()
        amount = float(self.amountEntry.get())
        if float(self.balance) > 0 and float(self.balance) >= float(amount):
            if toID == str(self.payEntry.get()) and str(self.wallet).strip() != str(self.payEntry.get()).strip():
                conn.execute('UPDATE STUDENTS SET BALANCE = (BALANCE + ?) WHERE WALLET = ?', [str(amount), str(self.payEntry.get())])
                conn.commit()
                conn.execute('UPDATE STUDENTS SET BALANCE = (BALANCE - ?) WHERE WALLET = ?', [str(amount), str(self.wallet)])
                conn.commit()
                tkinter.messagebox.showinfo('showinfo',' Payment Complete!')
                self.balance = str(float(self.balance) - amount)
                self.balanceVar.set(str(self.balance))
                logging.info(f'{self.wallet} sends {amount} to {self.payEntry.get()}')
            else:
                cursor = conn.execute('SELECT * FROM ADMIN')
                ll = []
                for _ in cursor:
                    ll.append(_[1])
                if str(self.payEntry.get()) in ll:
                    conn.execute('UPDATE ADMIN SET BALANCE = (BALANCE + ?) WHERE WALLET = ?',
                                 [str(amount), str(self.payEntry.get())])
                    conn.commit()
                    conn.execute('UPDATE STUDENTS SET BALANCE = (BALANCE - ?) WHERE WALLET = ?',
                                 [str(amount), str(self.wallet)])
                    conn.commit()
                    self.balance = str(float(self.balance) - amount)
                    self.balanceVar.set(str(self.balance))
                    logging.info(f'{self.wallet} sents {amount} to {self.payEntry.get()}')
                else:
                    tkinter.messagebox.showerror('showerror', 'please enter the correct wallet number')
                    logging.warning(f'{self.wallet} tried to make invalid transaction (invalid wallet)')
        else:
            tkinter.messagebox.showerror('showerror', 'ERROR: insufficient fund!')
            logging.warning(f'{self.wallet} tried to make invalid transaction (insufficient fund)')
        conn.close()

    def toSignUp(self):
        self.root.destroy()
        import Signup
        Signup.SignUp()