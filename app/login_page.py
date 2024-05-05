from tkinter import Tk, Button, Label, Toplevel, Frame,Scrollbar, Listbox, StringVar, Entry, W, E, N, S, PhotoImage,END
from tkinter import ttk
from tkinter import messagebox
from main_app import main_app

# Create the app obj
root = Tk()

##################################################################################

root.title("Login")
root.config(background="white")
root.geometry("925x500+300+200")
root.resizable(False, False)

frame=Frame(root, width=350, height=350, bg='white')
frame.place(x=480, y=70)

title_label = Label(frame, text='Sign In', bg='white', fg='#57a1f8', font=('Microsoft YaHei UI Light', 23))
title_label.place(x=100, y=5)

##############     User Name    ##################

def on_entry_user(a):
    name=user_entry.get()
    if name == 'Username':
        user_entry.delete(0, 'end')

def on_leave_user(a):
    name=user_entry.get()
    if name == '':
        user_entry.insert(0, 'Username')

user_entry = Entry(frame, width=25, bg='white', fg='black', border=0, highlightthickness=0, font=('Microsoft YaHei UI Light', 11))
user_entry.place(x=30, y=80)
user_entry.insert(0, 'Username')
user_entry.bind('<FocusIn>', on_entry_user)
user_entry.bind('<FocusOut>', on_leave_user)
Frame(frame, width=295, height=2 , bg='black').place(x=25, y=105)


##############     Password    ###################

def on_entry_password(a):
    password=password_entry.get()
    if password == 'Password':
        password_entry.delete(0, 'end')

def on_leave_password(a):
    password=password_entry.get()
    if password == '':
        password_entry.insert(0, 'Password')

password_entry = Entry(frame, width=25, bg='white', fg='black', border=0 , highlightthickness=0, font=('Microsoft YaHei UI Light', 11))
password_entry.place(x=30, y=140)
password_entry.insert(0, 'Password')
password_entry.bind('<FocusIn>', on_entry_password)
password_entry.bind('<FocusOut>', on_leave_password)
Frame(frame, width=295, height=2 , bg='black').place(x=25, y=165)



#################      Sign In       ################

def signin():
    username = user_entry.get()
    password = password_entry.get()
    if username == 'admin' and password == '1234':
        main_app(root)
    else:
        messagebox.showerror("Invalid", "Invalid username or password")

Button(frame, width=35, pady=7, text='Sign in', bg='#57a1f8', fg='white', border=0, command=signin).place(x=20, y=205)


root.mainloop()
