import tkinter as tk
from tkinter import messagebox
from auth import verify_login

def handle_login():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Login Failed", "Please enter both username and password.")
        return

    role = verify_login(username, password)

    if role is None:
        messagebox.showerror("Login Failed", "Invalid username or password.")
    else:
        messagebox.showinfo("Login Successful", f"Welcome! Logged in as {role}.")
        root.destroy()  # closes the login window

        if role == "Admin":
            open_admin_dashboard()
        elif role == "Receptionist":
            open_receptionist_dashboard()


def open_admin_dashboard():
    admin_win = tk.Tk()
    admin_win.title("Admin Dashboard")
    admin_win.geometry("800x600")
    tk.Label(admin_win, text="Welcome, Admin!", font=("Arial", 20)).pack(pady=50)
    admin_win.mainloop()


def open_receptionist_dashboard():
    reception_win = tk.Tk()
    reception_win.title("Receptionist Dashboard")
    reception_win.geometry("800x600")
    tk.Label(reception_win, text="Welcome, Receptionist!", font=("Arial", 20)).pack(pady=50)
    reception_win.mainloop()


root=tk.Tk()
root.title('Glow Salon Login')
root.geometry("800x600")
root.configure(bg='#F8F5F2')

login_box=tk.Frame(
root,
width=350,
height=350,
bg="#FFFFFF",
highlightbackground="#D4AF37",
highlightthickness=2
)

login_box.place(relx=0.5,rely=0.5,anchor='center')
login_box.pack_propagate(False)

title=tk.Label(
    login_box,
    text='Glow Salon Login',
    font=('Times new roman' , 20 , 'bold'),
    bg="#FFFFFF",
    fg="#3B3B3B"
)
title.pack(pady=20)

username_label=tk.Label(
    login_box,
    text='username',
    bg="#FFFFFF",
    font=("Arial", 12)
)
username_label.pack(anchor='w',padx=40)

username_entry=tk.Entry(
    login_box,
    width=30,
    highlightthickness=3
)

username_entry.pack(pady=5)

password_label=tk.Label(
    login_box,
    text='password',
    bg="#FFFFFF",
    font=("Arial", 12)
)
password_label.pack(anchor='w',padx=40, pady= (50,0) )


password_entry=tk.Entry(
    login_box,
    width=30,
    show='*',
    highlightthickness=3
)
password_entry.pack(pady=5)

login_button=tk.Button(
    login_box,
    text='Login',
    bg="#D4AF37",
    fg="white",
    width=20,
    command=handle_login
)
login_button.pack(pady=30)



root.mainloop()
