import sqlite3
import tkinter
import tkinter.messagebox
import random
import re
import datetime

conn = sqlite3.connect('KsuPayDB.db')

try:
    table = """CREATE TABLE STUDENTS 
    (FNAME TEXT NOT NULL,
    LNAME TEXT NOT NULL,
    ID INT PRIMARY KEY NOT NULL,
    PASSWORD VARCHAR(30),
    EMAIL VARCHAR(100),
    PHONE VARCHAR(10),
    WALLET VARCHAR(10) NOT NULL,
    BALANCE REAL,
    CREATED DATE,
    TYPE TEXT);"""
    conn.execute(table)
except Exception:
    pass
try:
    table = '''CREATE TABLE ADMIN
    (ENTITY TEXT NOT NULL,
    WALLET VARCHAR(10) PRIMARY KEY NOT NULL,
    BALANCE REAL,
    CREATED DATE,
    TYPE TEXT);'''
    conn.execute(table)
except Exception:
    pass
conn.close()


class SignUp:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry('300x500')
        self.root.title('KsuPay')
        self.root.iconphoto(False, tkinter.PhotoImage(file='img.png'))
        self.signUpLabel = tkinter.Label(self.root, text='Sign Up', font='50', bg='#0D97F2')
        self.buttonFrame = tkinter.Frame(self.root)

        #  prompts
        self.fNPrompt = tkinter.Label(self.root, text='First Name:')
        self.lNPrompt = tkinter.Label(self.root, text='Last Name:')
        self.idPrompt = tkinter.Label(self.root, text='ID Number:')
        self.pwPrompt = tkinter.Label(self.root, text='Password: ')
        self.cPPrompt = tkinter.Label(self.root, text='Confirm Password:')
        self.emPrompt = tkinter.Label(self.root, text='Email Address:')
        self.pNPrompt = tkinter.Label(self.root, text='Phone Number:')

        #  Entries
        self.fNEntry = tkinter.Entry(self.root, width=20)
        self.lNEntry = tkinter.Entry(self.root, width=20)
        self.idEntry = tkinter.Entry(self.root, width=20)
        self.pwEntry = tkinter.Entry(self.root, width=20, show='*')
        self.cPEntry = tkinter.Entry(self.root, width=20, show='*')
        self.emEntry = tkinter.Entry(self.root, width=20)
        self.pNEntry = tkinter.Entry(self.root, width=20)

        #  Buttons
        self.quitButton = tkinter.Button(self.buttonFrame, text='Quit', command=self.root.destroy)
        self.submitButton = tkinter.Button(self.root, text='Submit', command=self.submitAction)
        self.loginInfo = tkinter.Label(self.buttonFrame, text='Already signed up?')
        self.loginButton = tkinter.Button(self.buttonFrame, text='Login', command=self.toLogin)  # fix

        #  ============ PACKING ============
        #  Information Entering
        self.signUpLabel.pack(ipadx=10, ipady=10, fill='x')

        self.fNPrompt.pack()
        self.fNEntry.pack()

        self.lNPrompt.pack()
        self.lNEntry.pack()

        self.idPrompt.pack()
        self.idEntry.pack()

        self.pwPrompt.pack()
        self.pwEntry.pack()

        self.cPPrompt.pack()
        self.cPEntry.pack()

        self.emPrompt.pack()
        self.emEntry.pack()

        self.pNPrompt.pack()
        self.pNEntry.pack()

        #  Buttons
        self.submitButton.pack()
        self.buttonFrame.pack()
        self.quitButton.pack()
        self.loginInfo.pack(side='left')
        self.loginButton.pack(side='right')

        tkinter.mainloop()

    def submitAction(self):
        check = bool(False)
        if not self.fNEntry.get().isalpha() or self.fNEntry.get() == '':
            tkinter.messagebox.showerror('showerror', 'ERROR: please enter first name letters only')
        elif not self.lNEntry.get().isalpha() or self.lNEntry.get() == '':
            tkinter.messagebox.showerror('showerror', 'ERROR: please enter last name letters only')
        elif not self.idEntry.get().isdecimal() or self.idEntry.get() == '' or len(self.idEntry.get()) != 10:
            tkinter.messagebox.showerror('showerror', 'ERROR: please enter your id decimals only (10-digit)')
        elif not self.checkPasswords():
            return
        elif not self.checkEmail():
            return
        elif not self.checkPhone():
            return
        else:
            check = True

        if check is True:
            self.success()
            self.toLogin()

    def checkEmail(self):
        email = str(self.emEntry.get()).strip()
        x = re.search('^([a-zA-Z0-9\._-]+)@ksu.edu.sa$', email)
        connection = sqlite3.connect('KsuPayDB.db')
        cursor = connection.execute('SELECT EMAIL FROM STUDENTS')
        ll = []
        for _ in cursor:
            ll.append(_[0])
        connection.close()
        if x:
            if email not in ll:
                return True
            else:
                tkinter.messagebox.showerror('showerror', 'this email has already been signed up')
                return False
        else:
            tkinter.messagebox.showerror('showerror', 'ERROR: incorrect Email Address (XXXXXXXX@ksu.edu.sa)')
            return False

    def checkPasswords(self):
        x = re.search('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,}$', self.pwEntry.get())
        if x:
            if self.pwEntry.get() == self.cPEntry.get():
                return True
            else:
                tkinter.messagebox.showerror('showerror', 'ERROR: the passwords doesn\'t match')
        else:
            tkinter.messagebox.showerror('showerror', 'ERROR: incorrect password (at least 6 characters & at least '
                                                      'one capital letter and number)')
            return False

    def checkPhone(self):
        x = re.search('^(05)[0-9]{8}$', self.pNEntry.get())
        connection = sqlite3.connect('KsuPayDB.db')
        cursor = connection.execute('SELECT PHONE FROM STUDENTS')
        ll = []
        for _ in cursor:
            ll.append(_[0])
        connection.close()
        if x:
            if self.pNEntry.get() not in ll:
                return True
            else:
                tkinter.messagebox.showerror('showerror', 'the phone number has already been signed up')
                return False
        else:
            tkinter.messagebox.showerror('showerror', 'ERROR: incorrect Phone Number (05XXXXXXXX, 10-digits)')
            return False

    def success(self):
        connection = sqlite3.connect('KsuPayDB.db')
        wallet = random.randint(1000000000, 9999999999)
        date = datetime.datetime.now()
        cursor = connection.execute('SELECT WALLET FROM ADMIN WHERE WALLET = ?', [wallet])
        for row in cursor:
            while row[0] == wallet:
                wallet = random.randint(1000000000, 9999999999)

        query = (self.fNEntry.get(), self.lNEntry.get(), self.idEntry.get(), self.pwEntry.get(), self.emEntry.get(),
                 self.pNEntry.get(), wallet, 1000, date, 'STUDENT')
        try:
            connection.execute('INSERT INTO STUDENTS(FNAME, LNAME, ID, PASSWORD, EMAIL, PHONE, WALLET, BALANCE, CREATED, TYPE) \
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', query)
            connection.commit()
        except sqlite3.IntegrityError:
            tkinter.messagebox.showerror('showerror', 'ERROR: User Exists')
        else:
            tkinter.messagebox.showinfo('showinfo', 'Signup Successful!')
            tkinter.messagebox.showinfo('showinfo', f'''your wallet number is
                          {wallet}
                          created at {date}
                          you will get 1000SR as a initial balance!
                          ''')
        connection.close()

    def toLogin(self):
        self.root.destroy()
        import Login
        Login.Login()


SignUp()
