import tkinter
import random
import sqlite3
import tkinter.messagebox
import datetime
import tkinter.ttk as ttk
import csv


class Admin:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry('300x450')
        self.root.title("Admin")
        self.AdminLabel = tkinter.Label(self.root, text='KSU ENTITY ADMIN', font='50', bg='#0D97F2')

        # Frames-done
        self.entityFrame = tkinter.Frame(self.root)
        self.walletsFrame = tkinter.Frame(self.root)
        self.balanceFrame = tkinter.Frame(self.root)
        self.buttonFrame = tkinter.Frame(self.root)
        self.backUpFrame = tkinter.Frame(self.root)
        self.nameInfoFrame = tkinter.Frame(self.root)
        self.balanceInfoFrame = tkinter.Frame(self.root)

        # Promts=MM
        self.EntityPrompt = tkinter.Label(self.entityFrame, text='The Entity :')

        # wallet info
        self.walletLabel = tkinter.Label(self.walletsFrame, text='Wallet Number:')
        self.walletVar = tkinter.StringVar()
        self.walletCB = ttk.Combobox(self.walletsFrame, textvariable=self.walletVar)
        self.walletCB['state'] = 'readonly'
        self.makeUpdateCB()

        self.nameInfo = tkinter.Label(self.nameInfoFrame, text='Entity:')
        self.nameVar = tkinter.StringVar()
        self.nameOutput = tkinter.Label(self.nameInfoFrame, textvariable=self.nameVar)
        self.balanceInfo = tkinter.Label(self.balanceInfoFrame, text='Balance:')
        self.balanceVar = tkinter.StringVar()
        self.balanceOutput = tkinter.Label(self.balanceInfoFrame, textvariable=self.balanceVar)

        self.totalBalance = tkinter.Label(self.balanceFrame, text='Total Balance of KSU entities: ')
        self.tBVar = tkinter.StringVar()
        self.BalanceVar = tkinter.Label(self.balanceFrame, textvariable=self.tBVar)
        self.getTotal()

        # Entires=MM
        self.Entity = tkinter.Entry(self.entityFrame, width=50)

        # Buttons=done
        self.buttonBack = tkinter.Button(self.buttonFrame, text='Logout', command=self.logout)
        self.buttonSubmit = tkinter.Button(self.buttonFrame, text='Submit', command=self.submit)
        self.buttonPay = tkinter.Button(self.buttonFrame, text='Stipends', command=self.Pay)
        self.buttonClear = tkinter.Button(self.buttonFrame, text='Cash Out', command=self.clear)
        self.buttonWallet = tkinter.Button(self.walletsFrame, text='Get Info/Refresh', command=self.infoAction)
        self.buttonBackup = tkinter.Button(self.backUpFrame, text='Back Up', command=self.backUpAction)

        # packs
        self.AdminLabel.pack(ipadx=10, ipady=10, fill='x')
        # FRAMES
        self.entityFrame.pack()
        self.buttonFrame.pack()
        self.balanceFrame.pack()
        self.walletsFrame.pack()
        self.nameInfoFrame.pack()
        self.balanceInfoFrame.pack()
        self.backUpFrame.pack()

        # LABELS
        self.EntityPrompt.pack(side="top")
        self.Entity.pack(side="right")

        self.totalBalance.pack()
        self.BalanceVar.pack(pady=10)

        self.walletLabel.pack(side='top')
        self.walletCB.pack()

        self.nameInfo.pack(side='left')
        self.nameOutput.pack(side='right')

        self.balanceInfo.pack(side='left')
        self.balanceOutput.pack(side='right')

        # BUTTONS
        self.buttonBack.pack(side="bottom", pady=10)
        self.buttonSubmit.pack(side="top")
        self.buttonPay.pack(side="right")
        self.buttonClear.pack(side='left')
        self.buttonWallet.pack(side='bottom')
        self.buttonBackup.pack(side='bottom', pady=20)
        self.root.mainloop()

    def logout(self):
        self.root.destroy()
        import Signup
        Signup.SignUp()

    def submit(self):
        if self.Entity.get() == '':
            tkinter.messagebox.showerror('showerror','please enter the wallet name')
            return
        connection = sqlite3.connect('KsuPayDB.db')
        wallet = random.randint(1000000000, 9999999999)
        date = datetime.datetime.now()
        cursor = connection.execute('SELECT WALLET FROM STUDENTS WHERE WALLET = ?', [wallet])
        for row in cursor:
            while row[0] == wallet:
                wallet = random.randint(1000000000, 9999999999)

        query = (self.Entity.get(), wallet, 0, date, 'ENTITY')

        try:
            connection.execute('INSERT INTO ADMIN(ENTITY,WALLET, BALANCE, CREATED, TYPE) VALUES(?, ?, ?, ?, ?);', query)
            connection.commit()
        except sqlite3.IntegrityError:
            tkinter.messagebox.showerror('showerror', 'ERROR:404')
        else:
            tkinter.messagebox.showinfo('showinfo', ' Successful!')
            tkinter.messagebox.showinfo('showinfo', f'''your wallet number is
                                 {wallet}
                                 created at {date}
                                 you will get 0SR as a initial balance!
                                 ''')
        self.makeUpdateCB()
        connection.close()

    def Pay(self):
        connection = sqlite3.connect('KsuPayDB.db')

        connection.execute('UPDATE STUDENTS SET BALANCE = BALANCE+1000 ')
        connection.commit()
        tkinter.messagebox.showinfo('showinfo', '1000SR has been sent to every Student Wallet')
        connection.close()

    def clear(self):
        connection = sqlite3.connect('KsuPayDB.db')

        connection.execute('UPDATE ADMIN set BALANCE =0  ')
        connection.commit()
        tkinter.messagebox.showinfo('showinfo', 'Success')

        self.getTotal()
        connection.close()

    def getTotal(self):
        connection = sqlite3.connect('KsuPayDB.db')
        cursor = connection.execute('SELECT BALANCE FROM ADMIN')
        total = 0
        for row in cursor:
            total += float(row[0])
        self.tBVar.set(str(total))
        connection.close()

    def makeUpdateCB(self):
        conn = sqlite3.connect('KsuPayDB.db')
        cursor = conn.execute('SELECT WALLET FROM ADMIN')
        values = []
        for row in cursor:
            values.append(row[0])
        self.walletCB['values'] = values
        conn.close()

    def infoAction(self):
        conn = sqlite3.connect('KsuPayDB.db')
        if self.walletCB.get() != '':
            cursor = conn.execute('SELECT ENTITY, BALANCE FROM ADMIN WHERE WALLET = ?', [self.walletCB.get()])
            for _ in cursor:
                self.nameVar.set(str(_[0]))
                self.balanceVar.set(str(_[1]))
        conn.close()

    def backUpAction(self):
        file = open(file='AdminBackup.csv', mode='w')
        file2 = open(file='StudentsBackUp.csv', mode='w')
        csvwriter = csv.writer(file)
        csvwriter2 = csv.writer(file2)
        conn = sqlite3.connect('KsuPayDB.db')

        cursor = conn.execute('SELECT * FROM ADMIN')
        for n in cursor:
            csvwriter.writerow(n)

        cursor = conn.execute('SELECT * FROM STUDENTS')
        for n in cursor:
            csvwriter2.writerow(n)

        file.close()
        file2.close()
        conn.close()
        tkinter.messagebox.showinfo('showinfo', 'Back Up Completed')
