import tkinter as tk
import tkinter.messagebox
import sqlite3


class Login:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('200x200')
        self.root.title('KsuPay Login')
        self.root.iconphoto(False, tkinter.PhotoImage(file='img.png'))
        self.loginLabel = tk.Label(self.root, text='Login', font='50', bg='#0D97F2')

        # Frames
        self.userFrame = tk.Frame(self.root)
        self.passFrame = tk.Frame(self.root)
        self.buttonFrame = tk.Frame(self.root)

        #  prompts
        self.usernamePrompt = tk.Label(self.userFrame, text='Username:')
        self.passwordPrompt = tk.Label(self.passFrame, text='Password:')

        #  Entries
        self.usernameEntry = tk.Entry(self.userFrame, width=20)
        self.passEntry = tk.Entry(self.passFrame, width=20, show='*')

        # Buttons
        self.backButton = tk.Button(self.buttonFrame, text='Back', command=self.toSignUp)
        self.loginButton = tk.Button(self.buttonFrame, text='Login', command=self.inputCheck)
        #  Packing
        self.loginLabel.pack(ipadx=10, ipady=10, fill='x')

        self.userFrame.pack()
        self.usernamePrompt.pack(side='left')
        self.usernameEntry.pack(side='right')

        self.passFrame.pack()
        self.passwordPrompt.pack(side='left')
        self.passEntry.pack(side='right')

        self.buttonFrame.pack()
        self.backButton.pack(side='left')
        self.loginButton.pack(side='right')

        self.root.mainloop()

    def inputCheck(self):
        conn = sqlite3.connect('KsuPayDB.db')
        username = str(self.usernameEntry.get()).strip()
        password = str(self.passEntry.get()).strip()

        if username == 'admin' and password == 'admin':
            self.toAdmin()
            return

        if not username.isdecimal() or username == '' or len(username) != 10:
            tkinter.messagebox.showerror('showerror', 'ERROR: the username should be an ID (10-digit)')
            return

        elif password == "":
            tkinter.messagebox.showerror('showerror', 'ERROR: please enter your password')
            return

        cursor = conn.execute('SELECT ID FROM STUDENTS WHERE ID = ?', [username])
        thisID = None
        for row in cursor:
            thisID = str(row[0]).strip()
        if thisID == username:
            cursor = conn.execute('SELECT PASSWORD FROM STUDENTS WHERE ID = ?', [username])
            pwd = None
            for row in cursor:
                pwd = str(row[0]).strip()
            if pwd == password:
                self.toWallet(username)
            else:
                tkinter.messagebox.showinfo('showinfo', 'The password is incorrect')
        else:
            tkinter.messagebox.showinfo('showinfo', 'The username does not exist')
        conn.close()

    def toSignUp(self):
        self.root.destroy()
        import Signup
        Signup.SignUp()

    def toWallet(self, ID):
        self.root.destroy()
        import StudentWallet
        StudentWallet.StudentWallet(ID)

    def toAdmin(self):
        self.root.destroy()
        import Admin
        Admin.Admin()
