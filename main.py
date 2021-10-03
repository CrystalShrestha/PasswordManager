import sqlite3
import hashlib
from tkinter import *
from tkinter import simpledialog
from functools import partial

# Database
with sqlite3.connect("PasswordVault.db") as db:  # Connecting to Database
    cursor = db.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS masterpassword(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vault(
id INTEGER PRIMARY KEY,
website TEXT NOT NULL,
username TEXT NOT NULL,
password TEXT NOT NULL);
""")


# Creating Popup
def popup(text):
    answer = simpledialog.askstring("input string", text)
    return answer


root = Tk()
root.title("Password Vault")
root.wm_iconbitmap("vault.png")


def hashpassword(input):
    hash = hashlib.md5(input)  # Converting text into md5#
    hash = hash.hexdigest()  # Converting md5 into text

    return hash


def ScreenOne():
    root.geometry("250x150+600+350")  # Size
    lbl = Label(root, text="Create Master Password")  # Creating a Label
    lbl.config(anchor=CENTER)  # Aligning the Label to Center
    lbl.pack()  # Generating the created Label
    root.wm_iconbitmap("vault.png")


    text2 = Entry(root, width=20, show="*")
    text2.pack()
    text2.focus()

    label2 = Label(root, text="Re-Enter the Password.")
    label2.pack()

    text3 = Entry(root, width=20, show="*")
    text3.pack()

    lbl1 = Label(root)
    lbl1.pack()

    def SavePasswrd():
        if text2.get() == text3.get():
            hashedPassword = hashpassword(text2.get().encode('utf-8'))  # Strings to Encrypted words

            insert_password = """INSERT INTO masterpassword(password)
            VALUES(?)"""
            cursor.execute(insert_password, [(hashedPassword)])
            db.commit()
            PasswordVault()
        else:
            lbl1.config(text="Passwords do not match. Please try again!")

    button2 = Button(root, text="Save", command=SavePasswrd)
    button2.pack(pady=10)


def loginS():  # Login Screen
    root.geometry("350x100+600+350")  # Size
    lbl = Label(root, text="Enter Master Password")  # Creating a Label
    lbl.config(anchor=CENTER)  # Aligning the Label to Center
    lbl.pack()  # Generating the created Label

    text1 = Entry(root, width=20, show="*")
    text1.pack()
    text1.focus()

    label = Label(root)
    label.pack()

    def getMasterPw():
        checkHashedPassword = hashpassword(text1.get().encode('utf-8'))
        cursor.execute("SELECT * FROM masterpassword WHERE id = 1 AND password = ?", [(checkHashedPassword)])
        print(checkHashedPassword)
        return cursor.fetchall()

    def chkpassword():
        match = getMasterPw()

        print(match)

        if match:
            PasswordVault()
        else:
            text1.delete(0, 'end')  # Deletes the password and clears the input box.
            label.config(text="Incorrect Password")  # Says the password is incorrect if it does not match.

    button = Button(root, text="Login", command=chkpassword)
    button.pack(pady=10)


def PasswordVault():
    for widget in root.winfo_children():  # Clearning all the texts after logging in.
        widget.destroy()

    def addEntry():
        text1 = "Website"
        text2 = "Username"
        text3 = "Password"

        website = popup(text1)
        username = popup(text2)
        password = popup(text3)

        insert_fields = """INSERT INTO vault(website, username, password)
        VALUES(?, ?, ?)
        """
        cursor.execute(insert_fields, (website, username, password))
        db.commit()

        PasswordVault()

    def removeEntry(input):
        cursor.execute("DELETE FROM vault WHERE id = ?", (input,))
        db.commit()

        PasswordVault()

    root.geometry("700x350+400+250")  # Size for the Vault
    label1 = Label(root, text="Password Vault")  # Label for the Vault
    label1.grid(column=1, pady=10)
    root.wm_iconbitmap("vault.png")

    btn = Button(root, text="Add New Password", command=addEntry)
    btn.grid(column=1, pady=10)

    label1 = Label(root, text="Website")
    label1.grid(row=2, column=0, padx=80)
    label1 = Label(root, text="Username")
    label1.grid(row=2, column=1, padx=80)
    label1 = Label(root, text="Password")
    label1.grid(row=2, column=2, padx=80)

    cursor.execute("SELECT * FROM vault")
    if (cursor.fetchall() != None):
        i = 0
        while True:
            cursor.execute("SELECT * FROM vault")
            array = cursor.fetchall()

            lbl1 = Label(root, text=(array[i][1]))
            lbl1.grid(column=0, row=i + 3)  # i+3 because i=0, checking the entry and create a row adding 3.
            lbl1 = Label(root, text=(array[i][2]))
            lbl1.grid(column=1, row=i + 3)
            lbl1 = Label(root, text=(array[i][3]))
            lbl1.grid(column=2, row=i + 3)

            btn = Button(root, text="Delete", command=partial(removeEntry, array[i][0]))  # Button to delete the input
            btn.grid(column=3, row=i + 3, pady=10)

            i = i + 1

            cursor.execute("SELECT * FROM vault")
            if (len(cursor.fetchall()) <= i):
                break


cursor.execute("SELECT * FROM masterpassword")  # Calling the Function
if cursor.fetchall():
    loginS()
else:
    ScreenOne()
root.mainloop()
