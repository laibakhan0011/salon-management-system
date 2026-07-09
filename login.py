import tkinter as tk
from tkinter import messagebox
from auth import verify_login
from signup import open_signup_window
from customer_login import open_customer_login_window


def handle_login():
    username = username_entry.get().strip()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Login Failed", "Please enter both username and password.")
        return

    role = verify_login(username, password)

    if role is None:
        messagebox.showerror("Login Failed", "Invalid username or password.")
    elif role == "Admin":
        messagebox.showinfo("Login Successful", f"Welcome! Logged in as {role}.")
        root.withdraw()  # hide login window instead of destroying the only Tk root
        open_admin_dashboard()
    elif role == "Receptionist":
        messagebox.showinfo("Login Successful", f"Welcome! Logged in as {role}.")
        root.withdraw()
        open_receptionist_dashboard()
    else:
        messagebox.showerror("Login Failed", f"Unrecognized role '{role}'. Please contact an administrator.")


def open_admin_dashboard():
    admin_win = tk.Toplevel(root)
    admin_win.title("Admin Dashboard")
    admin_win.geometry("800x600")
    tk.Label(admin_win, text="Welcome, Admin!", font=("Arial", 20)).pack(pady=50)
    admin_win.protocol("WM_DELETE_WINDOW", root.destroy)


def open_receptionist_dashboard():
    reception_win = tk.Toplevel(root)
    reception_win.title("Receptionist Dashboard")
    reception_win.geometry("800x600")
    tk.Label(reception_win, text="Welcome, Receptionist!", font=("Arial", 20)).pack(pady=50)
    reception_win.protocol("WM_DELETE_WINDOW", root.destroy)


root = tk.Tk()
root.title('Glow Salon Login')
root.geometry("800x600")
root.configure(bg='#F8F5F2')

login_box = tk.Frame(
    root,
    width=350,
    height=540,
    bg="#FFFFFF",
    highlightbackground="#D4AF37",
    highlightthickness=2
)
login_box.place(relx=0.5, rely=0.5, anchor='center')
login_box.pack_propagate(False)

title = tk.Label(
    login_box,
    text='Glow Salon Login',
    font=('Times New Roman', 20, 'bold'),
    bg="#FFFFFF",
    fg="#3B3B3B"
)
title.pack(pady=20)

username_label = tk.Label(
    login_box,
    text='username',
    bg="#FFFFFF",
    font=("Arial", 12)
)
username_label.pack(anchor='w', padx=40)

username_entry = tk.Entry(
    login_box,
    width=30,
    highlightthickness=3
)
username_entry.pack(pady=5)

password_label = tk.Label(
    login_box,
    text='password',
    bg="#FFFFFF",
    font=("Arial", 12)
)
password_label.pack(anchor='w', padx=40, pady=(25, 0))

password_entry = tk.Entry(
    login_box,
    width=30,
    show='*',
    highlightthickness=3
)
password_entry.pack(pady=5)

login_button = tk.Button(
    login_box,
    text='Login',
    bg="#D4AF37",
    fg="white",
    width=20,
    command=handle_login
)
login_button.pack(pady=20)

signup_label = tk.Label(
    login_box,
    text="Don't have an account? Sign Up",
    bg="#FFFFFF",
    fg="#D4AF37",
    font=("Arial", 9, "underline"),
    cursor="hand2"
)
signup_label.pack(pady=5)
signup_label.bind("<Button-1>", lambda e: open_signup_window(root))

separator = tk.Frame(login_box, height=1, bg="#D4AF37")
separator.pack(fill='x', padx=40, pady=(15, 10))

customer_label = tk.Label(
    login_box,
    text="Are you a customer? Login / Sign Up",
    bg="#FFFFFF",
    fg="#3B3B3B",
    font=("Arial", 9, "underline"),
    cursor="hand2"
)
customer_label.pack(pady=5)
customer_label.bind("<Button-1>", lambda e: open_customer_login_window())

root.mainloop()