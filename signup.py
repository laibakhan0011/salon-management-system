import tkinter as tk
from tkinter import messagebox, ttk
from auth import create_account


def open_signup_window(parent=None):
    signup_win = tk.Toplevel(parent) if parent else tk.Toplevel()
    signup_win.title("Glow Salon - Sign Up")
    signup_win.geometry("400x500")
    signup_win.configure(bg='#F8F5F2')

    signup_box = tk.Frame(
        signup_win,
        width=350,
        height=450,
        bg="#FFFFFF",
        highlightbackground="#D4AF37",
        highlightthickness=2
    )
    signup_box.place(relx=0.5, rely=0.5, anchor='center')
    signup_box.pack_propagate(False)

    title = tk.Label(
        signup_box,
        text='Create Account',
        font=('Times New Roman', 20, 'bold'),
        bg="#FFFFFF",
        fg="#3B3B3B"
    )
    title.pack(pady=15)

    tk.Label(signup_box, text='Username', bg="#FFFFFF", font=("Arial", 11)).pack(anchor='w', padx=40)
    username_entry = tk.Entry(signup_box, width=30, highlightthickness=2)
    username_entry.pack(pady=5)

    tk.Label(signup_box, text='Email', bg="#FFFFFF", font=("Arial", 11)).pack(anchor='w', padx=40, pady=(10, 0))
    email_entry = tk.Entry(signup_box, width=30, highlightthickness=2)
    email_entry.pack(pady=5)

    tk.Label(signup_box, text='Password', bg="#FFFFFF", font=("Arial", 11)).pack(anchor='w', padx=40, pady=(10, 0))
    password_entry = tk.Entry(signup_box, width=30, show='*', highlightthickness=2)
    password_entry.pack(pady=5)

    tk.Label(signup_box, text='Confirm Password', bg="#FFFFFF", font=("Arial", 11)).pack(anchor='w', padx=40, pady=(10, 0))
    confirm_entry = tk.Entry(signup_box, width=30, show='*', highlightthickness=2)
    confirm_entry.pack(pady=5)

    tk.Label(signup_box, text='Role', bg="#FFFFFF", font=("Arial", 11)).pack(anchor='w', padx=40, pady=(10, 0))
    role_var = tk.StringVar(value="Receptionist")
    role_dropdown = ttk.Combobox(
        signup_box, textvariable=role_var,
        values=["Admin", "Receptionist"], width=27, state="readonly"
    )
    role_dropdown.pack(pady=5)

    def handle_signup():
        username = username_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get()
        confirm = confirm_entry.get()
        role = role_var.get()

        if not username or not email or not password or not confirm:
            messagebox.showerror("Signup Failed", "Please fill in all fields.")
            return

        if password != confirm:
            messagebox.showerror("Signup Failed", "Passwords do not match.")
            return

        if len(password) < 6:
            messagebox.showerror("Signup Failed", "Password must be at least 6 characters.")
            return

        success, message = create_account(username, email, password, role)

        if success:
            messagebox.showinfo("Success", message)
            signup_win.destroy()
        else:
            messagebox.showerror("Signup Failed", message)

    signup_button = tk.Button(
        signup_box,
        text='Sign Up',
        bg="#D4AF37",
        fg="white",
        width=20,
        command=handle_signup
    )
    signup_button.pack(pady=20)